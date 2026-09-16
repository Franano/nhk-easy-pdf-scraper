from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate_to(self, url: str):
        self.page.goto(url, wait_until="domcontentloaded")

    def get_text(self, selector: str) -> str:
        self.page.wait_for_selector(selector)
        return self.page.inner_text(selector).strip()

    def click_element(self, selector: str):
        self.page.wait_for_selector(selector)
        self.page.click(selector)