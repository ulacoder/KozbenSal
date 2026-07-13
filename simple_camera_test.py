"""Simple camera test - just show video feed."""
import cv2

print("Opening camera 0...")
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("ERROR: Cannot open camera 0")
    exit(1)

print("Camera opened! Press 'q' to quit.")
print("Window should appear showing camera feed...")

frame_count = 0
while True:
    ret, frame = cap.read()

    if not ret:
        print(f"ERROR: Cannot read frame (frame #{frame_count})")
        break

    frame_count += 1

    # Add frame counter to see if it's updating
    cv2.putText(frame, f"Frame: {frame_count}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Camera Test - Press Q to quit', frame)

    if frame_count % 30 == 0:
        print(f"Frames captured: {frame_count}")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Quitting...")
        break

cap.release()
cv2.destroyAllWindows()
print(f"Total frames: {frame_count}")
