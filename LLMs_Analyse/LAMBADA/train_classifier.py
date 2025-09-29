import pandas as pd
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
)
import torch
import numpy as np
from sklearn.metrics import accuracy_score, f1_score
import os

os.environ["WANDB_DISABLED"] = "true"


df = pd.read_csv("habits.csv")
dataset = Dataset.from_pandas(df)


model_name = "bert-base-german-cased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(
    model_name, num_labels=df["label"].nunique()
)


def preprocess(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True)


tokenized_dataset = dataset.map(preprocess, batched=True)


training_args = TrainingArguments(
    output_dir="./output/bert_german_cls",
    num_train_epochs=8,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=8,
    warmup_steps=50,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=10,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    metric_for_best_model="accuracy",
)


def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=-1)
    return {
        "accuracy": accuracy_score(labels, preds),
        "f1": f1_score(labels, preds, average="macro"),
    }


split_dataset = tokenized_dataset.train_test_split(test_size=0.2)
train_dataset = split_dataset["train"]
eval_dataset = split_dataset["test"]


trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
)


trainer.train()


trainer.save_model("./output/bert_german_cls/final_model")
