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

        self.select_product = page.locator("select")
        self.input_description = page.get_by_role("textbox", name="Description")
        self.input_qty = page.get_by_placeholder("Qty")
        self.btn_add_product = page.get_by_role("button", name="Product")

        self.input_remark = page.get_by_role(
            "textbox", name="Type your remark here"
        )

        self.btn_save = page.get_by_role("button", name="Save")
        self.btn_update = page.get_by_role("button", name="Update")

        self.toast_message = page.locator(
            ".toast-message, .p-toast-detail, .alert-success"
        )

    # ===============================
    # ADD PROJECT
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
        self.page.get_by_role("treeitem", name="Select Product")

        self.page.get_by_role(
            "row", name="Select Product"
        ).get_by_role("combobox").select_option(product_id)

        self.page.get_by_role(
            "row", name=product_name
        ).get_by_placeholder("Description").fill(description)

        self.page.get_by_role(
            "row", name=f"{product_name} {description}"
        ).get_by_placeholder("Qty").fill(qty)

    def add_remark(self, remark):
        self.input_remark.fill(remark)

    def save_project(self):
        self.btn_save.scroll_into_view_if_needed()
        expect(self.btn_save).to_be_enabled()
        self.btn_save.click()

    # ===============================
    # EDIT PROJECT
    # ===============================
    def open_edit_project(self):
        self.page.get_by_role("button", name="edit_project").click()

    def update_pdc_date(self, day):
        self.page.get_by_role("combobox", name="PDC Date").click()
        self.page.get_by_text(day).nth(1).click()

    def update_customer_name(self, customer_name):
        self.input_customer_name.click()
        self.input_customer_name.fill(customer_name)

    def update_remark(self, remark):
        self.input_remark.click()
        self.input_remark.fill(remark)

    def update_project(self):
        self.btn_update.scroll_into_view_if_needed()
        expect(self.btn_update).to_be_enabled()
        self.btn_update.click()

    # ===============================
    # TREE – PRJ_03 (EXACT LOCATORS)
    # ===============================
    def open_project_tree(self):
        self.page.get_by_role("button", name="itemDetails").click()

    def expand_tree_using_exact_locators(self, nodes: list[str]):
        """
        Expand tree by navigating through nodes.
        For each node:
        1. Try to click the expand button (if it exists)
        2. Click the label to select/navigate the node
        """
        for node in nodes:
            # Try to click expand button if it exists
            try:
                expand_button = self.page.get_by_role("treeitem", name=node).get_by_role("button")
                if expand_button.count() > 0:
                    expand_button.click(timeout=3000)
                    self.page.wait_for_timeout(300)
            except:
                # No button or timeout - this is likely a leaf node, continue
                pass
            
            # Click the label/text to navigate or select the node
            # Handle both partial and full text matches
            try:
                self.page.get_by_label(node).get_by_text(node).click()
            except:
                # If get_by_label fails, try direct text click
                self.page.get_by_text(node, exact=True).click()
            
            self.page.wait_for_timeout(300)

    def verify_tree_expanded(self):
        """
        Verify that the tree has been expanded.
        Simply checks that at least one tree item is visible.
        """
        tree_item = self.page.get_by_role("treeitem").first
        expect(tree_item).to_be_visible(timeout=5000)

    # ===============================
    # VERIFICATION
    # ===============================
    def verify_project_created(self, project_name):
        self.page.wait_for_timeout(2000)

        if self.toast_message.count() > 0:
            expect(self.toast_message).to_be_visible(timeout=5000)
            return

        self.link_projects.click()
        project_row = self.page.get_by_role(
            "row", name=lambda t: project_name.lower() in t.lower()
        )
        expect(project_row).to_be_visible(timeout=5000)
