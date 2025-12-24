# MoviePy Adapter для ComfyUI - Документация реализации

## Обзор

MoviePy Adapter (MPA) - это набор кастомных нод для ComfyUI, которые интегрируют функциональность библиотеки MoviePy для работы с видео.

## Архитектура проекта

```
src/ComfyUI_MovisAdapter/
├── common.py                              # Общие функции конвертации IMAGE ↔ MoviePy
├── nodes.py                               # Регистрация всех нод
├── node_types/
│   ├── __init__.py
│   ├── CombineVideos/
│   │   ├── __init__.py
│   │   └── combine_videos.py             # Объединение нескольких видео
│   ├── VideoTransition/
│   │   ├── __init__.py
│   │   └── video_transition.py           # Переходы между видео
│   ├── BrightnessEffect/
│   │   ├── __init__.py
│   │   └── brightness_effect.py          # Изменение яркости
│   ├── ContrastEffect/
│   │   ├── __init__.py
│   │   └── contrast_effect.py            # Изменение контраста
│   └── SpeedEffect/
│       ├── __init__.py
│       └── speed_effect.py               # Изменение скорости воспроизведения
```

## Реализованные ноды

### 1. MPA Combine Videos

**Назначение:** Объединение от 1 до 10 видео в одно последовательное видео.

**Входы:**
- `IMAGE1` (обязательный) - первое видео
- `IMAGE2-IMAGE10` (опциональные) - дополнительные видео
- `fps` - частота кадров для выходного видео (по умолчанию: 24.0)

**Выход:**
- `combined_video` - объединённое видео

**Особенности:**
- Все видео масштабируются до разрешения первого видео
- Видео объединяются последовательно (одно за другим)

---

### 2. MPA Video Transition

**Назначение:** Добавление переходов между двумя видеоклипами.

**Входы:**
- `IMAGE1` - первое видео
- `IMAGE2` - второе видео
- `transition_type` - тип перехода:
  - `crossfade` - плавное затухание первого и появление второго видео
  - `fadein` - только появление второго видео
  - `fadeout` - только затухание первого видео
  - `fadeinout` - затухание первого и появление второго (последовательно)
- `duration` - длительность перехода в секундах (по умолчанию: 1.0)
- `fps` - частота кадров (по умолчанию: 24.0)

**Выход:**
- `video_with_transition` - видео с переходом

---

### 3. MPA Brightness Effect

**Назначение:** Изменение яркости видео.

**Входы:**
- `IMAGE` - входное видео
- `factor` - множитель яркости (по умолчанию: 1.0)
  - `1.0` = без изменений
  - `> 1.0` = увеличение яркости
  - `< 1.0` = уменьшение яркости
- `fps` - частота кадров (по умолчанию: 24.0)

**Выход:**
- `adjusted_video` - видео с изменённой яркостью

---

### 4. MPA Contrast Effect

**Назначение:** Изменение контраста видео.

**Входы:**
- `IMAGE` - входное видео
- `factor` - множитель контраста (по умолчанию: 1.0)
  - `1.0` = без изменений
  - `> 1.0` = увеличение контраста
  - `< 1.0` = уменьшение контраста
- `fps` - частота кадров (по умолчанию: 24.0)

**Выход:**
- `adjusted_video` - видео с изменённым контрастом

---

### 5. MPA Speed Effect

**Назначение:** Изменение скорости воспроизведения видео.

**Входы:**
- `IMAGE` - входное видео
- `factor` - множитель скорости (по умолчанию: 1.0)
  - `1.0` = нормальная скорость
  - `> 1.0` = ускорение (например, 2.0 = в 2 раза быстрее)
  - `< 1.0` = замедление (например, 0.5 = в 2 раза медленнее)
- `fps` - частота кадров входного видео (по умолчанию: 24.0)

**Выход:**
- `adjusted_video` - видео с изменённой скоростью

---

## Технические детали

### Формат данных

- **Входной формат:** ComfyUI `IMAGE` тензор с формой `[B, H, W, C]`, где:
  - `B` = количество кадров
  - `H` = высота
  - `W` = ширина
  - `C` = количество каналов (обычно 3 для RGB)
- **Диапазон значений:** `[0.0, 1.0]` для ComfyUI
- **Конвертация:** значения автоматически конвертируются в `[0, 255]` для MoviePy и обратно

### Зависимости

Проект требует следующие зависимости (указаны в `pyproject.toml`):
- `moviepy >= 1.0.3`
- `numpy >= 1.20.0`
- `torch >= 1.13.0`

### Установка

1. Склонируйте репозиторий в папку custom_nodes ComfyUI
2. Установите зависимости:

```bash
pip install -e .
```

или

```bash
pip install moviepy numpy torch
```

3. Перезапустите ComfyUI

## Использование в ComfyUI

После установки все ноды будут доступны в меню ComfyUI в категории **MPA/video**:

- MPA Combine Videos
- MPA Video Transition
- MPA Brightness Effect
- MPA Contrast Effect
- MPA Speed Effect

## Примеры использования

### Объединение трёх видео с переходами

1. Загрузите 3 видео как IMAGE
2. Добавьте ноду **MPA Video Transition** между первым и вторым видео
3. Добавьте ноду **MPA Video Transition** между вторым и третьим видео
4. Используйте **MPA Combine Videos** для объединения результатов

### Создание slow-motion эффекта с повышенной яркостью

1. Загрузите видео как IMAGE
2. Добавьте ноду **MPA Speed Effect** с factor=0.5 (замедление в 2 раза)
3. Добавьте ноду **MPA Brightness Effect** с factor=1.2 (увеличение яркости на 20%)
4. Соедините ноды последовательно

## Общие функции (common.py)

Модуль `common.py` содержит утилиты для конвертации между форматами:

- `image_tensor_to_moviepy_clip(tensor, fps)` - конвертирует ComfyUI IMAGE в MoviePy VideoClip
- `moviepy_clip_to_image_tensor(clip)` - конвертирует MoviePy VideoClip в ComfyUI IMAGE
- `resize_clip_to_resolution(clip, width, height)` - изменяет разрешение клипа

## Расширения в будущем

Планируется добавить:
- Дополнительные эффекты: blur, rotate, scale
- Поддержка аудио
- Оптимизация производительности для больших видео
- Кэширование промежуточных результатов

## Структура регистрации нод

Все ноды регистрируются в `nodes.py`:

```python
NODE_CLASS_MAPPINGS = {
    "MPA Combine Videos": MPACombineVideos,
    "MPA Video Transition": MPAVideoTransition,
    "MPA Brightness Effect": MPABrightnessEffect,
    "MPA Contrast Effect": MPAContrastEffect,
    "MPA Speed Effect": MPASpeedEffect,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MPA Combine Videos": "MPA Combine Videos",
    "MPA Video Transition": "MPA Video Transition",
    "MPA Brightness Effect": "MPA Brightness Effect",
    "MPA Contrast Effect": "MPA Contrast Effect",
    "MPA Speed Effect": "MPA Speed Effect",
}
```

## Категоризация

Все ноды находятся в категории `MPA/video` для удобной навигации в интерфейсе ComfyUI.

## Префикс

Все ноды используют префикс `MPA ` (MoviePy Adapter) для идентификации и предотвращения конфликтов имён с другими пакетами нод.

---

**Версия:** 0.0.1  
**Автор:** nschpy  
**Лицензия:** GNU General Public License v3

