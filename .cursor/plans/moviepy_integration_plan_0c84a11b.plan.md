---
name: MoviePy Integration Plan
overview: "Создание набора кастомных нод ComfyUI для работы с видео на базе MoviePy: загрузка, склейка с переходами, эффекты, цветокоррекция, преобразование в кадры и сохранение."
todos:
  - id: video_types
    content: Создать модуль video_types.py с реализацией кастомного типа данных VIDEO (обертка над VideoClip)
    status: completed
  - id: load_save_nodes
    content: Реализовать ноды LoadVideo и SaveVideo в nodes.py для базовых операций загрузки и сохранения
    status: completed
  - id: transitions_module
    content: Создать модуль transitions.py с реализацией всех типов переходов (crossfade, fade, slide, zoom)
    status: completed
  - id: concatenate_node
    content: Реализовать ноду VideoConcatenate с поддержкой простой склейки и переходов
    status: completed
  - id: effects_module
    content: Создать модуль effects.py с реализацией всех видеоэффектов (blur, sharpen, mirror, speed, noise, vignette)
    status: completed
  - id: effects_node
    content: Реализовать ноду VideoEffects для применения эффектов к видео
    status: completed
  - id: color_grading_module
    content: Создать модуль color_grading.py с реализацией цветокоррекции (brightness, contrast, saturation, gamma, hue_shift)
    status: completed
  - id: color_grading_node
    content: Реализовать ноду ColorGrading для применения цветокоррекции
    status: completed
  - id: video_to_images
    content: Реализовать ноду VideoToImages для преобразования видео в последовательность кадров (IMAGE)
    status: completed
  - id: register_nodes
    content: Зарегистрировать все ноды в NODE_CLASS_MAPPINGS и NODE_DISPLAY_NAME_MAPPINGS в __init__.py
    status: completed
---

# План адаптации MoviePy для ComfyUI

## Архитектура решения

### Типы данных

- **STRING** - для входных путей к видеофайлам
- **VIDEO** - кастомный тип данных (обертка над `VideoClip` из MoviePy) для передачи между нодами
- **IMAGE** - стандартный тип ComfyUI для кадров видео

### Структура модулей

```javascript
src/ComfyUI_MovisAdapter/
├── __init__.py          # Экспорт нод
├── nodes.py             # Основные ноды
├── video_types.py       # Кастомный тип VIDEO и утилиты
├── transitions.py       # Реализация переходов между клипами
├── effects.py           # Реализация видеоэффектов
└── color_grading.py    # Реализация цветокоррекции
```



## Реализуемые ноды

### 1. LoadVideo

**Файл:** `nodes.py`Загружает видео из файла и возвращает объект типа VIDEO.**INPUT_TYPES:**

- `video_path` (STRING) - путь к видеофайлу
- `audio` (BOOLEAN) - загружать ли аудио (default: True)

**RETURN_TYPES:** `("VIDEO",)`**Функциональность:**

- Использует `VideoFileClip` из MoviePy
- Валидация существования файла
- Обработка ошибок загрузки

---

### 2. VideoConcatenate

**Файл:** `nodes.py`Склеивает несколько видеоклипов с поддержкой переходов.**INPUT_TYPES:**

- `videos` (VIDEO, список) - список видеоклипов для склейки
- `mode` (COMBO) - режим склейки: `["simple", "transition"]`
- `transition_type` (COMBO) - тип перехода: `["none", "crossfade", "fade_black", "fade_white", "slide_left", "slide_right", "zoom_in", "zoom_out"]`
- `transition_duration` (FLOAT) - длительность перехода в секундах (default: 1.0, min: 0.1, max: 10.0)

**RETURN_TYPES:** `("VIDEO",)`**Функциональность:**

- Режим `simple`: использует `concatenate_videoclips`
- Режим `transition`: применяет выбранный переход между клипами
- Нормализация FPS и разрешения перед склейкой
- Обработка случаев с разными параметрами видео

**Модуль:** `transitions.py` - реализация переходов через MoviePy (`crossfadein`, `fadein`, `fadeout`, `CompositeVideoClip`)---

### 3. VideoEffects

**Файл:** `nodes.py`Применяет эффекты к видео.**INPUT_TYPES:**

- `video` (VIDEO) - входное видео
- `effect_type` (COMBO) - тип эффекта: `["none", "blur", "sharpen", "mirror_x", "mirror_y", "speed_up", "slow_down", "noise", "vignette"]`
- `intensity` (FLOAT) - интенсивность эффекта (default: 1.0, min: 0.0, max: 10.0)
- `blur_radius` (INT, optional) - радиус размытия для blur (default: 2, min: 1, max: 20)
- `speed_factor` (FLOAT, optional) - коэффициент скорости для speed_up/slow_down (default: 1.5, min: 0.1, max: 10.0)
- `noise_level` (FLOAT, optional) - уровень шума для noise (default: 0.1, min: 0.0, max: 1.0)

