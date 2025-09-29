import time
import os
from openai import OpenAI, api_key


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Please enter the job ID you want to query here
job_id = OpenAI(api_key=os.getenv("JOB_ID"))

print(f"Polling status of fine-tuning task {job_id}...\n")

while True:
    job = client.fine_tuning.jobs.retrieve(job_id)
    status = job.status
    print(f"Current status: {status}")

    if status in ["succeeded", "failed", "cancelled"]:

        events = client.fine_tuning.jobs.list_events(
            fine_tuning_job_id=job_id, limit=200
        )
        for e in sorted(events.data, key=lambda x: x.created_at):
            msg = getattr(e, "message", "") or getattr(e, "data", "")
            print(f"[{e.created_at}] {msg}")
        break

    time.sleep(20)
