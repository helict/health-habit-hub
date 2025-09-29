import pandas as pd
from pathlib import Path


def diff_xlsx(test_path, base_path, key_col="Model", test_sheet=0, base_sheet=0):
    A = (
        pd.read_excel(test_path, sheet_name=test_sheet)
        .set_index(key_col)
        .apply(pd.to_numeric, errors="coerce")
    )
    B = (
        pd.read_excel(base_path, sheet_name=base_sheet)
        .set_index(key_col)
        .apply(pd.to_numeric, errors="coerce")
    )

    diff = A.sub(B, fill_value=0).reset_index()

    out_path = Path(test_path).with_name(f"diff_{Path(test_path).stem}.xlsx")
    diff.to_excel(out_path, index=False)
    return diff, out_path


diff, out_path = diff_xlsx(
    "llm_all_info_with_cost_performance_oneshot.xlsx",
    "llm_all_info_with_cost_performance_zeroshot.xlsx",
    test_sheet="Sheet2",
    base_sheet="Sheet6",
)
diff, out_path = diff_xlsx(
    "llm_all_info_with_cost_performance_fewshot.xlsx",
    "llm_all_info_with_cost_performance_zeroshot.xlsx",
    test_sheet="Sheet2",
    base_sheet="Sheet6",
)
diff, out_path = diff_xlsx(
    "llm_all_info_with_cost_performance_with_definition.xlsx",
    "llm_all_info_with_cost_performance_zeroshot.xlsx",
    test_sheet="Sheet2",
    base_sheet="Sheet6",
)
diff, out_path = diff_xlsx(
    "llm_all_info_with_cost_performance_oneshot_with_definition.xlsx",
    "llm_all_info_with_cost_performance_zeroshot.xlsx",
    test_sheet="Sheet2",
    base_sheet="Sheet6",
)
diff, out_path = diff_xlsx(
    "llm_all_info_with_cost_performance_fewshot_with_definition.xlsx",
    "llm_all_info_with_cost_performance_zeroshot.xlsx",
    test_sheet="Sheet2",
    base_sheet="Sheet6",
)