**RETURN_TYPES:** `("VIDEO",)`**Функциональность:**

- Применение эффектов через MoviePy (`vfx`, `fl_image`, `resize`)
- Условное отображение параметров в зависимости от типа эффекта
- Реализация эффектов в модуле `effects.py`

---

### 4. ColorGrading

**Файл:** `nodes.py`Применяет цветокоррекцию к видео.**INPUT_TYPES:**

- `video` (VIDEO) - входное видео
- `brightness` (FLOAT) - яркость (default: 0.0, min: -1.0, max: 1.0, step: 0.01)
- `contrast` (FLOAT) - контраст (default: 0.0, min: -1.0, max: 1.0, step: 0.01)
- `saturation` (FLOAT) - насыщенность (default: 0.0, min: -1.0, max: 1.0, step: 0.01)
- `gamma` (FLOAT) - гамма-коррекция (default: 1.0, min: 0.1, max: 3.0, step: 0.01)
- `hue_shift` (FLOAT) - цветовой сдвиг в градусах (default: 0.0, min: -180.0, max: 180.0, step: 1.0)

**RETURN_TYPES:** `("VIDEO",)`**Функциональность:**

- Применение всех параметров за один проход через `fl_image`
- Использование numpy для цветовых преобразований
- Реализация в модуле `color_grading.py`

---

### 5. VideoToImages

**Файл:** `nodes.py`Преобразует видео в последовательность кадров (images).**INPUT_TYPES:**

- `video` (VIDEO) - входное видео
- `fps` (FLOAT, optional) - частота кадров для извлечения (default: None - использовать FPS видео)
- `start_time` (FLOAT, optional) - время начала в секундах (default: 0.0)
- `end_time` (FLOAT, optional) - время окончания в секундах (default: None - до конца)

**RETURN_TYPES:** `("IMAGE",)` (список кадров)**Функциональность:**

- Извлечение кадров через `iter_frames()` или `get_frame()`
- Преобразование в формат ComfyUI IMAGE (torch.Tensor [B, H, W, C])
- Поддержка выборочного извлечения по времени

---

### 6. SaveVideo

**Файл:** `nodes.py`Сохраняет видео в файл.**INPUT_TYPES:**

- `video` (VIDEO) - видео для сохранения
- `filename` (STRING) - имя файла (default: "output.mp4")
- `codec` (COMBO) - кодек: `["libx264", "libx265", "mpeg4"]` (default: "libx264")
- `bitrate` (STRING) - битрейт (default: "8000k")
- `audio_codec` (COMBO) - аудио кодек: `["aac", "mp3", "libvorbis"]` (default: "aac")
- `preset` (COMBO) - пресет кодирования: `["ultrafast", "fast", "medium", "slow"]` (default: "medium")

**RETURN_TYPES:** `("STRING",)` - путь к сохраненному файлу**OUTPUT_NODE:** `True`**Функциональность:**

- Использование `write_videofile()` из MoviePy
- Валидация пути и создание директорий при необходимости
- Обработка ошибок кодирования

---

## Вспомогательные модули

### video_types.py

Реализация кастомного типа данных VIDEO:

- Класс-обертка над `VideoClip`
- Методы для сериализации/десериализации (если потребуется)
- Утилиты для нормализации параметров видео

### transitions.py

Реализация переходов:

- Функции для каждого типа перехода
- Использование `CompositeVideoClip`, `crossfadein`, `fadein`, `fadeout`
- Обработка временных интервалов

### effects.py

Реализация эффектов:

- Функции для каждого типа эффекта
- Использование `vfx`, `fl_image`, numpy для обработки кадров
- Оптимизация производительности

### color_grading.py

Реализация цветокоррекции:

- Функции преобразования цветов через numpy
- Применение brightness, contrast, saturation, gamma, hue_shift
- Комбинирование всех параметров в одной функции

---

## Технические детали

### Обработка ошибок

- Валидация входных параметров через `VALIDATE_INPUTS`
- Проверка существования файлов
- Обработка несовпадения FPS/разрешения при склейке
- Graceful degradation при ошибках MoviePy

### Производительность

- Ленивая загрузка видео (MoviePy по умолчанию)
- Кэширование промежуточных результатов где возможно
- Оптимизация операций с кадрами

### Зависимости

- `moviepy` - основная библиотека
- `numpy` - для цветокоррекции и эффектов
- Стандартные библиотеки Python

---

## Порядок реализации

1. **video_types.py** - базовая инфраструктура типа VIDEO
2. **nodes.py** - LoadVideo и SaveVideo (базовые операции)
3. **transitions.py** + VideoConcatenate нода
4. **effects.py** + VideoEffects нода
5. **color_grading.py** + ColorGrading нода
6. **VideoToImages** нода
7. Тестирование и оптимизация

---

## Категории нод в ComfyUI

Все ноды будут в категории `"video/moviepy"`:

- `video/moviepy/load` - LoadVideo