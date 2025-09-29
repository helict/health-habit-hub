from networkx import cost_of_flow
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path
import tiktoken
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    matthews_corrcoef,
    cohen_kappa_score,
)
from transformers import AutoTokenizer
import re
import os

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"


try:
    import anthropic

    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False
    
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


# Automatically select the tokenizer function based on the model name
def select_tokenizer(model_name: str):
    name = model_name.lower().strip()
    if name.startswith("gemini"):
        try:
            import google.generativeai as genai
            import os

            # Prioritize obtaining the API Key from environment variables
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError(
                    "The environment variable GOOGLE_API_KEY is not set, so Gemini cannot use it."
                )
            genai.configure(api_key=api_key)

            # Initializing the Gemini model
            if "pro" in name:
                model = genai.GenerativeModel("gemini-2.5-pro")
                # print("gemini-2.5-pro")
            else:
                model = genai.GenerativeModel("gemini-2.0-flash")
                # print("gemini-2.0-flash")

            def count_tokens(text: str) -> int:
                try:
                    response = model.count_tokens(text)
                    # print(f"Successful output {response.total_tokens}")
                    return response.total_tokens
                except Exception as e:
                    print(f"[Gemini Tokenizer Error] {e}")
                    return len(text.split())

            return count_tokens

        except Exception as e:
            print(
                f"[Gemini Fallback] Unable to initialize Gemini tokenizer, using space estimation: {e}"
            )
            return lambda text: len(text.split())

        # —— o series & GPT-4.1 —— using o200k_base ——
    if any(
        k in name
        for k in [
            "o1",
            "o3",
            "o4",
            "4o",
            "gpt-4.1",
            "gpt4.1",
        ]
    ):
        enc = tiktoken.get_encoding("o200k_base")
        return lambda text: len(enc.encode(text))

    # Claude Series
    elif "claude" in name:
        if HAS_ANTHROPIC and ANTHROPIC_API_KEY:
            client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

            MODEL_MAP = {
                "claude sonnet 4 (extended)": "claude-sonnet-4-20250514",
                "claude sonnet 4": "claude-sonnet-4-20250514",
                "claude sonnet 3.7 (extended)": "claude-3-7-sonnet-20250219",
                "claude sonnet 3.7": "claude-3-7-sonnet-20250219",
                "claude sonnet 3.5": "claude-3-5-sonnet-20241022",
                "claude opus 4 (extended)": "claude-opus-4-20250514",
                "claude opus 4": "claude-opus-4-20250514",
                "claude opus 3": "claude-opus-4-20250514",
            }

            def count_tokens_claude(text: str) -> int:
                chosen = MODEL_MAP.get(name, "claude-opus-4-20250514")
                try:
                    response = client.messages.count_tokens(
                        model=chosen,
                        system="You are a token counting tool.",
                        messages=[{"role": "user", "content": text}],
                    )
                    return response.input_tokens
                except Exception as e:
                    return len(text.split())

            return count_tokens_claude
        else:
            enc = tiktoken.encoding_for_model("gpt-4")
            return lambda text: len(enc.encode(text))

    #  LLaMA 4 Maverick / Scout
    elif "llama" in name and "maverick" in name:
        tokenizer = AutoTokenizer.from_pretrained(
            "meta-llama/Llama-4-Maverick-17B-128E-Instruct", use_fast=True
        )
        # print("meta-llama/Llama-4-Maverick-17B-128E-Instruct")
        return lambda text: len(tokenizer.encode(text, add_special_tokens=False))
    #  LLaMA 4 Maverick / Scout
    elif "llama" in name and "scout" in name:
        tokenizer = AutoTokenizer.from_pretrained(
            "meta-llama/Llama-4-Scout-17B-16E-Instruct", use_fast=True
        )
        # print("meta-llama/Llama-4-Scout-17B-16E-Instruct")
        return lambda text: len(tokenizer.encode(text, add_special_tokens=False))
    elif "llama" in name and "3b" in name:
        tokenizer = AutoTokenizer.from_pretrained(
            "meta-llama/Llama-3.2-3B-Instruct", use_fast=True
        )
        # print("meta-llama/Llama-4-Scout-17B-16E-Instruct")
        return lambda text: len(tokenizer.encode(text, add_special_tokens=False))
    elif "llama" in name and "70b" in name:
        tokenizer = AutoTokenizer.from_pretrained(
            "meta-llama/Llama-3.3-70B-Instruct", use_fast=True
        )
        # print("meta-llama/Llama-4-Scout-17B-16E-Instruct")
        return lambda text: len(tokenizer.encode(text, add_special_tokens=False))
    elif "llama" in name and "8b" in name:
        tokenizer = AutoTokenizer.from_pretrained(
            "meta-llama/Meta-Llama-3.1-8B-Instruct", use_fast=True
        )
        # print("meta-llama/Llama-4-Scout-17B-16E-Instruct")
        return lambda text: len(tokenizer.encode(text, add_special_tokens=False))
    #  mistral
    elif "mistral" in name and "large" in name:
        tokenizer = AutoTokenizer.from_pretrained(
            "mistralai/Mistral-Large-Instruct-2407", use_fast=True
        )
        # print("mistralai/Mistral-Large-Instruct-2407")
        return lambda text: len(tokenizer.encode(text, add_special_tokens=False))
    elif "mistral" in name and "7b" in name:
        tokenizer = AutoTokenizer.from_pretrained(
            "mistralai/Mistral-7B-Instruct-v0.3", use_fast=True
        )
        # print("mistralai/Mistral-Large-Instruct-2407")
        return lambda text: len(tokenizer.encode(text, add_special_tokens=False))

    #  DeepSeek-V3
    elif "deepseek" in name and "v3" in name:
        tokenizer = AutoTokenizer.from_pretrained(
            "deepseek-ai/DeepSeek-V3", trust_remote_code=True
        )
        return lambda text: len(tokenizer.encode(text, add_special_tokens=False))
    elif "deepseek" in name and "v2" in name:
        tokenizer = AutoTokenizer.from_pretrained(
            "deepseek-ai/DeepSeek-Coder-V2-Lite-Instruct", trust_remote_code=True
        )
        return lambda text: len(tokenizer.encode(text, add_special_tokens=False))
    elif "deepseek" in name and "r1" in name:
        tokenizer = AutoTokenizer.from_pretrained(
            "deepseek-ai/DeepSeek-R1", trust_remote_code=True
        )
        return lambda text: len(tokenizer.encode(text, add_special_tokens=False))

    elif "qwen3" in name:
        tokenizer = AutoTokenizer.from_pretrained(
            "Qwen/Qwen3-8B", trust_remote_code=True
        )
        return lambda text: len(tokenizer.encode(text, add_special_tokens=False))

    #  Default fallback: space word segmentation
    else:
        print(f"{name} Model not found!")
        return lambda text: len(text.split())


