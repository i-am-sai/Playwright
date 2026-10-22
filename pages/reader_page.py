import re # Python's built-in Regular Expression module.
from playwright.sync_api import expect
from pages.base_page import BasePage
from utils.logger import logger


class ReaderPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        self.epub_frame = page.frame_locator('iframe[title="EPUB Book Content"]')
        self.toc_button = page.get_by_role("button", name="table of contents")  
        self.title_heading = page.get_by_role("heading",name="Basic Life Support Instructor")
        self.back_to_shelf = page.get_by_role("button",name="back to shelf")
        self.title_content = page.locator("iframe[title=\"EPUB Book Content\"]").content_frame.get_by_text("Preparing for the Course")
       
        self.reader_search_button = page.get_by_role("button", name="search in reader")
        self.annotation_listing_button = page.get_by_role("button", name="annotation listing")
        self.bookmark_button = page.get_by_role("button", name="bookmark")
        self.brightness_button = page.get_by_role("button", name="Brightness control")
        self.theme_toggle_button = page.get_by_role("button", name="toggle light or dark mode")
        self.text_size_button = page.get_by_role("button", name="text size control")
        self.scroll_mode_button = page.get_by_role("button", name="switch to scroll")
        self.fullscreen_button = page.get_by_role("button", name="switch to fullscreen mode")

        self.seek_bar = page.locator("#sliderContainer").get_by_role("slider").first
        self.seek_bar_label = page.locator("#sliderContainer").get_by_text(re.compile(r"^Part \d+")).first
        self.seek_bar_percentage = page.locator("label.seekbarlabel span.ml-1")
    

    def open_table_of_contents(self):
        logger.info("Opening Table of Contents")
        self.toc_button.click()

    def click_toc_chapter(self, chapter_name):
        logger.info(f"Navigating to chapter: {chapter_name}")
        self.page.get_by_role("link", name=re.compile(chapter_name)).click()

    def verify_chapter_heading(self, heading_text):
        logger.info(f"Verifying heading visible in EPUB: {heading_text}")
        heading = self.epub_frame.locator(".partn2", has_text=heading_text)
        expect(heading).to_be_visible()

    # Verify Reader Loading 
    def verify_reader_loaded(self):
        logger.info("Verifying Reader loaded")
        expect(self.title_heading).to_be_visible()
    
    # Verifying Reader UI Elements

    def verify_back_to_shelf_button(self):
        logger.info("Verifying 'Back to Shelf' button is visible")
        expect(self.back_to_shelf).to_be_visible()

    def verify_table_of_contents_button(self):
        logger.info("Verifying 'Table of Contents' button is visible")
        expect(self.toc_button).to_be_visible()
    
    def click_back_to_shelf(self):
        logger.info("Returning to Shelf")
        self.back_to_shelf.click()
    
    def verify_title_heading(self):
        logger.info("Verifying book title heading is visible")
        expect(self.title_heading).to_be_visible()

    def verify_reader_search_button(self):
        logger.info("Verifying Reader Search button is visible and enabled")
        expect(self.reader_search_button).to_be_visible()
        expect(self.reader_search_button).to_be_enabled()

    def verify_annotation_listing_button(self):
        logger.info("Verifying Annotation Listing button is visible and enabled")
        self._verify_ready(self.annotation_listing_button, "Annotation Listing")

    def verify_bookmark_button(self):
        logger.info("Verifying Bookmark button is visible and enabled")
        self._verify_ready(self.bookmark_button, "Bookmark")

    def verify_brightness_button(self):
        self._verify_ready(self.brightness_button, "Brightness Control")

    def verify_theme_toggle_button(self):
        self._verify_ready(self.theme_toggle_button, "Light/Dark Mode Toggle")

    def verify_text_size_button(self):
        self._verify_ready(self.text_size_button, "Text Size Control")

    def verify_scroll_mode_button(self):
        self._verify_ready(self.scroll_mode_button, "Swipe/Scroll Switch")

    def verify_fullscreen_button(self):
        self._verify_ready(self.fullscreen_button, "Fullscreen Mode")

    def verify_seek_bar(self):
        self._verify_ready(self.seek_bar, "Seek Bar")

    def verify_seek_bar_label(self):
        logger.info("Verifying seek bar label is visible")
        expect(self.seek_bar_label).to_be_visible()

    def verify_seek_bar_percentage(self):
        logger.info("Verifying seek bar percentage is visible and formatted")
        expect(self.seek_bar_percentage).to_be_visible()
        expect(self.seek_bar_percentage).to_have_text(re.compile(r"^\s*\d+%\s*$"))

    def verify_chapter_content(self, paragraph_id: str):
        """Confirms a specific paragraph (by DOM id) is present and visible in the loaded chapter."""
        
        logger.info(f"Verifying chapter content — checking for paragraph #{paragraph_id}")
        frame = self.page.locator("iframe[title='EPUB Book Content']").content_frame

        # Wait for the frame body to be ready before checking specific content
        frame.locator("body").wait_for(state="visible", timeout=10000)

        paragraph = frame.locator(f"#{paragraph_id}")
        expect(paragraph).to_be_visible(timeout=10000)

        logger.info(f"Paragraph #{paragraph_id} confirmed visible")
        return paragraph

 # """Checks every element and reports ALL failures together instead of stopping at the first."""
    def verify_all_reader_ui_elements(self):
        checks = {
            "Title heading": self.verify_title_heading,
            "Back to Shelf": self.verify_back_to_shelf_button,
            "Table of Contents": self.verify_table_of_contents_button,
            "Reader search": self.verify_reader_search_button,
            "Annotation listing": self.verify_annotation_listing_button,
            "Bookmark": self.verify_bookmark_button,
            "Brightness": self.verify_brightness_button,
            "Theme toggle": self.verify_theme_toggle_button,
            "Text size": self.verify_text_size_button,
            "Scroll mode": self.verify_scroll_mode_button,
            "Fullscreen": self.verify_fullscreen_button,
            "Seek bar": self.verify_seek_bar,
            "Seek bar label": self.verify_seek_bar_label,
            "Seek bar percentage": self.verify_seek_bar_percentage,
        }
        failures = []
        for name, check in checks.items():
            try:
                check()
            except AssertionError:
                failures.append(name)
        assert not failures, f"Reader UI elements failed: {failures}"