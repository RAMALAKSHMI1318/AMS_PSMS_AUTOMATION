from pathlib import Path
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
    # COMMON TREE
    # ===============================
    def open_project_tree(self):
        self.page.get_by_role("button", name="itemDetails").click()
        self.page.get_by_role("tree").wait_for(state="visible", timeout=10000)

    # ===============================
    # ADD PROJECT – PRJ_01
    # ===============================
    def open_add_project(self):
        self.link_projects.click()
        self.btn_add_project.click()

    def fill_basic_details(self, po_no, project_name, customer_name):
        self.input_po_no.fill(str(po_no))
        self.input_project_name.fill(project_name)
        self.input_customer_name.fill(customer_name)

    def select_pdc_date(self, day):
        self.pdc_date_picker.click()
        self.page.get_by_text(str(day), exact=True).click()

    def select_responsible_engineer(self, engineer_name):
        self.select_engineer.click()
        self.page.get_by_role("option", name=engineer_name).click()

    def add_first_product(self, product_id, description, qty):
      product_id = str(product_id)

    # ✅ Wait for select itself (not option)
      expect(self.select_product).to_be_enabled(timeout=10000)

    # ✅ Select by value (native dropdown)
      self.select_product.select_option(product_id)

      self.input_description.fill(description)
      self.input_qty.fill(str(qty))


    def add_second_product(self, product_id, product_name, description, qty):
        self.btn_add_product.click()

        self.page.get_by_role(
            "row", name="Select Product"
        ).get_by_role("combobox").select_option(str(product_id))

        self.page.get_by_role(
            "row", name=product_name
        ).get_by_placeholder("Description").fill(description)

        self.page.get_by_role(
            "row", name=f"{product_name} {description}"
        ).get_by_placeholder("Qty").fill(str(qty))

    def add_remark(self, remark):
        self.input_remark.fill(remark)

    def save_project(self):
      self.btn_save.scroll_into_view_if_needed()
      expect(self.btn_save).to_be_enabled()
      self.btn_save.click()

    # ✅ wait for backend save / UI settle
      self.page.wait_for_timeout(2000)
    def verify_project_row(
    self,
    project_name: str,
    po_no: str,
    customer_name: str,
    status: str = "PROCESSING",
):
    # Go to Project List
         self.page.get_by_role("link", name="Projects").click()

    # Wait for table
         self.page.wait_for_selector("table", timeout=15000)

    # ✅ Locate row by project name text
         row = self.page.locator("tr", has_text=project_name)

         expect(row).to_be_visible(timeout=15000)

    # ✅ Column validations (exactly like UI)
         expect(row.get_by_text(project_name, exact=True)).to_be_visible()
         expect(row.get_by_text(po_no, exact=True)).to_be_visible()
         expect(row.get_by_text(customer_name, exact=True)).to_be_visible()
         expect(row.get_by_text(status, exact=True)).to_be_visible()


    # ===============================
    # EDIT PROJECT – PRJ_02
    # ===============================
    def open_edit_project(self):
        self.page.get_by_role("button", name="edit_project").click()

    def update_pdc_date(self, day):
        self.page.get_by_role("combobox", name="PDC Date").click()
        self.page.get_by_text(day).nth(1).click()

    def update_customer_name(self, customer_name):
        self.input_customer_name.fill(customer_name)

    def update_remark(self, remark):
        self.input_remark.fill(remark)

    def update_project(self):
        self.btn_update.scroll_into_view_if_needed()
        expect(self.btn_update).to_be_enabled()
        self.btn_update.click()

    # ===============================
    # TREE – PRJ_03
    # ===============================
    def expand_tree_using_exact_locators(self, nodes: list[str]):
        for node in nodes:
            tree_item = self.page.get_by_role("treeitem", name=node)

            try:
                tree_item.get_by_role("button").click(timeout=3000)
            except:
                pass

            try:
                tree_item.locator("span.p-treenode-label").click()
            except:
                pass

    # ===============================
    # TREE – PRJ_04 (ADD PRODUCT)
    # ===============================
    def right_click_on_project_node(self, project_name: str):
        self.page.locator(
            "span.p-treenode-label", has_text=project_name
        ).first.click(button="right")

    def click_add_product_from_context(self):
        self.page.get_by_role("button", name="➕ Product").click()

    def fill_product_details(
        self,
        product_name: str,
        delivery_day: str,
        quantity: str,
        unit: str,
        remarks: str,
        file_path: str,
    ):
        self.page.get_by_role("combobox", name="Select Product").click()
        self.page.get_by_text(product_name).click()

        self.page.get_by_role(
            "combobox", name="Planned Delivery Date"
        ).click()
        self.page.get_by_text(delivery_day).nth(1).click()

        self.page.get_by_placeholder("Quantity").fill(quantity)
        self.page.get_by_role("textbox", name="Unit").fill(unit)
        self.page.get_by_role(
            "textbox", name="Type your remarks here"
        ).fill(remarks)

        if file_path:
            self.page.locator("input[type=file]").set_input_files(file_path)

    def save_product(self):
        self.page.get_by_role("button", name="Save").click()

    # ===============================
    # PRJ_05 – ADD MILESTONE
    # ===============================
    def expand_strategic_project_tracking(self):
        node = self.page.get_by_role(
            "treeitem",
            name="Strategic Project Tracking System"
        )
        expect(node).to_be_visible(timeout=10000)
        node.get_by_role("button").click()

    def right_click_mission_project_tracking(self):
        self.page.get_by_role(
            "treeitem",
            name="Mission Project Tracking"
        ).locator("span").first.click(button="right")

    def click_add_milestone_from_context(self):
        self.page.get_by_role("button", name="➕ Milestone").click()
        self.page.get_by_role("dialog").wait_for(state="visible", timeout=5000)

    def fill_milestone_details(
        self,
        milestone_name,
        start_day,
        end_day,
        remarks,
        file_path=None,
    ):
        self.page.get_by_role(
            "textbox", name="Milestone Name"
        ).fill(milestone_name)

        self.page.get_by_role(
            "combobox", name="Milestone Start Date"
        ).click()
        self.page.get_by_text(start_day, exact=True).click()

        self.page.get_by_role(
            "combobox", name="Milestone End Date"
        ).click()
        self.page.get_by_text(end_day, exact=True).click()

        self.page.get_by_role(
            "textbox", name="Type your remarks here"
        ).fill(remarks)

        if file_path:
         self.page.locator("input[type=file]").set_input_files(file_path)
    def save_milestone(self):
        self.page.get_by_role("button", name="Save").click()


    # ===============================
