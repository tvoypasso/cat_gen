"""Загрузка обученного текстового классификатора и предсказание эмоции."""

import json
from dataclasses import dataclass

import joblib

from config import TEXT_MODEL_PATH
from src.constants import LABELS


@dataclass
class TextPrediction:
    label: str
    probabilities: dict[str, float]
    confident: bool


class TextModel:
    def __init__(self):
        self.model = joblib.load(TEXT_MODEL_PATH)
        meta_path = TEXT_MODEL_PATH.parent / "metadata.json"
        self.threshold = json.loads(meta_path.read_text(encoding="utf-8"))[
            "confidence_threshold"
        ]

    def predict(self, text: str) -> TextPrediction:
        values = self.model.predict_proba([text])[0]
        # Порядок model.classes_ не обязан совпадать с LABELS,
        # поэтому собираем словарь по именам классов.
        probabilities = dict(zip(self.model.classes_, map(float, values)))
        label = max(LABELS, key=probabilities.__getitem__)
        score = probabilities[label]
        return TextPrediction(label, probabilities, confident=score >= self.threshold)
