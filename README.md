# KozbenSal - Eye Tracking Drawing Application

**Smart assistive glasses with eye-tracking for hands-free computer control**

This project enables people with limited motor functions to draw, type, and control computers using only their eye movements.

[Русская версия ниже](#kozbensal---приложение-для-рисования-с-отслеживанием-глаз)

---

## 🏆 Achievements

- 🥈 **2nd place WRO 2026 Regional**
- Assistive technology for people with motor disabilities
- Affordable alternative to expensive commercial solutions ($50 vs $15,000+)

## ✨ Features

- **Eye Tracking** - Real-time eye movement tracking with hybrid detection
- **Blink-Based Interaction** - Draw by blinking instead of holding gaze
- **Point-to-Point Drawing** - Place points with blinks, automatically connect with lines
- **Calibration** - Accurate 9-point calibration for precise screen mapping
- **Visual Feedback** - Real-time cursor, preview lines, and status indicators
- **Intuitive Interface** - Works out of the box, no complex setup

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/ulacoder/KozbenSal.git
cd KozbenSal

# Install dependencies
pip install -r requirements.txt
```

### Camera Setup

**IMPORTANT:** By default, the system uses camera index 1 (external PS3 Eye camera).

- Index 0 = Built-in laptop camera
- Index 1 = External USB camera (PS3 Eye)

To change camera, edit `eye_tracker.py`, line 19:
```python
def __init__(self, camera_id: int = 1):  # change 1 to desired index
```

Test your cameras:
```bash
python test_cameras.py
```

### Launch

```bash
python main.py
```

## 🎮 Controls

### General Commands
- `TAB` - Switch between calibration and drawing modes
- `R` - Reset calibration
- `P` - Pause/unpause
- `E` - Show/hide camera preview
- `ESC` - Exit

### Drawing Mode
- `BLINK` - Place points and draw lines
- `U` - Undo last line
- `C` - Clear canvas
- `G` - Toggle grid
- `S` - Save drawing

### How to Draw

**The System:**

1. **Calibration** (on first launch):
   - System shows 9 calibration points on screen
   - Look at each point
   - Calibration completes automatically
   - You'll see "Calibration Complete!"

2. **Switch to Drawing Mode**:
   - Press `TAB` to enter Drawing Mode
   - White canvas replaces camera view

3. **Draw Lines**:
   - **Blink once** → places first point (green marker appears)
   - **Move your gaze** → see gray preview line following cursor
   - **Blink again** → line is drawn between the two points

4. **Cursor Colors**:
   - Blue cursor = waiting for first point
   - Orange cursor = waiting for second point
   - Green dot = first point placed

5. **Useful Functions**:
   - `U` - undo last line if you make a mistake
   - `C` - clear entire canvas
   - `S` - save drawing (saves as `drawing_YYYYMMDD_HHMMSS.png`)
   - `G` - show grid for precise drawing

**Tips:**
- Sit 40-60 cm from camera
- Good lighting = better tracking
- If calibration is inaccurate, press `R` to recalibrate
- Camera preview (top-right) shows if eyes are tracked (green dots)
- Purple rings in preview = CV pupil detection active

## 🏗️ Architecture

```
kozbensal-python/
├── eye_tracker.py          # Hybrid eye tracking (MediaPipe + CV)
├── calibration_manager.py  # 9-point calibration & mapping
├── drawing_canvas.py       # Point-to-point canvas system
├── main.py                 # Main application
├── test_cameras.py         # Camera testing utility
└── requirements.txt        # Dependencies
```

### Components

#### `EyeTracker`
- Uses **MediaPipe Face Mesh** for eye landmark detection
- **Hybrid pupil detection**: CV contour analysis + MediaPipe iris
- **Blink detection** via Eye Aspect Ratio (EAR) calculation
- Gaze smoothing with exponential moving average

#### `CalibrationManager`
- 9-point calibration for accurate mapping
- Homography transform for perspective correction
- Automatic transition to drawing after calibration

#### `DrawingCanvas`
- Blink-based point placement
- Point-to-point line drawing
- Preview line rendering
- Undo, clear, save functionality

## 🔧 Technologies

- **Python 3.8+**
- **OpenCV** - Video processing, pupil detection
- **MediaPipe** - Face and eye landmark detection
- **Pygame** - GUI and rendering
- **NumPy/SciPy** - Mathematical transformations

## 📝 Project History

Original **EyeWriter** project was built in C++ with OpenFrameworks. This version is a complete port to Python with modern computer vision libraries.

### What Changed from Original:
- ✅ C++/OpenFrameworks → Python/MediaPipe
- ✅ Manual pupil/glint detection → Hybrid MediaPipe + CV
- ✅ Complex setup → Works out of the box
- ✅ Required IR camera → Works with regular webcam
- ✅ Dwell-time interaction → Blink-based point placement

## 🎯 Applications

- **Assistive Technology** - For people with cerebral palsy, ALS, spinal cord injuries
- **Education** - Teaching computer interaction
- **Art** - Creating digital art hands-free
- **Communication** - Text input, app control

## 📊 Performance

- **FPS**: 30 (configurable)
- **Latency**: ~50ms from eye movement to cursor / ~55ms with CV pupil detection
- **Accuracy**: Depends on calibration, typically ±20-30px
- **Blink Detection**: EAR < 0.21 for 2 consecutive frames

## 🤝 Contributing

This project is open source. Pull requests welcome!

### TODO
- [ ] Keyboard mode for text input (virtual keyboard)
- [ ] Improved calibration (more points, automatic)
- [ ] Multiple drawing modes (shapes, fill)
- [ ] Export formats (SVG, PDF)
- [ ] Raspberry Pi version for standalone operation
- [ ] Per-user blink sensitivity calibration

## 📄 License

Open Source - Use freely to help people.

## 👤 Author

Created for **nFactorial Incubator 2026**

**Contact**: ulagatnurtas10@gmail.com

**Repository**: https://github.com/ulacoder/KozbenSal

---

> "Technology should be accessible to everyone, regardless of physical abilities."

---
---

# KozbenSal - Приложение для рисования с отслеживанием глаз

**Умные очки с eye-tracking для управления компьютером без рук**

Проект позволяет людям с ограниченными двигательными функциями рисовать, печатать и управлять компьютером с помощью движений глаз.

## 🏆 Достижения

- 🥈 **2-е место WRO 2026 Regional**
- Assistive technology для людей с моторными нарушениями
- Доступная альтернатива дорогим коммерческим решениям ($50 vs $15,000+)

## ✨ Возможности

- **Eye Tracking** - Отслеживание движений глаз в реальном времени с гибридной детекцией
- **Управление морганием** - Рисуй морганием вместо задержки взгляда
- **Рисование точка-в-точку** - Ставь точки морганием, линии соединяются автоматически
- **Калибровка** - Точное сопоставление координат глаз с экраном (9-точечная калибровка)
- **Визуальная обратная связь** - Курсор, линии предпросмотра, индикаторы состояния
- **Интуитивный интерфейс** - Работает из коробки, без сложных настроек

## 🚀 Быстрый старт

### Установка

```bash
# Клонировать репозиторий
git clone https://github.com/ulacoder/KozbenSal.git
cd KozbenSal

# Установить зависимости
pip install -r requirements.txt
```

### Настройка камеры

**ВАЖНО**: По умолчанию используется камера с индексом 1 (внешняя PS3 Eye камера).

- Индекс 0 = встроенная камера ноутбука
- Индекс 1 = внешняя USB камера (PS3 Eye)

Если нужно изменить камеру, отредактируй `eye_tracker.py`, строка 19:
```python
def __init__(self, camera_id: int = 1):  # измени 1 на нужный индекс
```

Протестировать камеры:
```bash
python test_cameras.py
```

### Запуск

```bash
python main.py
```

## 🎮 Управление

### Общие команды
- `TAB` - переключение между калибровкой и рисованием
- `R` - сброс калибровки
- `P` - пауза/продолжить
- `E` - показать/скрыть превью камеры
- `ESC` - выход

### Режим рисования
- `МОРГАНИЕ` - Ставить точки и рисовать линии
- `U` - отменить последнюю линию
- `C` - очистить холст
- `G` - показать/скрыть сетку
- `S` - сохранить рисунок

### Как рисовать

**Система работы:**

1. **Калибровка** (при первом запуске):
   - Программа покажет 9 точек на экране
   - Смотри на каждую точку
   - Калибровка пройдет автоматически
   - Увидишь сообщение "Calibration Complete!"

2. **Переход в режим рисования**:
   - Нажми `TAB` чтобы переключиться в Drawing Mode
   - Белый холст заменит видео с камеры

3. **Рисование линий**:
   - **Моргни один раз** → ставится первая точка (зелёный маркер)
   - **Двигай взглядом** → видишь серую линию предпросмотра
   - **Моргни снова** → линия рисуется между точками

4. **Цвета курсора**:
   - Синий курсор = жду первую точку
   - Оранжевый курсор = жду вторую точку
   - Зелёная точка = первая точка установлена

5. **Полезные функции**:
   - `U` - отменить последнюю линию если ошибся
   - `C` - очистить весь холст
   - `S` - сохранить рисунок (сохранится как `drawing_YYYYMMDD_HHMMSS.png`)
   - `G` - показать сетку для точного рисования

**Советы:**
- Сиди на расстоянии 40-60 см от камеры
- Хорошее освещение = лучшее отслеживание
- Если калибровка неточная, нажми `R` чтобы откалибровать заново
- В правом верхнем углу есть превью камеры - убедись что глаза отслеживаются (зеленые точки)
- Фиолетовые кольца в превью = активна CV детекция зрачка

## 🏗️ Архитектура

```
kozbensal-python/
├── eye_tracker.py          # Гибридный eye tracking (MediaPipe + CV)
├── calibration_manager.py  # 9-точечная калибровка
├── drawing_canvas.py       # Система холста точка-в-точку
├── main.py                 # Главное приложение
├── test_cameras.py         # Утилита тестирования камер
└── requirements.txt        # Зависимости
```

### Компоненты

#### `EyeTracker`
- Использует **MediaPipe Face Mesh** для детекции глаз
- **Гибридная детекция зрачка**: CV контурный анализ + MediaPipe iris
- **Детекция моргания** через расчёт Eye Aspect Ratio (EAR)
- Сглаживание взгляда экспоненциальным скользящим средним

#### `CalibrationManager`
- 9-точечная калибровка для точного маппинга
- Homography transform для perspective correction
- Автоматический переход к рисованию после калибровки

#### `DrawingCanvas`
- Установка точек морганием
- Рисование линий точка-в-точку
- Рендеринг линий предпросмотра
- Отмена, очистка, сохранение

## 🔧 Технологии

- **Python 3.8+**
- **OpenCV** - Обработка видео, детекция зрачка
- **MediaPipe** - Детекция лица и глаз
- **Pygame** - GUI и рендеринг
- **NumPy/SciPy** - Математические трансформации

## 📝 История проекта

Оригинальный проект **EyeWriter** был создан на C++ с использованием OpenFrameworks. Данная версия - полный порт на Python с современными computer vision библиотеками.

### Что изменилось от оригинала:
- ✅ C++/OpenFrameworks → Python/MediaPipe
- ✅ Ручная детекция pupil/glint → Гибридный MediaPipe + CV
- ✅ Сложная настройка → Работает из коробки
- ✅ Требует IR камеру → Работает с обычной веб-камерой
- ✅ Взаимодействие через задержку → Управление морганием

## 🎯 Применение

- **Assistive Technology** - для людей с ДЦП, ALS, травмами спинного мозга
- **Образование** - обучение работе с компьютером
- **Творчество** - создание цифрового искусства без рук
- **Коммуникация** - печать текста, управление приложениями

## 📊 Производительность

- **FPS**: 30 (настраивается)
- **Latency**: ~50ms от движения глаз до курсора / ~55ms с CV детекцией
- **Точность**: зависит от калибровки, обычно ±20-30px
- **Детекция моргания**: EAR < 0.21 на 2 последовательных кадрах

## 🤝 Вклад в проект

Проект open source. Pull requests приветствуются!

### TODO
- [ ] Режим печати текста (виртуальная клавиатура)
- [ ] Улучшенная калибровка (больше точек, автоматическая)
- [ ] Разные режимы рисования (фигуры, заливка)
- [ ] Экспорт в разные форматы (SVG, PDF)
- [ ] Raspberry Pi версия для автономной работы
- [ ] Персональная калибровка чувствительности моргания

## 📄 Лицензия

Open Source - используйте свободно для помощи людям.

## 👤 Автор

Создано для **nFactorial Incubator 2026**

**Contact**: ulagatnurtas10@gmail.com

**Repository**: https://github.com/ulacoder/KozbenSal

---

> "Технологии должны быть доступны всем, независимо от физических возможностей."
