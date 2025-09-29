import re
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Sequence, Union, Optional, List

def _safe_name(s: str) -> str:
    return re.sub(r"[^a-zA-Z0-9._-]+", "_", s).strip("_").lower()

def plot_each_prompt_bar_from_excel(
    xlsx_path: Union[str, Path],
    sheet: Union[int, str] = 0,
    model_col: str = "Model",
    value_cols: Sequence[str] = (
        "zero shot",
        "one shot",
        "few shot",
        "with definition",
        "one shot with definition",
        "few shot with definition",
    ),
    orientation: str = "vertical",        
    baseline: Optional[float] = None,     
    figsize=(12, 7),
    dpi: int = 160,
    out_dir: Optional[Union[str, Path]] = None,  
    prefix: str = "kappa_context_",               
    ylim: Optional[tuple] = (-0.1, 1.05), 
) -> List[Path]:
    """
    Draw a single-series bar chart for each column in value_cols
    """
    xlsx_path = Path(xlsx_path)
    df = pd.read_excel(xlsx_path, sheet_name=sheet)

    
    missing = [c for c in [model_col, *value_cols] if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in table: {missing}\nExisting columns: {list(df.columns)}")

    
    data = df[[model_col, *value_cols]].copy()
    for c in value_cols:
        data[c] = pd.to_numeric(data[c], errors="coerce")

    saved_paths: List[Path] = []

    for col in value_cols:
        
        d = data[[model_col, col]].dropna(subset=[col])

        plt.figure(figsize=figsize, dpi=dpi)
        ax = plt.gca()

        if orientation.lower().startswith("h"):
            ax.barh(d[model_col], d[col])
            ax.set_xlabel("Score")
            ax.set_ylabel(model_col)
            if baseline is not None:
                ax.axvline(baseline, linestyle="--")
        else:
            ax.bar(d[model_col], d[col])
            ax.set_ylabel("Score")
            ax.set_xlabel(model_col)
            plt.xticks(rotation=75, ha="right")
            if baseline is not None:
                ax.axhline(baseline, linestyle="--")

        ax.set_title(f"Mean Accuracy (Embedding-Based) – {col}")
        if ylim is not None:
            ax.set_ylim(*ylim)
        plt.tight_layout()

        if out_dir is not None:
            out_dir = Path(out_dir)
            out_dir.mkdir(parents=True, exist_ok=True)
            fpath = out_dir / f"{prefix}{_safe_name(col)}_{orientation}.png"
            plt.savefig(fpath, bbox_inches="tight")
            saved_paths.append(fpath)
            plt.close()
        else:
            plt.show()

    return saved_paths

plot_each_prompt_bar_from_excel(
    xlsx_path="fig.xlsx",
    sheet=1,
    orientation="vertical",
    baseline=0.85,
    out_dir="figs_habit_context_classification",
)



