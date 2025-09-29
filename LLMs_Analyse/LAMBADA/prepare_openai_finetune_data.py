import pandas as pd
import json


df = pd.read_csv("habits.csv")
df["label"] = df["label"].astype(str)


output_file = "habits_gpt_finetune.jsonl"


with open(output_file, "w", encoding="utf-8") as f:
    for _, row in df.iterrows():
        system_msg = f"You are a generator for category {row['label']}."
        user_msg = "Please give me a typical example."
        assistant_msg = row["text"]

        json.dump(
            {
                "messages": [
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg},
                    {"role": "assistant", "content": assistant_msg},
                ]
            },
            f,
            ensure_ascii=False,
        )
        f.write("\n")

print(f" JSONL file saved to: {output_file}")
