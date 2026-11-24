"""Пути и настройки проекта.

Все пути строятся от расположения этого файла (__file__), а не от текущей
папки. Так скрипты и приложение работают независимо от того, откуда запущены.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"

TEXT_MODEL_PATH = ROOT / "models" / "text_classifier" / "model.joblib"
IMAGE_MODEL_PATH = ROOT / "models" / "cat_classifier" / "model.pt"
PREDICTIONS_CSV = DATA_DIR / "image_predictions.csv"
IMAGES_DIR = DATA_DIR / "cats_big"
FONT_PATH = ROOT / "assets" / "fonts" / "NotoSans-Bold.ttf"

MAX_TEXT_LENGTH = 280
TOP_K = 25
