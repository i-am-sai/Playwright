import re # Python's built-in Regular Expression module.
from playwright.sync_api import expect
from pages.base_page import BasePage
from utils.logger import logger


class TOCPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        
        self.toc_button = page.get_by_role("button", name="table of contents")
        self.toc_search_button = page.get_by_role("button", name="search with value")
        # self.toc_search_field = page.get_by_placeholder("Search in Table of Contents")        
        self.toc_close_button = page.get_by_role("button", name="Close toc")
        self.toc_front_matter_link = page.get_by_role("link", name="Front Matter", exact=True)
        self.toc_algorithms_link = page.get_by_role("link",name=re.compile(r"^Algorithms \(\d+\)$"))       
        self.toc_figures_link = page.get_by_role("link", name=re.compile(r"^Figures \(\d+\)"))
        self.toc_accordion_toggles = page.get_by_role("heading").get_by_label("Toggle Accordion")

    
    # --- TOC verification ---
    def open_table_of_contents(self):
        logger.info("Opening Table of Contents")
        self.toc_button.click()


    def verify_toc_search(self):
        logger.info("Verifying TOC search field and search icon")
        # self._verify_ready(self.toc_search_field, "TOC Search Field")
        self._verify_ready(self.toc_search_button, "TOC Search Icon")

    def verify_toc_close_button(self):
        self._verify_ready(self.toc_close_button, "TOC Close Icon")

    def verify_toc_front_matter_link(self):
        self._verify_ready(self.toc_front_matter_link, "TOC Front Matter")

    def verify_toc_algorithms_link(self):
        self._verify_ready(self.toc_algorithms_link, "TOC Algorithms")
    
    def get_algorithms_count(self):
        text = self.toc_algorithms_link.inner_text()
        match = re.search(r"\((\d+)\)", text)
        return int(match.group(1))

    def verify_toc_figures_link(self):
        self._verify_ready(self.toc_figures_link, "TOC Figures")

    def get_figures_count(self):
        match = re.search(r"\((\d+)\)", self.toc_figures_link.inner_text())
        return int(match.group(1))

    def verify_toc_chapter_accordions(self):
        logger.info("Verifying TOC chapter accordions are present")
        expect(self.toc_accordion_toggles.first).to_be_visible()
        assert self.toc_accordion_toggles.count() > 0, "No chapter accordions found in TOC"

    def verify_toc_accordion_expands(self, chapter_heading: str, child_link: str):
        """Expands a chapter accordion and verifies one of its child links appears."""
        logger.info(f"Expanding accordion '{chapter_heading}' and checking '{child_link}'")
        self.page.get_by_role("heading", name=chapter_heading).get_by_label("Toggle Accordion").click()
        expect(self.page.get_by_role("link", name=child_link)).to_be_visible()

    def verify_toc_closes(self):
        logger.info("Closing TOC and verifying it is gone")
        self.toc_close_button.click()
        expect(self.toc_close_button).to_be_hidden()

    def verify_all_toc_ui_elements(self):
        checks = {
            "Search field/icon": self.verify_toc_search,
            "Close icon": self.verify_toc_close_button,
            "Front Matter": self.verify_toc_front_matter_link,
            "Algorithms": self.verify_toc_algorithms_link,
            "Figures": self.verify_toc_figures_link,
            "Chapter accordions": self.verify_toc_chapter_accordions,
        }
        failures = []
        for name, check in checks.items():
            try:
                check()
            except AssertionError as e:
                failures.append(f"{name}: " + " | ".join(str(e).splitlines()[:6]))
        assert not failures, "TOC UI elements failed:\n" + "\n".join(failures)