import json


input_file = "habits_gpt_finetune1.jsonl"
train_file = "habits_train.jsonl"
valid_file = "habits_valid.jsonl"


with open(input_file, "r", encoding="utf-8") as f:
    lines = [json.loads(line.strip()) for line in f if line.strip()]


habit_examples = lines[:33]
nonhabit_examples = lines[33:]


valid_set = habit_examples[:10] + nonhabit_examples[:10]


train_set = habit_examples[10:] + nonhabit_examples[10:]


with open(train_file, "w", encoding="utf-8") as f_train:
    for item in train_set:
        json.dump(item, f_train, ensure_ascii=False)
        f_train.write("\n")


with open(valid_file, "w", encoding="utf-8") as f_valid:
    for item in valid_set:
        json.dump(item, f_valid, ensure_ascii=False)
        f_valid.write("\n")

print(
    f"Dataset splitting completed:\n - Training set: {len(train_set)} items → {train_file}\n - Validation set: {len(valid_set)} items → {valid_file}"
)
