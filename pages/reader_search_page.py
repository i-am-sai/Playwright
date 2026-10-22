from playwright.sync_api import expect
from pages.base_page import BasePage
from utils.logger import logger

class ReaderSearchPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        self.search_button = page.get_by_role("button", name="search in reader")
        self.search_field = page.locator("input[placeholder='Search']:visible")
        self.results = page.locator("div.showtext")

    def search_for(self, term: str):
        logger.info(f"Searching reader for '{term}'")
        self.search_button.click()
        self.search_field.fill(term)
        expect(self.results.first).to_be_visible(timeout=15000)

    def verify_first_result(self, term: str):
        result = self.results.first

        logger.info("Verifying highlighted term")
        expect(result.locator("span.selectedsearch").first).to_have_text(term, ignore_case=True)

        logger.info("Verifying snippet text")
        expect(result.locator("a.results")).to_contain_text(term, ignore_case=True)

        logger.info("Verifying chapter name")
        expect(result.locator("p.chapterName")).to_contain_text("Chapter Name:")