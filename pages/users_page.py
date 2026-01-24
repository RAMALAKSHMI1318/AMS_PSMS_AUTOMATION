from playwright.sync_api import Page, expect


class UserPage:

    def __init__(self, page: Page):
        self.page = page

        # ---------- Navigation ----------
        self.btn_user = page.get_by_role("button", name="User")

        # ---------- Form fields ----------
        self.input_employee_code = page.get_by_role(
            "textbox", name="Enter Employee Code"
        )
        self.input_full_name = page.get_by_role(
            "textbox", name="Enter Full Name"
        )
        self.dropdown_designation = page.get_by_role(
            "combobox", name="Select Designation"
        )
        self.dropdown_department = page.get_by_role(
            "combobox", name="Select Department"
        )

        self.input_office_number = page.get_by_role(
            "textbox", name="Enter Office Number", exact=True
        )
        self.input_mobile_number = page.get_by_role(
            "textbox", name="Enter mobile Number"
        )
        self.input_email = page.get_by_role(
            "textbox", name="Enter Email"
        )
        self.input_position = page.get_by_role(
            "textbox", name="Enter Position"
        )

        self.btn_save = page.get_by_role("button", name="Save")


        self.search_user_input = page.get_by_role(
            "textbox", name="Search Users"
        )

        self.edit_button = page.get_by_role(
            "button", name="edit_pic"
        )

    # ===============================
    # ACTIONS
    # ===============================
    def open_user_page(self):
        self.btn_user.click()

    def select_roles(self, roles: str):
     """
    PrimeNG p-multiSelect role selection
    - Supports single & multiple roles
    - Does NOT click checkbox
    - Uses ARIA role="option"
    """

    # 1️⃣ Open Roles dropdown (placeholder text)
     self.page.get_by_text("Select Role", exact=True).click()

    # 2️⃣ Split comma-separated roles from Excel
     role_list = [r.strip() for r in roles.split(",")]

     for role in role_list:
        option = self.page.get_by_role(
            "option",
            name=role,
            exact=True
        ).first

        # 3️⃣ Ensure visible & click option row
        option.scroll_into_view_if_needed()
        option.click()


    def fill_user_details(
        self,
        employee_code: str,
        full_name: str,
        designation: str,
        office_number: str,
        mobile_number: str,
        email: str,
        department: str,
        roles: str,
        position: str,
    ):
        self.input_employee_code.fill(employee_code)
        self.input_full_name.fill(full_name)

        # Designation (PrimeNG p-select)
        self.dropdown_designation.click()
        self.page.locator(
            'li[role="option"]',
            has_text=designation
        ).first.click()

        self.input_office_number.fill(office_number)
        self.input_mobile_number.fill(mobile_number)
        self.input_email.fill(email)

        # Department (PrimeNG p-select)
        self.dropdown_department.click()
        self.page.locator(
            'li[role="option"]',
            has_text=department
        ).first.click()

        # Roles (PrimeNG p-multiSelect)
        self.select_roles(roles)

        self.input_position.fill(position)

    def save(self):
        self.btn_save.click()

    def verify_user_created(self, full_name: str):
        expect(
            self.page.get_by_text(full_name).first
        ).to_be_visible(timeout=5000)

        
