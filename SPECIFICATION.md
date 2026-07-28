# Degg Text Join — SPECIFICATION

## 1. Назначение

Объединение нескольких текстов в один через разделитель. Аналог стандартной ноды "Объединить", но с динамическими входами — подключаешь сколько нужно, до 20.

## 2. Файлы

| Файл | Назначение |
|------|-----------|
| `deg_text_join_node.py` | Python-класс `DeggTextJoin` — separator + динамические STRING входы |
| `web/js/deg_text_join.js` | LiteGraph-расширение: динамические входы text_1..text_N |
| `__init__.py` | Экспорт маппингов, `WEB_DIRECTORY` |

## 3. Python: класс DeggTextJoin

### INPUT_TYPES

| Поле | Тип | По умолчанию | Описание |
|------|-----|-------------|----------|
| `separator` | `STRING` | `", "` | Разделитель между текстами |

### optional

| Поле | Тип | Описание |
|------|-----|----------|
| `text_1` … `text_20` | `STRING` (forceInput) | Тексты для объединения. Появляются динамически при подключении |

### OUTPUT

- `RETURN_TYPES = ("STRING",)` — объединённый текст
- `RETURN_NAMES = ("text",)`

### Логика join()

1. Итерирует `text_1`..`text_20` из kwargs
2. Собирает непycтые значения в список
3. Склеивает через `separator.join(texts)`

## 4. JS: расширение LiteGraph

### Импорт app

```javascript
const { app } = window.comfyAPI.app;
```

### Динамические входы

| Событие | Результат |
|---------|-----------|
| Нода создана | Только `text_1` |
| Провод к `text_N` | Появился `text_{N+1}` (если N < 20) |
| Отключён `text_N` | Все пустые входы с номером > N удалены |

### Функции

- `findLastConnected(node)` — находит последний подключённый text-вход
- `rebuildInputs(node)` — перестраивает входы

## 5. Рабочая копия

`D:\ComfyUI_windows_portable\ComfyUI\custom_nodes\Degg_TextJoin\`
