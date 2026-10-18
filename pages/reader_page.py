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

    def verify_reader_loaded(self):
        logger.info("Verifying Reader loaded")
        expect(self.title_heading).to_be_visible()
    
    def click_back_to_shelf(self):
        logger.info("Returning to Shelf")
        self.back_to_shelf.click()
    
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