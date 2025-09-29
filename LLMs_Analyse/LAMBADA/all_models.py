from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

jobs = client.fine_tuning.jobs.list(limit=20)

for job in jobs.data:
    print(f"ID: {job.id}")
    print(f"Fine-tuned model: {job.fine_tuned_model}")
    print(f"Base model: {job.model}")
    print(f"Status: {job.status}")
    print(f"Created at: {job.created_at}")
    print("-" * 40)
