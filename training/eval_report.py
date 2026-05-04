import json
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from transformers import pipeline

from config import DATASET_CSV, MODEL_OUTPUT_DIR, MAX_LENGTH

MODEL_DIR = Path(__file__).parent / MODEL_OUTPUT_DIR


def normalize(text: str) -> str:
    text = text.lower()
    text = unicodedata.normalize("NFD", text)
    return "".join(c for c in text if unicodedata.category(c) != "Mn")


def main():
    csv_path = Path(__file__).parent / DATASET_CSV
    df = pd.read_csv(csv_path)

    categories = sorted(df["category"].unique().tolist())
    label2id = {name: i for i, name in enumerate(categories)}

    df["text"] = df["text"].apply(normalize)
    df["label_id"] = df["category"].map(label2id)

    # Mismo split que en train.py: 85/15 estratificado con random_state=42
    _, val_df = train_test_split(
        df, test_size=0.15, stratify=df["label_id"], random_state=42
    )
    print(f"Evaluando sobre {len(val_df)} ejemplos de validacion...")

    classifier = pipeline(
        "text-classification",
        model=str(MODEL_DIR),
        tokenizer=str(MODEL_DIR),
        top_k=1,
        device=-1,
        truncation=True,
        max_length=MAX_LENGTH,
    )

    texts = val_df["text"].tolist()
    true_labels = val_df["category"].tolist()

    print("Corriendo inferencia...")
    results = classifier(texts, batch_size=32)
    pred_labels = [r[0]["label"] for r in results]

    print("\n" + "=" * 60)
    print("CLASSIFICATION REPORT")
    print("=" * 60)
    print(classification_report(true_labels, pred_labels, digits=3))

    print("CONFUSION MATRIX")
    print("=" * 60)
    cm = confusion_matrix(true_labels, pred_labels, labels=categories)
    header = f"{'':25s}" + "".join(f"{c[:6]:>8s}" for c in categories)
    print(header)
    for i, row_label in enumerate(categories):
        row = f"{row_label:25s}" + "".join(f"{v:>8d}" for v in cm[i])
        print(row)

    # Detectar categorías con F1 < 0.80 para alertar
    report = classification_report(
        true_labels, pred_labels, output_dict=True, zero_division=0
    )
    weak = [
        cat for cat in categories
        if report.get(cat, {}).get("f1-score", 1.0) < 0.80
    ]
    if weak:
        print(f"\nADVERTENCIA: F1 < 0.80 en: {weak}")
        print("Considera agregar mas ejemplos o diversificar templates para estas categorias.")
    else:
        print("\nTodas las categorias tienen F1 >= 0.80")


if __name__ == "__main__":
    main()