# PRJ_06 – ADD TASK FROM TREE
# ===============================

    def expand_strategic_project_tracking(self):
     node = self.page.get_by_role(
        "treeitem",
        name="Strategic Project Tracking"
    )
     expect(node).to_be_visible(timeout=10000)
     node.get_by_role("button").click()


    def expand_mission_project_tracking(self):
     node = self.page.get_by_role(
        "treeitem",
        name="Mission Project Tracking"
    )
     expect(node).to_be_visible(timeout=10000)
     node.get_by_role("button").click()
  


    def right_click_phase_node(self, phase_name: str):
     self.page.locator(
        "span", has_text=phase_name
    ).first.click(button="right")


    def click_add_task_from_context(self):
     self.page.get_by_role("button", name="➕ Task").click()
     self.page.get_by_role("dialog").wait_for(
        state="visible", timeout=5000
    )


    def fill_task_details(
    self,
    task_name: str,
    priority: str,
    complexity: str,
    remarks: str,
    file_path: str,
):
     self.page.get_by_role(
        "textbox", name="Task Name"
    ).fill(task_name)

    # Priority
     self.page.get_by_role(
        "combobox", name="Task Priority"
    ).click()
     self.page.get_by_role(
        "option", name=priority
    ).click()

    # Complexity
     self.page.get_by_role(
        "combobox", name="Task Complexity"
    ).click()
     self.page.get_by_label(
        "Option List"
    ).get_by_text(complexity, exact=True).click()

     self.page.get_by_role(
        "textbox", name="Type your remarks here"
    ).fill(remarks)

     if file_path:
        self.page.locator(
            "input[type=file]"
        ).set_input_files(file_path)



    def save_task(self):
     self.page.get_by_role(
        "button", name="Save"
    ).click()

    # ===============================
    # PRJ_07 – ADD SUBTASK FROM TREE
    # ===============================

    def expand_phase_node(self, phase_name: str):
     node = self.page.get_by_role(
        "treeitem",
        name=phase_name
    )
     expect(node).to_be_visible(timeout=10000)
     node.get_by_role("button").click()


    def right_click_task_node(self, task_name: str):
     self.page.locator(
        "span", has_text=task_name
    ).first.click(button="right")


    def click_add_subtask_from_context(self):
     self.page.get_by_role("button", name="➕ Subtask").click()
     self.page.get_by_role("dialog").wait_for(
        state="visible", timeout=5000
    )


    def fill_subtask_details(
    self,
    subtask_name: str,
    start_day: str,
    end_day: str,
    assign_to: str,
    assignee: str,
    shift: str,
    priority: str,
    complexity: str,
    remarks: str,
    file_path: str,
):
     self.page.get_by_role(
        "textbox", name="Subtask Name"
    ).fill(subtask_name)

    # Start Date
     self.page.get_by_role(
        "combobox", name="Subtask Start Date"
    ).click()
     self.page.get_by_text(start_day, exact=True).click()

    # End Date
     self.page.get_by_role(
        "combobox", name="Subtask End Date"
    ).click()
     self.page.get_by_text(end_day, exact=True).click()

    # Assign To
     self.page.get_by_role(
        "combobox", name="Assign To"
    ).click()
     self.page.get_by_text(assign_to, exact=True).click()

    # Assignee Name
     self.page.get_by_role(
        "combobox", name="Assignee Name"
    ).click()
     self.page.get_by_text(assignee, exact=True).click()

    # Shift
     self.page.get_by_role(
        "combobox", name="Shift"
    ).click()
     self.page.get_by_text(shift, exact=True).click()

    # Priority
     self.page.get_by_role(
        "combobox", name="Task Priority"
    ).click()
     self.page.get_by_text(priority, exact=True).click()

    # Complexity (PrimeNG)
     self.page.get_by_role(
        "combobox", name="Task Complexity"
    ).click()
     self.page.get_by_label(
        "Option List"
    ).get_by_text(complexity, exact=True).click()

    # Remarks
     self.page.get_by_role(
        "textbox", name="Type your remarks here"
    ).fill(remarks)

    # File upload (same logic as Product / Milestone / Task)
     if file_path:
        self.page.locator(
            "input[type=file]"
        ).set_input_files(file_path)


    def save_subtask(self):
     self.page.get_by_role(
        "button", name="Save"
    ).click()
     
    # ===============================
