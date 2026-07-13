"""
Drawing Scene - KozbenSal
Main drawing interface with eye-controlled cursor.
"""

import pygame
import numpy as np
from typing import List, Tuple, Optional
from enum import Enum


class DrawMode(Enum):
    """Drawing modes."""
    NONE = 0          # Waiting for first point
    WAITING = 1       # First point placed, waiting for second
    PREVIEW = 2       # Showing line preview between points


class Stroke:
    """Represents a single continuous stroke."""

    def __init__(self, color: Tuple[int, int, int] = (0, 0, 0), thickness: int = 3):
        self.points: List[Tuple[int, int]] = []
        self.color = color
        self.thickness = thickness

    def add_point(self, x: int, y: int):
        """Add a point to the stroke."""
        self.points.append((x, y))

    def draw(self, surface: pygame.Surface):
        """Draw the stroke on a surface."""
        if len(self.points) < 2:
            return

        pygame.draw.lines(surface, self.color, False, self.points, self.thickness)


class DrawingCanvas:
    """Main drawing canvas with eye-controlled cursor."""

    def __init__(self, width: int, height: int):
        """
        Initialize drawing canvas.

        Args:
            width: Canvas width
            height: Canvas height
        """
        self.width = width
        self.height = height

        # Canvas surface
        self.canvas = pygame.Surface((width, height))
        self.canvas.fill((255, 255, 255))

        # Drawing state
        self.strokes: List[Stroke] = []
        self.current_stroke: Optional[Stroke] = None
        self.draw_mode = DrawMode.NONE

        # Cursor position
        self.cursor_x = width // 2
        self.cursor_y = height // 2

        # Point-to-point drawing
        self.first_point: Optional[Tuple[int, int]] = None
        self.second_point: Optional[Tuple[int, int]] = None

        # Drawing settings
        self.draw_color = (0, 0, 0)
        self.draw_thickness = 3

        # Grid
        self.show_grid = False
        self.grid_spacing = 20

    def update_cursor(self, x: int, y: int):
        """
        Update cursor position from gaze coordinates.

        Args:
            x: X coordinate
            y: Y coordinate
        """
        self.cursor_x = x
        self.cursor_y = y

    def on_blink(self):
        """
        Handle blink event - places points and draws lines.

        Logic:
        - First blink: place first point
        - Second blink: place second point and draw line between them
        """
        if self.draw_mode == DrawMode.NONE:
            # Place first point
            self.first_point = (self.cursor_x, self.cursor_y)
            self.draw_mode = DrawMode.WAITING
            print(f"Point 1 placed at {self.first_point}")

        elif self.draw_mode == DrawMode.WAITING:
            # Place second point and draw line
            self.second_point = (self.cursor_x, self.cursor_y)

            # Create a stroke with these two points
            stroke = Stroke(self.draw_color, self.draw_thickness)
            stroke.add_point(self.first_point[0], self.first_point[1])
            stroke.add_point(self.second_point[0], self.second_point[1])
            self.strokes.append(stroke)

            print(f"Point 2 placed at {self.second_point}, line drawn!")

            # Reset for next line
            self.first_point = None
            self.second_point = None
            self.draw_mode = DrawMode.NONE

    def undo(self):
        """Undo last stroke."""
        if self.strokes:
            self.strokes.pop()

    def undo_point(self):
        """Remove last point from current stroke."""
        if self.current_stroke is not None and self.current_stroke.points:
            self.current_stroke.points.pop()

    def clear(self):
        """Clear all strokes and reset state."""
        self.strokes.clear()
        self.current_stroke = None
        self.draw_mode = DrawMode.NONE
        self.first_point = None
        self.second_point = None
        self.canvas.fill((255, 255, 255))

    def toggle_grid(self):
        """Toggle grid visibility."""
        self.show_grid = not self.show_grid

    def render(self) -> pygame.Surface:
        """
        Render canvas with all strokes.

        Returns:
            Rendered surface
        """
        # Clear canvas
        self.canvas.fill((255, 255, 255))

        # Draw grid if enabled
        if self.show_grid:
            grid_color = (220, 220, 220)
            for x in range(0, self.width, self.grid_spacing):
                pygame.draw.line(self.canvas, grid_color, (x, 0), (x, self.height), 1)
            for y in range(0, self.height, self.grid_spacing):
                pygame.draw.line(self.canvas, grid_color, (0, y), (self.width, y), 1)

        # Draw all completed strokes
        for stroke in self.strokes:
            stroke.draw(self.canvas)

        # Draw first point if placed
        if self.first_point is not None:
            pygame.draw.circle(self.canvas, (0, 255, 0), self.first_point, 8, -1)
            # Draw preview line from first point to cursor
            pygame.draw.line(self.canvas, (150, 150, 150),
                           self.first_point, (self.cursor_x, self.cursor_y), 2)

        return self.canvas

    def draw_cursor(self, surface: pygame.Surface, current_time: float):
        """
        Draw cursor with state indicator.

        Args:
            surface: Surface to draw on
            current_time: Current time (unused now, kept for compatibility)
        """
        # Draw cursor - color depends on state
        if self.draw_mode == DrawMode.NONE:
            cursor_color = (100, 100, 255)  # Blue - waiting for first point
        elif self.draw_mode == DrawMode.WAITING:
            cursor_color = (255, 165, 0)    # Orange - waiting for second point
        else:
            cursor_color = (100, 100, 255)

        pygame.draw.circle(surface, cursor_color, (self.cursor_x, self.cursor_y), 10, 3)
        pygame.draw.circle(surface, (255, 255, 255), (self.cursor_x, self.cursor_y), 3, -1)

    def save_image(self, filename: str):
        """
        Save canvas to image file.

        Args:
            filename: Output filename
        """
        pygame.image.save(self.canvas, filename)
        print(f"Canvas saved to {filename}")

    def get_stroke_count(self) -> int:
        """Get number of strokes."""
        return len(self.strokes)

    def get_total_points(self) -> int:
        """Get total number of points across all strokes."""
        total = sum(len(stroke.points) for stroke in self.strokes)
        if self.current_stroke:
            total += len(self.current_stroke.points)
        return total


if __name__ == "__main__":
    # Test drawing canvas
    pygame.init()

    canvas = DrawingCanvas(800, 600)
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Drawing Canvas Test")
    clock = pygame.time.Clock()

    running = True
    while running:
        current_time = pygame.time.get_ticks() / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if canvas.draw_mode == DrawMode.NONE:
                        canvas.start_drawing()
                    else:
                        canvas.end_stroke()
                elif event.key == pygame.K_u:
                    canvas.undo()
                elif event.key == pygame.K_c:
                    canvas.clear()
                elif event.key == pygame.K_g:
                    canvas.toggle_grid()

        # Update cursor from mouse (for testing)
        mx, my = pygame.mouse.get_pos()
        canvas.update_cursor(mx, my)

        # Add point if drawing
        if canvas.draw_mode == DrawMode.DRAWING:
            canvas.add_point()

        # Render
        canvas_surface = canvas.render()
        screen.blit(canvas_surface, (0, 0))
        canvas.draw_cursor(screen, current_time)

        # Status
        font = pygame.font.Font(None, 24)
        status = f"Strokes: {canvas.get_stroke_count()} | Points: {canvas.get_total_points()}"
        text = font.render(status, True, (0, 0, 0))
        screen.blit(text, (10, 10))

        instructions = font.render("SPACE: start/stop | U: undo | C: clear | G: grid", True, (100, 100, 100))
        screen.blit(instructions, (10, 580))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
