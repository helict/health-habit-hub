import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from pathlib import Path
from typing import Sequence, Union, Dict, Any, Optional


def plot_kappa_lines(
    xlsx_paths: Sequence[Union[str, Path]],
    out_path: Union[str, Path] = "kappa_lines.png",
    sheet: Union[int, str, Sequence[Any], Dict[Any, Any]] = 0,
    key_col: str = "Model",
    value_col: str = "Kappa",
    labels: Optional[Dict[str, str]] = None,
    line_width: float = 0.8,
    marker_size: float = 3.0,
):
    xlsx_paths = [Path(p) for p in xlsx_paths]
    assert len(xlsx_paths) >= 2

    def resolve_sheet(i: int, p: Path):
        if isinstance(sheet, (int, str)):
            return sheet
        if isinstance(sheet, (list, tuple)):
            return sheet[i]
        if isinstance(sheet, dict):
            return sheet.get(
                i, sheet.get(str(p), sheet.get(p.name, sheet.get(p.stem, 0)))
            )
        return 0

    palette = (
        list(cm.get_cmap("tab10").colors)
        + list(cm.get_cmap("Set2").colors)
        + list(cm.get_cmap("Dark2").colors)
    )

    s0 = resolve_sheet(0, xlsx_paths[0])
    df0 = pd.read_excel(xlsx_paths[0], sheet_name=s0)[[key_col, value_col]]
    order = df0[key_col].astype(str).tolist()

    plt.figure(figsize=(12, 6))
    plt.axhline(0, color="gray", linestyle="--", linewidth=1)

    for i, p in enumerate(xlsx_paths):
        si = resolve_sheet(i, p)
        df = pd.read_excel(p, sheet_name=si)[[key_col, value_col]]
        df[key_col] = df[key_col].astype(str)
        y = (
            df.set_index(key_col)
            .reindex(order)[value_col]
            .astype(float)
            .fillna(0.0)
            .values
        )
        label = labels.get(p.stem, p.stem) if labels else p.stem

        color = palette[i % len(palette)]
        plt.plot(
            order,
            y,
            color=color,
            marker="o",
            markersize=marker_size,
            markerfacecolor="white",
            markeredgewidth=0.8,
            markeredgecolor=color,
            linewidth=line_width,
            label=label,
        )

    plt.xlabel(key_col)
    plt.ylabel(value_col)
    plt.title(f"{value_col} comparison")
    plt.xticks(rotation=60, ha="right")
    plt.legend()
    plt.tight_layout()
    out_path = Path(out_path)
    plt.savefig(out_path, dpi=300)
    plt.show()
    return out_path


name_map = {
    "diff_llm_all_info_with_cost_performance_oneshot": "Oneshot",
    "diff_llm_all_info_with_cost_performance_with_definition": "Definition",
    "diff_llm_all_info_with_cost_performance_fewshot": "Few-shot",
    "diff_llm_all_info_with_cost_performance_fewshot_with_definition": "Few-shot+Def",
    "diff_llm_all_info_with_cost_performance_oneshot_with_definition": "Oneshot+Def",
}


plot_kappa_lines(
    [
        "EN_llm_all_info_with_cost_performance_zeroshot.xlsx",
        "EN_llm_all_info_with_cost_performance_zeroshot.xlsx",
        "diff_llm_all_info_with_cost_performance_fewshot_with_definition.xlsx",
    ],
    sheet="Sheet3",
    labels=name_map,
    out_path="kappa_lines1.png",
)
