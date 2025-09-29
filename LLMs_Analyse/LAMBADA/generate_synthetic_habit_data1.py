from openai import OpenAI
import pandas as pd
import os


api_key = os.getenv("OPENAI_API_KEY")


client = OpenAI(api_key=api_key)

# Please enter the trained model id
model_id = os.getenv("FINETUNED_MODEL_ID")



def generate_labeled_samples(
    num_habit=10, num_not_habit=10, output_file="generated_labeled_data.csv"
):
    label_prompts = {
        0: f"Write {num_habit} German sentences that each describe a habit. ",
        1: f"Write {num_not_habit} German sentences that clearly describes a unique, one-time action or event (not a habit). ",
    }

    generated_samples = []

    for label, prompt in label_prompts.items():
        print(f"\nGenerating {prompt}")
        if label == 0:
            system_msg = "You generate a typical German sentence describing a habitual behavior in daily life."
        else:
            system_msg = "You generate a German sentence describing a non-habitual, one-time or spontaneous event."
        response = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt},
            ],
            temperature=0.25,
            top_p=0.85,
            frequency_penalty=0.4,
            presence_penalty=0.3,
            max_tokens=300,
        )

        sentences = [
            s.strip().lstrip("0123456789. ").strip()
            for s in response.choices[0].message.content.split("\n")
            if s.strip()
        ]

        for s in sentences:
            generated_samples.append({"text": s, "label": label})

    df_gen = pd.DataFrame(generated_samples)
    df_gen.to_csv(output_file, index=False, encoding="utf-8")
    print(f"\nSaved to {output_file}")


def generate_labeled_samples_one_by_one(
    num_habit=10, num_not_habit=10, output_file="generated_labeled_data_onebyone.csv"
):
    generated_samples = []

    for label in [0, 1]:
        if label == 0:
            system_msg = "You generate a typical German sentence describing a habitual behavior in daily life."
            single_prompt = (
                "Write one German sentence that clearly describes a habitual behavior."
            )
        else:
            system_msg = "You generate a German sentence describing a non-habitual, one-time or spontaneous event."
            single_prompt = "Write one German sentence that clearly describes a unique, one-time action or event (not a habit)."

        target_count = num_habit if label == 0 else num_not_habit

        for i in range(target_count):
            print(f"\nGenerating sentence {i+1}/{target_count} for label {label}...")

            response = client.chat.completions.create(
                model=model_id,
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": single_prompt},
                ],
                temperature=0.25,
                top_p=0.85,
                frequency_penalty=0.4,
                presence_penalty=0.3,
                max_tokens=30,
            )

            sentence = response.choices[0].message.content.strip()
            generated_samples.append({"text": sentence, "label": label})

    df_gen = pd.DataFrame(generated_samples)
    df_gen.to_csv(output_file, index=False, encoding="utf-8")
    print(f"\n Saved to {output_file}")


if __name__ == "__main__":
    generate_labeled_samples(num_habit=5, num_not_habit=5)
