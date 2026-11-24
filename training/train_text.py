"""Обучение текстового классификатора: TF-IDF + логистическая регрессия.

Запуск из корня проекта:
    python -m training.train_text
"""

import csv
import json

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.pipeline import make_pipeline, make_union

from config import DATA_DIR, TEXT_MODEL_PATH
from src.constants import LABELS

DATA = DATA_DIR / "phrases.csv"
OUT = TEXT_MODEL_PATH.parent
CONFIDENCE_THRESHOLD = 0.4


def read_split(split):
    with DATA.open(encoding="utf-8-sig", newline="") as f:
        rows = [r for r in csv.DictReader(f) if r["split"] == split]
    return [r["text"].strip() for r in rows], [r["label"] for r in rows]


def build_model():
    features = make_union(
        TfidfVectorizer(analyzer="word", ngram_range=(1, 2), sublinear_tf=True),
        TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 5), sublinear_tf=True, min_df=2),
    )
    return make_pipeline(
        features,
        LogisticRegression(C=1.0, class_weight="balanced", max_iter=2000),
    )


def main():
    x_train, y_train = read_split("train")
    x_val, y_val = read_split("validation")
    x_test, y_test = read_split("test")
    print(f"train={len(x_train)} validation={len(x_val)} test={len(x_test)}")

    model = build_model()
    model.fit(x_train, y_train)

    val_pred = model.predict(x_val)
    print("validation macro F1:", round(f1_score(y_val, val_pred, average="macro"), 4))

    # Test смотрим один раз, после всех решений.
    test_pred = model.predict(x_test)
    print("test accuracy:", round(accuracy_score(y_test, test_pred), 4))
    print("test macro F1:", round(f1_score(y_test, test_pred, average="macro"), 4))

    OUT.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, TEXT_MODEL_PATH)
    (OUT / "metadata.json").write_text(
        json.dumps(
            {"labels": list(LABELS), "confidence_threshold": CONFIDENCE_THRESHOLD},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print("saved:", TEXT_MODEL_PATH)


if __name__ == "__main__":
    main()
