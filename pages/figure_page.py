import re
from playwright.sync_api import expect
from pages.base_page import BasePage
from utils.logger import logger


class FigurePage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        # Listing page
        self.listing_heading = page.locator("p.h5", has_text=re.compile(r"Figures \(\d+\)"))
        self.back_button = page.get_by_role("button", name="Go to back page")
        self.figure_items = page.locator("button.mediaListingImage")
        self.first_figure = self.figure_items.first

        # Preview page
        self.go_to_content_button = page.get_by_role("button", name="Go to Content")
        self.next_button = page.get_by_role("button", name="Next")
        self.previous_button = page.get_by_role("button", name="Previous")
        self.zoom_in_button = page.get_by_role("button", name="Zoom in")
        self.zoom_out_button = page.get_by_role("button", name="Zoom out")
        self.zoom_percentage = (
            page.get_by_text(re.compile(r"^\d+%$")).and_(page.locator(":visible"))
        )

        

    # --- listing page ---
    def verify_listing_heading(self, expected_count: int):
        logger.info(f"Verifying Figures heading and {expected_count} figures")
        expect(self.listing_heading).to_have_text(re.compile(rf"Figures \({expected_count}\)"))
        expect(self.figure_items).to_have_count(expected_count)

    def open_first_figure(self):
        logger.info("Opening first figure")
        self.first_figure.click()

    # --- preview page ---
    def verify_go_to_content_and_next(self):
        self._verify_ready(self.go_to_content_button, "Go to Content")
        self._verify_ready(self.next_button, "Next")

    def click_next_and_verify_previous(self):
        logger.info("Clicking Next and verifying Previous appears")
        self.next_button.click()
        self._verify_ready(self.previous_button, "Previous")

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