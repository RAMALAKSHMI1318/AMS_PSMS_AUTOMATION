import pandas as pd
import os
import time


def update_excel_status(
    excel_path: str,
    tcid: str,
    status: str,
    remarks: str
):
    """
    Update Status and Remarks for a test case in Excel
    """

    df = pd.read_excel(excel_path)

    if tcid not in df["TC ID"].values:
        raise ValueError(f"{tcid} not found in Excel")

    df.loc[df["TC ID"] == tcid, "Status"] = status
    df.loc[df["TC ID"] == tcid, "Remarks"] = remarks

    # Safe write (avoid file lock issues)
    temp_file = excel_path.replace(".xlsx", "_temp.xlsx")
    df.to_excel(temp_file, index=False)

    os.replace(temp_file, excel_path)