class LLMInfo:
    input_prompt = ""  # Input prompt common to all models

    def __init__(self, name: str, input_cost: float, output_cost: float):
        self.name = name
        self.input_cost = input_cost
        self.output_cost = output_cost
        self.output = ""
        self.tokenizer_fn = select_tokenizer(name)
        self.metrics = None
        self.cost = None
        self.cost_performance = {}

    def __repr__(self):
        return (
            f"LLMInfo(name='{self.name}', input_cost={self.input_cost}, "
            f"output_cost={self.output_cost}, output_preview={repr(self.output[:30]) + '...'})"
        )

    @classmethod
    def set_input_prompt(cls, prompt: str):
        cls.input_prompt = prompt

    def compute_total_cost(self) -> float:
        if self.tokenizer_fn is None:
            raise ValueError("Tokenizer function is not defined.")
        input_tokens = self.tokenizer_fn(LLMInfo.input_prompt)
        output_tokens = self.tokenizer_fn(self.output)
        # print(self.input_cost)
        input_price = input_tokens / 1_000_000 * self.input_cost
        output_price = output_tokens / 1_000_000 * self.output_cost
        self.cost = round(input_price + output_price, 4)
        return self.cost

    @staticmethod
    def extract_labels(text: str):
        pattern = re.compile(r"—.*?\b(habit|not a habit)\b", re.IGNORECASE)
        return [match.group(1).lower() for match in pattern.finditer(text)]

    @staticmethod
    def normalize_labels(raw_labels):
        label_map = {"habit": 1, "not a habit": 0, "Habit": 1, "Not a habit": 0}
        return [label_map.get(str(x).strip().lower(), 0) for x in raw_labels]

    def evaluate(self, true_labels: list):
        """
        Evaluate the label performance of the current LLM output and return all common classification metrics
        """
        pred_labels = LLMInfo.extract_labels(self.output)
        min_len = min(len(true_labels), len(pred_labels))
        y_true = LLMInfo.normalize_labels(true_labels[:min_len])
        y_pred = LLMInfo.normalize_labels(pred_labels[:min_len])

        self.metrics = {
            "accuracy": accuracy_score(y_true, y_pred),
            "precision": precision_score(y_true, y_pred, zero_division=0),
            "recall": recall_score(y_true, y_pred, zero_division=0),
            "f1": f1_score(y_true, y_pred, zero_division=0),
            "mcc": matthews_corrcoef(y_true, y_pred),
            "kappa": cohen_kappa_score(y_true, y_pred),
        }
        return self.metrics

    def get_cost_performance(self):
        """
        Calculate the ratio of all evaluated metrics to the cost and store it as the self.cost_performance attribute.
        """
        if self.metrics is None:
            raise ValueError("Please call the evaluate() method first to generate metrics.")
        cost = self.compute_total_cost()
        if cost == 0:
            raise ValueError("The model cost is 0, so the cost-effectiveness cannot be calculated.")

        self.cost_performance = {
            metric: value / cost for metric, value in self.metrics.items()
        }
        return self.cost_performance


def load_llms_from_excel(file_path: str) -> dict:
    df = pd.read_excel(file_path)
    llm_dict = {
        row["LLM Name"]: LLMInfo(
            row["LLM Name"],
            row["Costs per 1M token (input)"],
            row["Costs per 1M token (output)"],
        )
        for _, row in df.iterrows()
    }
    return llm_dict
