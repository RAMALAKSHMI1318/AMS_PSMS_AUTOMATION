from playwright.sync_api import Page, expect


class MachinesPage:

    def __init__(self, page: Page):
        self.page = page

        # ---------- Navigation ----------
        self.tab_machines = page.get_by_role("tab", name="Machines")
        self.btn_add_machine = page.get_by_role("button", name="Add Machine")

        # ---------- Add Machine form ----------
        # NOTE: nth() used because codegen gave it – can be improved later
        self.input_machine_code = page.get_by_role("textbox").nth(1)
        self.input_machine_name = page.get_by_role("textbox").nth(2)
        self.input_serial_number = page.get_by_role("textbox").nth(3)
        self.input_capacity = page.get_by_role("spinbutton")
        self.input_location = page.get_by_role("textbox").nth(4)

        self.tab_machines = page.get_by_role("tab", name="Machines")

        # ---------- Search ----------
        self.input_search_machine = page.get_by_role(
            "textbox", name="Search Machines"
        )


        self.btn_status_dropdown = page.get_by_label(
            "Add Machine"
        ).get_by_role("button", name="dropdown trigger")

        self.btn_save = page.get_by_role("button", name="Save")

        self.toast_message = page.locator(
            ".toast-message, .p-toast-detail, .alert-success"
        )

    def open_machines_tab(self):
        """Navigate to Machines tab"""
        self.tab_machines.click()

    def open_add_machine(self):
        """Navigate to Machines tab and open Add Machine dialog"""
        self.tab_machines.click()
        self.btn_add_machine.click()

    def enter_machine_details(
        self,
        code: str,
        name: str,
        serial: str,
        qty: str,
        location: str,
    ):
        """Fill machine form fields"""
        self.input_machine_code.fill(code)
        self.input_machine_name.fill(name)
        self.input_serial_number.fill(serial)
        self.input_capacity.fill(qty)
        self.input_location.fill(location)

    def select_status_by_index(self, index: int):
        """Select status from dropdown using index (Excel-driven)"""
        self.btn_status_dropdown.click()
        self.page.get_by_role("option").nth(index).click()

    def save(self):
        """Click Save button"""
        self.btn_save.click()


    def verify_machine_created(self, machine_name: str):
        try:
            expect(self.toast_message).to_be_visible(timeout=5000)
        except Exception:
            # fallback verification in grid/table
            expect(
                self.page.get_by_text(machine_name)
            ).to_be_visible(timeout=5000)


    def search_machine(self, machine_name: str):
        """Search machine by name"""
        self.input_search_machine.click()
        self.input_search_machine.fill(machine_name)

    def verify_machine_search_result(self, machine_name: str):
        """Verify machine appears in search result (strict-mode safe)"""
        expect(
            self.page.get_by_role("cell", name=machine_name).first
        ).to_be_visible(timeout=5000)


    def click_edit_first_machine(self):
        self.page.get_by_role("button").nth(1).click()

    def update_machine_code(self, new_code: str):
        
        code_input = self.page.get_by_role("textbox").nth(1)
        code_input.click()
        code_input.fill(new_code)

    def update_location(self, location: str):
        location_input = self.page.get_by_role("textbox").nth(4)
        location_input.click()
        location_input.fill(location)

    def save_updated_machine(self):
        self.page.get_by_role("button", name="Save").click()

    def verify_machine_updated(self, updated_code: str):
        expect(
            self.page.get_by_role("cell", name=updated_code).first
        ).to_be_visible(timeout=5000)

    def delete_first_machine(self):
        
        self.page.get_by_role("button").nth(2).click()

        self.page.get_by_role("button", name="Yes").click()

    def verify_machine_deleted(self, search_text: str):
        
        grid_cell = self.page.get_by_role(
            "cell", name=search_text
        )

        expect(grid_cell).to_have_count(0)

