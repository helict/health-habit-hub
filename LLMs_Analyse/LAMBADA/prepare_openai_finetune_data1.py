import pandas as pd
import json
import random
from pathlib import Path


input_file = Path("habits1.csv")
output_file = Path("habits_gpt_finetune1.jsonl")


label_to_prompt = {
    "0": [
        "Please write a German sentence that describes a daily habit.",
        "Write a German example of a habitual action someone might do."
    ],
    "1": [
        "Please write a German sentence that does NOT describe a habit.",
        "Write a German statement that describes a one-time or non-habitual event."
    ]
}


df = pd.read_csv(input_file)
df = df.dropna(subset=["label", "text"])
df["label"] = df["label"].astype(str).str.strip()
df["text"] = df["text"].astype(str).str.strip()


with output_file.open("w", encoding="utf-8") as f:
    for _, row in df.iterrows():
        label = row["label"]
        if row["label"] == "0":
            system_msg = "You generate a typical German sentence describing a habitual behavior in daily life."
        else:
            system_msg = "You generate a German sentence describing a non-habitual, one-time or spontaneous event."

        
        user_msg = random.choice(label_to_prompt.get(label, ["Please give me a typical example."]))
        assistant_msg = row["text"]

        json.dump({
            "messages": [
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg},
                {"role": "assistant", "content": assistant_msg}
            ]
        }, f, ensure_ascii=False)
        f.write("\n")

print(f"The JSONL file is generated and saved to: {output_file.resolve()}")
