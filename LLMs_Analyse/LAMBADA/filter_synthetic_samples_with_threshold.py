import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F


model_path = "./output/bert_german_cls/final_model"
input_file = "generated_labeled_data.csv"
output_file = "filtered_synthetic_data.csv"
threshold = 0.6


tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)
model.eval()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)


df = pd.read_csv(input_file)

filtered_rows = []


def predict_with_threshold(text, true_label, threshold=0.3):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=128).to(device)
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = F.softmax(logits, dim=1)
        pred_label = torch.argmax(probs, dim=1).item()
        confidence = probs[0][true_label].item()  

    return pred_label == true_label and confidence >= threshold


for idx, row in df.iterrows():
    if predict_with_threshold(row["text"], row["label"], threshold=threshold):
        filtered_rows.append(row)


df_filtered = pd.DataFrame(filtered_rows)
df_filtered.to_csv(output_file, index=False, encoding="utf-8")
print(f"Filtering is done using threshold={threshold}, retaining {len(df_filtered)} samples and saving them to {output_file}")
