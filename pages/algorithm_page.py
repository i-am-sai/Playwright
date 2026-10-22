import re
from playwright.sync_api import expect
from pages.base_page import BasePage
from utils.logger import logger


class AlgorithmPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        self.listing_heading = page.locator("p.h5", has_text=re.compile(r"^\s*Algorithms \(\d+\)"))
        self.back_button = page.get_by_role("button", name="Go to back page")
        self.algorithm_items = page.locator("button.mediaListingImage")
        self.first_algorithm = self.algorithm_items.first

        # Preview page
        self.go_to_content_button = page.get_by_role("button", name="Go to Content")
        self.next_button = page.get_by_role("button", name="Next")
        self.previous_button = page.get_by_role("button", name="Previous")
        self.zoom_in_button = page.get_by_role("button", name="Zoom in")
        self.zoom_out_button = page.get_by_role("button", name="Zoom out")
        self.zoom_percentage = (
            page.get_by_text(re.compile(r"^\d+%$")).and_(page.locator(":visible"))
        )

        # Inside the algorithm iframe
        self.frame = page.frame_locator("iframe[title='Algorithm content']")
        self.long_description_link = self.frame.get_by_role(
            "link", name=re.compile("Read the long description")
        )
        self.algorithm_image = self.frame.get_by_role("img").first

    # --- listing page ---
    def verify_listing_heading(self, expected_count: int):
        logger.info(f"Verifying heading and {expected_count} algorithms")
        expect(self.listing_heading).to_have_text(re.compile(rf"Algorithms \({expected_count}\)"))

    def open_first_algorithm(self):
        logger.info("Opening first algorithm")
        self.first_algorithm.click()

    # --- preview page ---
    def verify_go_to_content_and_next(self):
        self._verify_ready(self.go_to_content_button, "Go to Content")
        self._verify_ready(self.next_button, "Next")

    def click_next_and_verify_previous(self):
        logger.info("Clicking Next and verifying Previous appears")
        self.next_button.click()
        self._verify_ready(self.previous_button, "Previous")

    def _zoom_percent(self) -> int:
        return int(self.zoom_percentage.inner_text().strip().rstrip("%"))

    def verify_zoom_controls(self):
        logger.info("Verifying zoom controls and percentage")
        expect(self.zoom_in_button).to_be_visible()
        expect(self.zoom_out_button).to_be_visible()
        expect(self.zoom_percentage).to_be_visible()

        # Starting state: 100% -> zoom out disabled, zoom in enabled
        expect(self.zoom_percentage).to_have_text("100%")
        expect(self.zoom_out_button).to_be_disabled()
        expect(self.zoom_in_button).to_be_enabled()

        # Zoom in -> percentage changes, zoom out becomes enabled
        self.zoom_in_button.click()
        expect(self.zoom_percentage).not_to_have_text("100%")
        expect(self.zoom_out_button).to_be_enabled()

        # Zoom out -> back to 100%, zoom out disabled again
        self.zoom_out_button.click()
        expect(self.zoom_percentage).to_have_text("100%")
        expect(self.zoom_out_button).to_be_disabled()

    def verify_description_and_image(self):
        logger.info("Verifying algorithm image and long description link")
        expect(self.algorithm_image).to_be_visible()
        expect(self.long_description_link).to_be_visible()

    # def verify_listing_descriptions(self):
    #     logger.info("Verifying each algorithm has a description")
    #     for i in range(self.algorithm_descriptions.count()):
    #         text = self.algorithm_descriptions.nth(i).inner_text().strip()
    #         assert text, f"Algorithm #{i} has an empty description"