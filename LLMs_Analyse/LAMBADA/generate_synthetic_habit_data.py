import openai
import pandas as pd
import os

#  Configurations
openai.api_key = os.getenv("OPENAI_API_KEY")

# Please enter the trained model id
model_id = os.getenv("FINETUNED_MODEL_ID")

def generate_labeled_samples(
    num_habit=10, num_not_habit=10, output_file="generated_labeled_data.csv"
):
    label_prompts = {
        0: "Please write a German sentence that describes a daily habit.",
        1: "Please write a German sentence that does NOT describe a habit.",
    }

    sample_counts = {
        0: num_habit,
        1: num_not_habit,
    }

    generated_samples = []

    for label, prompt in label_prompts.items():
        print(f"\n Generating {sample_counts[label]} samples for label {label}...")
        for i in range(sample_counts[label]):
            response = openai.ChatCompletion.create(
                model=model_id,
                messages=[
                    {"role": "system", "content": "You are a German text generator."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.9,
                top_p=0.95,
                frequency_penalty=0.5,
                presence_penalty=0.8,
                max_tokens=50,
            )
            generated_text = response["choices"][0]["message"]["content"].strip()
            print(f"{i+1}. {generated_text}")
            generated_samples.append({"text": generated_text, "label": label})

    # Save to file
    df_gen = pd.DataFrame(generated_samples)
    df_gen.to_csv(output_file, index=False, encoding="utf-8")
    print(f"\nSaved to {output_file}")


#  example usage
if __name__ == "__main__":
    generate_labeled_samples(num_habit=20, num_not_habit=20)
