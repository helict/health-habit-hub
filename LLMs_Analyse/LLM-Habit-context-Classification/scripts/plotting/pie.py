"""
Generate a pie chart of prompt-type distribution from an Excel sheet.

Expected columns:
- "Prompt Type"
- "Number"

Default sheet: "Sheet 4"
"""

import argparse
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def read_data(
    xlsx_path: Path,
    sheet: str = "Sheet 4",
    label_col: str = "Prompt Type",
    value_col: str = "Number",
) -> pd.DataFrame:
    df = pd.read_excel(xlsx_path, sheet_name=sheet)
    data = df[[label_col, value_col]].copy()
    data[value_col] = pd.to_numeric(data[value_col], errors="coerce")
    data = data.dropna(subset=[value_col])
    return data.groupby(label_col, as_index=False)[value_col].sum()


def plot_pie(
    data: pd.DataFrame,
    label_col: str = "Prompt Type",
    value_col: str = "Number",
    title: str = "Prompt-type distribution (Mean Accuracy (Embedding-Based)>=0.85) – Habit context classification",
    out_path: Path = Path("prompt_type_pie.png"),
):
    labels = list(data[label_col])
    sizes = list(data[value_col])

    fig, ax = plt.subplots(figsize=(7, 7), dpi=200)
    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        autopct=lambda p: f"{p:.1f}%\n({round(p/100.0*sum(sizes))})" if p >= 0 else "",
        startangle=90,
        pctdistance=0.8,
        labeldistance=1.1,
    )
    ax.axis("equal")
    ax.set_title(title)
    plt.tight_layout()
    fig.savefig(out_path, bbox_inches="tight")
    print(f"Saved pie chart to: {out_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate a prompt-type pie chart from an Excel sheet."
    )
    parser.add_argument(
        "excel", type=str, help="Path to the Excel file (e.g., data.xlsx)"
    )
    parser.add_argument("--sheet", type=str, default="Sheet 4", help="Sheet name")
    parser.add_argument(
        "--out", type=str, default="prompt_type_pie.png", help="Output image path"
    )
    args = parser.parse_args()

    data = read_data(args.excel, sheet=args.sheet)
    plot_pie(data, out_path=Path(args.out))


if __name__ == "__main__":
    main()

# python pie.py "fig.xlsx" --sheet "Sheet3" --out "prompt_type_habit_context_pie.png"
