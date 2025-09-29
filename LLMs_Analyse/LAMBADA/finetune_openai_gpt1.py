import os
from openai import OpenAI


TRAIN_FILE_PATH = "habits_train1.jsonl"
VALID_FILE_PATH = "habits_valid1.jsonl"
MODEL_NAME = "gpt-4.1-mini-2025-04-14"
N_EPOCHS = 8
BATCH_SIZE = 4
LR_MULTIPLIER = 0.05
SUFFIX = "habit-66-v3"


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

try:
    
    with open(TRAIN_FILE_PATH, "rb") as f:
        train_file = client.files.create(file=f, purpose="fine-tune")
    print(f"Training file uploaded: {train_file.id}")

    
    with open(VALID_FILE_PATH, "rb") as f:
        valid_file = client.files.create(file=f, purpose="fine-tune")
    print(f"Verify that the file has been uploaded: {valid_file.id}")

    
    job = client.fine_tuning.jobs.create(
        model=MODEL_NAME,
        training_file=train_file.id,
        validation_file=valid_file.id,
        hyperparameters={
            "n_epochs": N_EPOCHS,
            "batch_size": BATCH_SIZE,
            "learning_rate_multiplier": LR_MULTIPLIER
        },
        suffix=SUFFIX,
        seed=42,
        metadata={
            "project": "habit-gen",
            "source": "66_sentences",
            "version": "v3"
        }
    )

    print("Fine-tuning task started")
    print("Job ID:", job.id)

except Exception as e:
    print("An error occurred:", e)
