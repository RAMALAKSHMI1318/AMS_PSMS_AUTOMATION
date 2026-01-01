import allure


class AllureHelper:

    @staticmethod
    def attach_description(tcid: str):
        allure.dynamic.title(tcid)
        allure.dynamic.description(f"Automation Test Case: {tcid}")

    @staticmethod
    def attach_text(name: str, text: str):
        allure.attach(text, name, allure.attachment_type.TEXT)

    @staticmethod
    def attach_screenshot(path: str):
        with open(path, "rb") as image:
            allure.attach(
                image.read(),
                name="Failure Screenshot",
                attachment_type=allure.attachment_type.PNG
            )
