import allure
import pandas as pd
import os


class AllureHelper:

    _test_data_df = None

    @staticmethod
    def _load_test_data():
        if AllureHelper._test_data_df is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            xlsx_path = os.path.join(base_dir, "data", "testdata.xlsx")

            if not os.path.exists(xlsx_path):
                raise FileNotFoundError(f"Test data Excel not found: {xlsx_path}")

            AllureHelper._test_data_df = pd.read_excel(xlsx_path)

            # Clean column names
            AllureHelper._test_data_df.columns = (
                AllureHelper._test_data_df.columns.str.strip()
            )

        return AllureHelper._test_data_df

    @staticmethod
    def get_test_row(tcid: str) -> dict:
        df = AllureHelper._load_test_data()
        rows = df[df["TC ID"] == tcid].to_dict(orient="records")
        if not rows:
            raise ValueError(f"No test data found for TC ID: {tcid}")
        return rows[0]

    # =====================================================
    # ✅ ADD THIS METHOD (DO NOT CHANGE TEST CODE)
    # =====================================================
    @staticmethod
    def attach_description(tcid: str):
        """
        Compatibility method for existing tests.
        """
        AllureHelper.attach_common_description(tcid)

    # =====================================================

    @staticmethod
    def attach_common_description(tcid: str):
        row = AllureHelper.get_test_row(tcid)

        allure.dynamic.title(tcid)
        allure.dynamic.description_html(f"""
        <b>TC ID:</b> {tcid}<br>
        <b>Screen:</b> {row.get("Screen", "")}<br>
        <b>Test Case:</b> {row.get("Test Case", "")}<br>
        <b>Steps:</b> {row.get("Steps", "")}<br>
        <b>Test Data:</b> {row.get("Test Data", "")}<br>
        <b>Expected Result:</b> {row.get("Expected Result", "")}<br>
        """)

    @staticmethod
    def attach_pass_description(tcid: str):
        row = AllureHelper.get_test_row(tcid)
        allure.attach(
            row.get("Pass Description", ""),
            name="PASS Description",
            attachment_type=allure.attachment_type.TEXT
        )

    @staticmethod
    def attach_fail_description(tcid: str):
        row = AllureHelper.get_test_row(tcid)
        allure.attach(
            row.get("Fail Description", ""),
            name="FAIL Description",
            attachment_type=allure.attachment_type.TEXT
        )

    @staticmethod
    def attach_failure(error: str):
        allure.attach(
            error,
            name="Failure Error",
            attachment_type=allure.attachment_type.TEXT
        )
