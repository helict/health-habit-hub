from networkx import cost_of_flow
import pandas as pd
from io import StringIO
import tiktoken
from dotenv import load_dotenv
from pathlib import Path
import numpy as np
import csv
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    matthews_corrcoef,
    cohen_kappa_score,
    hamming_loss,
)
from transformers import AutoTokenizer
import re
import os

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
import re
from typing import Dict, List
from sentence_transformers import SentenceTransformer, util

try:
    import anthropic

    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


def select_tokenizer(model_name: str):
    """
    Automatically select the tokenizer function based on the model name.
    """
    name = model_name.lower().strip()
    # The Gemini series uses the Vertex AI local tokenizer
    if name.startswith("gemini"):
        try:
            import google.generativeai as genai
            import os

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

        # o series & GPT-4.1 — Using o200k_base
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
    if "gpt-oss-120b" in name or "gpt-oss-20b" in name:
        enc = tiktoken.get_encoding("o200k_harmony")
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
                    # print(f"[Claude tokenizer] Error: {e}; fallback to crude count,{name}")
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

    else:
        print(f"Model {name} not found!")
        return lambda text: len(text.split())


class LLMInfo:
    input_prompt = ""

    def __init__(self, name: str, input_cost: float, output_cost: float):
        self.name = name
        self.input_cost = input_cost
        self.output_cost = output_cost
        self.output = ""
        self.tokenizer_fn = select_tokenizer(name)
        self.metrics = None
        self.embedding_metrics = (None,)
        self.substring_metrics = (None,)
        self.binary_metrics = (None,)
        self.cost = None
        self.cost_performance = ({},)
        self.embedding_cost_performance = ({},)
        self.substring_cost_performance = ({},)
        self.binary_metrics_cost_performance = {}

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

    def parse_output_to_context_labels(self) -> Dict[str, List[List[str]]]:
        """
        Parses a collection of tags representing six contextual components from self.output (a CSV string).
        Automatically strips Markdown wrappers (e.g., ```csv```), cleans bracket confidence, spaces, punctuation, and lowercases.
        """
        raw_output = self.output.strip()

        if raw_output.startswith("```csv"):
            raw_output = raw_output[6:].strip()
        if raw_output.endswith("```"):
            raw_output = raw_output[:-3].strip()

        if not raw_output:
            raise ValueError("Output is empty. Please set self.output before parsing.")

        # Replace the header to prevent model output errors
        header = "Number,Original Sentence,TIME,PHYSICAL SETTING,PRIOR BEHAVIOR,OTHER PEOPLE,INTERNAL STATE,BEHAVIOR"
        lines = raw_output.splitlines()
        lines[0] = header

        # Processing fields using the csv module
        reader = csv.reader(StringIO("\n".join(lines)))
        rows = list(reader)

        headers = rows[0]
        data_rows = rows[1:]

        # Repair line length
        processed_data = []
        for row in data_rows:
            if len(row) < 8:
                row.extend([""] * (8 - len(row)))
            elif len(row) > 8:
                row[7] = ",".join(row[7:])
                row = row[:8]
            processed_data.append(row)

        df = pd.DataFrame(processed_data, columns=headers)

        contextual_components = [
            "TIME",
            "PHYSICAL SETTING",
            "PRIOR BEHAVIOR",
            "OTHER PEOPLE",
            "INTERNAL STATE",
            "BEHAVIOR",
        ]

        result: Dict[str, List[List[str]]] = {}

        for col in contextual_components:
            processed_col = []

            for raw_cell in df[col].fillna("").astype(str):
                parts = raw_cell.split("//") if "//" in raw_cell else [raw_cell]
                labels = []

                for part in parts:
                    cleaned = re.sub(r"\s*\(.*?\)", "", part)
                    cleaned = cleaned.strip().rstrip(".,，。").lower()

                    # Skip fields with only confidence (e.g. "0.99")
                    if not cleaned or re.fullmatch(r"\d+(\.\d+)?", cleaned):
                        continue

                    labels.append(cleaned)

                processed_col.append(labels)

            result[col] = processed_col

        return result

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

    def evaluate_with_embedding_similarity(
        self,
        component_names: List[str],
        predicted: Dict[str, List[List[str]]],
        gold: Dict[str, List[List[str]]],
        sim_threshold: float = 0.75,
        embedding_model: SentenceTransformer = SentenceTransformer(
            "paraphrase-MiniLM-L6-v2"
        ),
    ) -> Dict[str, float]:
        """
        Evaluate the semantic similarity between predicted and gold and return the accuracy for each context feature.
        """

        def normalize(s: str) -> str:
            return s.strip().lower().rstrip(".,，。")

        def is_match(pred_cell: List[str], gold_cell: List[str]) -> bool:
            if not gold_cell:
                return not pred_cell
            if not pred_cell:
                return False

            pred_text = normalize(pred_cell[0])
            gold_texts = [normalize(g) for g in gold_cell]

            pred_emb = embedding_model.encode(pred_text, convert_to_tensor=True)
            gold_embs = embedding_model.encode(gold_texts, convert_to_tensor=True)
            cosine_scores = util.cos_sim(pred_emb, gold_embs)
            max_score = cosine_scores.max().item()
            return max_score >= sim_threshold

        self.embedding_metrics = {}

        for component in component_names:
            y_pred = predicted.get(component, [])
            y_true = gold.get(component, [])
            assert len(y_pred) == len(y_true), f"{component}: Mismatched lengths"

            correct = sum(is_match(y_pred[i], y_true[i]) for i in range(len(y_true)))
            acc = correct / len(y_true) if y_true else 0.0
            self.embedding_metrics[component] = acc
            # print(f"{component} Accuracy (Embedding): {acc:.2%} ({correct}/{len(y_true)})")

        return self.embedding_metrics

    def evaluate_with_substring_match(
        self,
        component_names: List[str],
        predicted: Dict[str, List[List[str]]],
        gold: Dict[str, List[List[str]]],
    ) -> Dict[str, float]:
        """
        The classification accuracy is evaluated using substring matching: if the predicted value is a substring of any expression in the gold label, it is considered correct.
        """

        def normalize(s: str) -> str:
            return s.strip().lower().rstrip(".,，。")

        def is_match(pred_cell: List[str], gold_cell: List[str]) -> bool:
            if not gold_cell:
                return not pred_cell
            if not pred_cell:
                return False
            p = normalize(pred_cell[0])
            for g in gold_cell:
                g_clean = normalize(g)
                if p in g_clean:
                    return True
            return False

        self.substring_metrics = {}

        for component in component_names:
            y_pred = predicted.get(component, [])
            y_true = gold.get(component, [])
            assert len(y_pred) == len(y_true), f"{component}：Prediction and label length are inconsistent"

            correct = 0
            for i in range(len(y_true)):
                if is_match(y_pred[i], y_true[i]):
                    correct += 1

            acc = correct / len(y_true) if y_true else 0.0
            self.substring_metrics[component] = acc
            # print(f"{component} Accuracy (Substring Match): {acc:.2%} ({correct}/{len(y_true)})")

        return self.substring_metrics

    def evaluate_binary_metrics_per_component(
        self,
        component_names: List[str],
        predicted: Dict[str, List[List[str]]],
        gold: Dict[str, List[List[str]]],
        metrics_to_compute: List[str] = [
            "accuracy",
            "precision",
            "recall",
            "f1",
            "mcc",
            "kappa",
        ],
    ) -> Dict[str, Dict[str, float]]:
        """
        Treat each context component as a binary classification task (whether it is correctly identified or not), calculate multiple evaluation metrics, and supplement the overall micro_f1, macro_f1, and hamming_loss.
        """
        results = {}

        y_true_all = []
        y_pred_all = []

        for component in component_names:
            pred_list = predicted.get(component, [])
            gold_list = gold.get(component, [])

            assert len(pred_list) == len(
                gold_list
            ), f"{component}: Prediction and label length are inconsistent"

            y_pred = [1 if p else 0 for p in pred_list]
            y_true = [1 if g else 0 for g in gold_list]

            y_true_all.append(y_true)
            y_pred_all.append(y_pred)

            component_result = {}

            if "accuracy" in metrics_to_compute:
                component_result["accuracy"] = accuracy_score(y_true, y_pred)

            if "precision" in metrics_to_compute:
                component_result["precision"] = precision_score(
                    y_true, y_pred, zero_division=0
                )

            if "recall" in metrics_to_compute:
                component_result["recall"] = recall_score(
                    y_true, y_pred, zero_division=0
                )

            if "f1" in metrics_to_compute:
                component_result["f1"] = f1_score(y_true, y_pred, zero_division=0)

            if "mcc" in metrics_to_compute:
                component_result["mcc"] = matthews_corrcoef(y_true, y_pred)

            if "kappa" in metrics_to_compute:
                component_result["kappa"] = cohen_kappa_score(y_true, y_pred)

            results[component] = component_result

        y_true_all = np.array(y_true_all).T  # shape: (n_samples, n_components)
        y_pred_all = np.array(y_pred_all).T

        results["__overall__"] = {
            "micro_f1": f1_score(
                y_true_all, y_pred_all, average="micro", zero_division=0
            ),
            "macro_f1": f1_score(
                y_true_all, y_pred_all, average="macro", zero_division=0
            ),
            "hamming_loss": hamming_loss(y_true_all, y_pred_all),
        }

        self.binary_metrics = results
        return results

    def get_binary_cost_performance(self) -> Dict[str, float]:
        """
        Computes the ratio of the two-level metric structure generated by evaluate_binary_metrics_per_component() to the cost.
        The output format is {"COMPONENT.METRIC": value / cost}
        """
        if not hasattr(self, "binary_metrics") or self.binary_metrics is None:
            raise ValueError(
                "Please call evaluate_binary_metrics_per_component() first to generate binary_metrics."
            )

        cost = self.compute_total_cost()
        if cost == 0:
            raise ValueError("The model cost is 0 and the cost-effectiveness cannot be calculated.")

        self.binary_metrics_cost_performance = {}

        for component, metrics_dict in self.binary_metrics.items():
            for metric_name, value in metrics_dict.items():
                if isinstance(value, (int, float)):
                    key = f"{component}.{metric_name}"
                    self.binary_metrics_cost_performance[key] = round(value / cost, 4)

        return self.binary_metrics_cost_performance

    def get_embedding_cost_performance(self):
        """
        Calculate the ratio of all evaluated metrics to the cost and store it as the self.cost_performance attribute.
        """
        if self.embedding_metrics is None:
            raise ValueError("Please call the evaluate() method first to generate metrics.")
        cost = self.compute_total_cost()
        if cost == 0:
            raise ValueError("The model cost is 0, so the cost-effectiveness cannot be calculated.")

        self.embedding_cost_performance = {
            metric: value / cost for metric, value in self.embedding_metrics.items()
        }
        return self.embedding_cost_performance

    def get_substring_cost_performance(self):
        """
        Calculate the ratio of all evaluated metrics to the cost and store it as the self.cost_performance attribute.
        """
        if self.substring_metrics is None:
            raise ValueError("Please call the evaluate() method first to generate metrics.")
        cost = self.compute_total_cost()
        if cost == 0:
            raise ValueError("The model cost is 0, so the cost-effectiveness cannot be calculated.")

        self.substring_cost_performance = {
            metric: value / cost for metric, value in self.substring_metrics.items()
        }
        return self.substring_cost_performance

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
