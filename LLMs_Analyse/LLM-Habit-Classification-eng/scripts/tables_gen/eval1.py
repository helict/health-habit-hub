import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from pathlib import Path
from typing import Sequence, Union, Dict, Any, Optional

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
    labels: Optional[Union[Dict[str, str], Sequence[str]]] = None,
    line_width: float = 0.8,
    marker_size: float = 3.0,
):
    xlsx_paths = [Path(p) for p in xlsx_paths]
    assert len(xlsx_paths) >= 2, "Enter at least two data sources (or two different sheets of the same file)"

    def resolve_sheet(i: int, p: Path):
        if isinstance(sheet, (int, str)):
            return sheet
        if isinstance(sheet, (list, tuple)):
            return sheet[i]
        if isinstance(sheet, dict):
            return sheet.get(
                i,
                sheet.get(
                    str(i),
                    sheet.get(str(p), sheet.get(p.name, sheet.get(p.stem, 0))),
                ),
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

        if labels:
            if isinstance(labels, (list, tuple)):
                label = labels[i]
            else:
                label = labels.get(p.stem, p.stem)
        else:
            label = p.stem

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


plot_kappa_lines(
    xlsx_paths=[
        "EN_llm_all_info_with_cost_performance_zeroshot.xlsx",
        "EN_llm_all_info_with_cost_performance_zeroshot.xlsx",
    ],
    sheet=["Sheet2", "Sheet3"],
    labels=["English", "German"],
    key_col="Model",
    value_col="Kappa",
    out_path="Kappa_en_de.png",
)