# PRJ_08 – ADD WORKLOG FROM TREE
# ===============================

    def expand_task_node(self, task_name: str):
     node = self.page.get_by_role(
        "treeitem",
        name=task_name
    )
     expect(node).to_be_visible(timeout=10000)
     node.get_by_role("button").click()


    def right_click_subtask_node(self, subtask_name: str):
     self.page.locator(
        "span", has_text=subtask_name
    ).first.click(button="right")


    def click_add_worklog_from_context(self):
     self.page.get_by_role("button", name="➕ Worklog").click()
     self.page.get_by_role("dialog").wait_for(
        state="visible", timeout=5000
    )


    def fill_worklog_details(
    self,
    worklog_day: str,
    time_spent: str,
    work_description: str,
    remarks: str,
    file_path: str,
):
    # Worklog date
     self.page.get_by_role(
        "combobox", name="Select worklog date"
    ).click()
     self.page.get_by_text(worklog_day, exact=True).click()

    # Time spent
     self.page.get_by_placeholder(
        "Time Spent (hrs)"
    ).fill(time_spent)

    # Work description
     self.page.get_by_role(
        "textbox", name="Work Description"
    ).fill(work_description)

    # Remarks
     self.page.get_by_role(
        "textbox", name="Type your remarks here"
    ).fill(remarks)

    # File upload (same logic as Product / Milestone / Task / Subtask)
     if file_path:
        self.page.locator(
            "input[type=file]"
        ).set_input_files(file_path)


    def save_worklog(self):
     self.page.get_by_role(
        "button", name="Save"
    ).click()


