import os
import openai


openai.api_key = os.getenv("OPENAI_API_KEY")

file_path = "habits_gpt_finetune.jsonl"


print(" Uploading file...")
upload = openai.File.create(file=open(file_path, "rb"), purpose="fine-tune")
file_id = upload["id"]
print(f" Uploaded file_id: {file_id}")


print(" Starting fine-tuning job...")
job = openai.FineTuningJob.create(training_file=file_id, model="gpt-3.5-turbo")


print(f" Fine-tuning job started: {job['id']}")
print(" You can monitor at https://platform.openai.com/finetune/")
