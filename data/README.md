# Данные

## Источники и лицензии

**Фото** — Roboflow `cats-xofvm/cat-emotions` (зеркало:
kaggle.com/datasets/trendcart/cat-emotions-dataset), лицензия **CC BY 4.0**.
671 реальное фото 640x640 в `cats_big/`, 7 исходных классов.
Атрибуция: `cats_big/ATTRIBUTION.md`.

**Тексты** — `Djacon/ru-izard-emotions` (HuggingFace), лицензия **MIT**,
плюс синтетические шаблоны из этого же проекта.

Сведения об источнике и лицензии хранятся здесь, а не отдельными колонками в CSV.

## Единая таксономия (6 классов)

| ID | Русский | Класс фото | Класс текста |
|---|---|---|---|
| `joy` | радость | Happy | joy, enthusiasm |
| `sadness` | грусть | Sad | sadness, guilt, shame |
| `tiredness` | усталость | Normal | neutral |
| `anger` | раздражение | Angry | anger, disgust |
| `surprise` | удивление | Surprised | surprise |
| `confusion` | растерянность | Scared | fear |

`Disgusted` (79 фото) остаётся в `cats_big/` для каталога, но в обучении не
участвует: мало примеров и метка неоднозначна.

## Файлы и схемы

```text
image_labels.csv       path,label,split                    # 592 фото: train 412 / val 90 / test 90
phrases.csv            text,label,group_id,split           # 14 064 фразы: train 10 829 / val 1 375 / test 1 860
image_predictions.csv  path,predicted_label,score          # каталог всех 671 фото
```

- `path` — путь относительно корня проекта (`data/cats_big/...`);
- `label` — истинная метка из датасета;
- `predicted_label`, `score` — предсказание ResNet18 и его уверенность,
  это **не** разметка;
- `group_id` — группа перефразировок: одна группа целиком попадает в один split,
  иначе получается утечка данных;
- `split` — `train`, `validation` или `test`. Test открывается один раз.

## Ограничения

- Эмоции котов субъективны: класс — условный визуальный признак, а не
  измеренное состояние животного.
- Согласованность разметчиков не измерялась; метки взяты из исходного датасета.
- Синтетические текстовые шаблоны упрощают лексику и могут завышать метрики
  на шаблонных фразах.
