import json
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import numpy as np
import evaluate
from datasets import Dataset
import pandas as pd
from sklearn.model_selection import train_test_split
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    DataCollatorWithPadding,
)

from config import (
    BASE_MODEL,
    DATASET_CSV,
    MODEL_OUTPUT_DIR,
    NUM_TRAIN_EPOCHS,
    PER_DEVICE_TRAIN_BATCH_SIZE,
    PER_DEVICE_EVAL_BATCH_SIZE,
    LEARNING_RATE,
    WEIGHT_DECAY,
    WARMUP_RATIO,
    MAX_LENGTH,
    LOGGING_STEPS,
)

accuracy_metric = evaluate.load("accuracy")


def normalize(text: str) -> str:
    text = text.lower()
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return text


def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return accuracy_metric.compute(predictions=predictions, references=labels)


def main():
    csv_path = Path(__file__).parent / DATASET_CSV
    print(f"Cargando dataset desde {csv_path}...")
    df = pd.read_csv(csv_path)

    categories = sorted(df["category"].unique().tolist())
    num_labels = len(categories)
    label2id = {name: i for i, name in enumerate(categories)}
    id2label = {i: name for i, name in enumerate(categories)}
    print(f"Categorias ({num_labels}): {categories}")

    df["text"] = df["text"].apply(normalize)
    df["labels"] = df["category"].map(label2id)

    train_df, val_df = train_test_split(
        df, test_size=0.15, stratify=df["labels"], random_state=42
    )
    print(f"Train: {len(train_df)} | Val: {len(val_df)}")

    train_dataset = Dataset.from_pandas(train_df[["text", "labels"]].reset_index(drop=True))
    val_dataset = Dataset.from_pandas(val_df[["text", "labels"]].reset_index(drop=True))

    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)

    def tokenize(batch):
        return tokenizer(batch["text"], truncation=True, max_length=MAX_LENGTH)

    train_dataset = train_dataset.map(tokenize, batched=True, remove_columns=["text"])
    val_dataset = val_dataset.map(tokenize, batched=True, remove_columns=["text"])

    model = AutoModelForSequenceClassification.from_pretrained(
        BASE_MODEL,
        num_labels=num_labels,
        id2label=id2label,
        label2id=label2id,
    )

    output_dir = str(Path(__file__).parent / MODEL_OUTPUT_DIR)

    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=NUM_TRAIN_EPOCHS,
        per_device_train_batch_size=PER_DEVICE_TRAIN_BATCH_SIZE,
        per_device_eval_batch_size=PER_DEVICE_EVAL_BATCH_SIZE,
        learning_rate=LEARNING_RATE,
        weight_decay=WEIGHT_DECAY,
        warmup_ratio=WARMUP_RATIO,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="accuracy",
        logging_steps=LOGGING_STEPS,
        report_to="none",
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        tokenizer=tokenizer,
        data_collator=DataCollatorWithPadding(tokenizer),
        compute_metrics=compute_metrics,
    )

    print("Iniciando fine-tuning...")
    trainer.train()

    print(f"Guardando modelo en {output_dir}...")
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)

    label_map_path = Path(output_dir) / "label_map.json"
    with open(label_map_path, "w", encoding="utf-8") as f:
        json.dump(id2label, f, ensure_ascii=False, indent=2)

    print(f"Listo! Modelo guardado en {output_dir}")
    print(f"Mapa de etiquetas: {label_map_path}")


if __name__ == "__main__":
    main()
