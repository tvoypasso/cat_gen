"""Выбор фото кота из готовой таблицы image_predictions.csv."""

import csv
import random

from config import PREDICTIONS_CSV, ROOT, TOP_K


class CatSelector:
    def __init__(self):
        self.rows = []  # сюда сложим все фото из таблицы

        # Читаем таблицу один раз при запуске.
        with PREDICTIONS_CSV.open(encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                self.rows.append(
                    {
                        "path": ROOT / row["path"],        # полный путь к файлу
                        "label": row["predicted_label"],   # эмоция фото
                        "score": float(row["score"]),      # уверенность модели
                    }
                )

        self.random = random.Random(42)  # чтобы выбор был случайным, но повторяемым
        self.last_path = None            # фото, показанное в прошлый раз

    def pick(self, label):
        # 1. Берём только фото нужной эмоции.
        matching = [r for r in self.rows if r["label"] == label]

        # 2. Если таких нет — берём радость, чтобы не было пустого результата.
        if not matching:
            matching = [r for r in self.rows if r["label"] == "joy"]

        # 3. Сортируем: самые уверенные фото идут первыми.
        matching.sort(key=lambda r: r["score"], reverse=True)

        # 4. Оставляем лучшие 25 штук.
        best = matching[:TOP_K]

        # 5. Убираем то фото, что показывали в прошлый раз (если есть из чего выбрать).
        if len(best) > 1:
            best = [r for r in best if r["path"] != self.last_path]

        # 6. Берём случайное из оставшихся и запоминаем его.
        photo = self.random.choice(best)
        self.last_path = photo["path"]
        return photo
