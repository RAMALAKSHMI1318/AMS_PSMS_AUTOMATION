# from playwright.sync_api import Page, expect


# class ProjectPage:
#     def __init__(self, page: Page):
#         self.page = page

#         # ===============================
#         # Navigation
#         # ===============================
#         self.link_projects = page.get_by_role("link", name="Projects")
#         self.btn_add_project = page.get_by_role(
#     "button", name="Project", exact=True
# )


#         # ===============================
#         # Add Project Form Fields
#         # ===============================
#         self.input_po_no = page.get_by_role("textbox", name="PO No.")
#         self.input_project_name = page.get_by_role("textbox", name="Project Name")
#         self.input_customer_name = page.get_by_role("textbox", name="Customer Name")

#         # Dropdown (based on your codegen)
#         self.select_customer = page.locator("select")

#         self.input_description = page.get_by_role("textbox", name="Description")
#         self.input_qty = page.get_by_placeholder("Qty")
#         self.input_remark = page.get_by_role(
#             "textbox", name="Type your remark here"
#         )

#         self.pdc_date_picker = page.get_by_role("combobox", name="PDC Date")

#         self.btn_save = page.get_by_role("button", name="Save")

#         # ===============================
#         # Common / Validation
#         # ===============================
#         self.toast_message = page.locator(
#             ".toast-message, .p-toast-detail, .alert-success"
#         )

#     # ===============================
#     # Actions
#     # ===============================

#     def open_projects_tab(self):
#         """Open Projects module"""
#         self.link_projects.click()

#     def open_add_project(self):
#         """Open New Project form"""
#         self.open_projects_tab()
#         self.btn_add_project.click()

#     def fill_project_details(
#         self,
#         po_no: str,
#         project_name: str,
#         customer: str,
#         description: str,
#         qty: str,
#         remark: str,
#     ):
#         """Fill Project creation form"""
#         self.input_po_no.fill(po_no)
#         self.input_project_name.fill(project_name)
#         self.input_customer_name.fill(customer)

#         # Static select option as per your current app behavior
#         self.select_customer.select_option("172")

#         self.input_description.fill(description)
#         self.input_qty.fill(qty)
#         self.input_remark.fill(remark)

#     def select_pdc_date(self, day: str = "26"):
#         """Select PDC date"""
#         self.pdc_date_picker.click()
#         self.page.get_by_text(day, exact=True).click()

#     def save_project(self):
#         """Save Project"""
#         self.btn_save.click()

#     # ===============================
#     # Verifications
#     # ===============================

#     def verify_project_created(self, project_name: str):
#         """Verify project creation"""
#         try:
#             expect(self.toast_message).to_be_visible(timeout=5000)
#         except Exception:
#             # Fallback verification in grid/list
#             expect(
#                 self.page.get_by_text(project_name)
#             ).to_be_visible(timeout=5000)
from playwright.sync_api import Page, expect


class ProjectPage:
    def __init__(self, page: Page):
        self.page = page

        # ===============================
        # Navigation
        # ===============================
        self.link_projects = page.get_by_role("link", name="Projects")
        self.btn_add_project = page.get_by_role("button", name="Project", exact=True)

        # ===============================
        # Project Form Fields
        # ===============================
        self.input_po_no = page.get_by_role("textbox", name="PO No.")
        self.input_project_name = page.get_by_role("textbox", name="Project Name")
        self.input_customer_name = page.get_by_role("textbox", name="Customer Name")

        self.pdc_date_picker = page.get_by_role("combobox", name="PDC Date")
        self.select_engineer = page.get_by_role(
            "combobox", name="Select Responsible Engineer"
        )

        # Product section
        self.select_product = page.locator("select")
        self.input_description = page.get_by_role("textbox", name="Description")
        self.input_qty = page.get_by_placeholder("Qty")
        self.btn_add_product = page.get_by_role("button", name="Product")

        self.input_remark = page.get_by_role(
            "textbox", name="Type your remark here"
        )

        self.btn_save = page.get_by_role("button", name="Save")

        self.toast_message = page.locator(
            ".toast-message, .p-toast-detail, .alert-success"
        )

    # ===============================
    # Actions
    # ===============================

    def open_add_project(self):
        self.link_projects.click()
        self.btn_add_project.click()

    def fill_basic_details(self, po_no, project_name, customer_name):
        self.input_po_no.fill(po_no)
        self.input_project_name.fill(project_name)
        self.input_customer_name.fill(customer_name)

    def select_pdc_date(self, day):
        self.pdc_date_picker.click()
        self.page.get_by_text(day, exact=True).click()

    def select_responsible_engineer(self, engineer_name):
        self.select_engineer.click()
        self.page.get_by_role("option", name=engineer_name).click()

    def add_first_product(self, product_id, description, qty):
        self.select_product.select_option(product_id)
        self.input_description.fill(description)
        self.input_qty.fill(qty)

    def add_second_product(self, product_id, product_name, description, qty):
        self.btn_add_product.click()

        self.page.get_by_role(
            "row", name="Select Product"
        ).get_by_role("combobox").select_option(product_id)

        self.page.get_by_role(
            "row", name=product_name
        ).get_by_placeholder("Description").fill(description)

        # ✅ FIX IS HERE (keyword argument)
        self.page.get_by_role(
            "row", name=f"{product_name} {description}"
        ).get_by_placeholder("Qty").fill(qty)

    def add_remark(self, remark):
        self.input_remark.fill(remark)

    def save_project(self):
        self.btn_save.click()

    # ===============================
    # Verification
    # ===============================

    def verify_project_created(self, project_name):
    # Wait a bit for backend response
     self.page.wait_for_timeout(2000)

    # Case 1: Success toast appears
     if self.toast_message.count() > 0:
        expect(self.toast_message).to_be_visible(timeout=5000)
        return

    # Case 2: Navigation to list page
     if "project-add" not in self.page.url:
        expect(self.page.get_by_text(project_name)).to_be_visible(timeout=5000)
        return

    # Case 3: Save failed – capture error
     raise AssertionError(
         f"Project creation failed. Still on page: {self.page.url}"
    )

