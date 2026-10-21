import pytest
from playwright.sync_api import expect
from pages.shelf_page import ShelfPage
from pages.reader_page import ReaderPage
from utils.config_reader import ConfigReader
from utils.logger import logger


class TestTableOfContents:
    
    @pytest.mark.dev
    def test_toc_ui_elements(self, reader_on_chapter):
        logger.info("\nTest Case 4: Table of Contents UI Elements Verified")    
        reader_on_chapter.capture_screenshot("Reader Loaded")
        reader_on_chapter.verify_table_of_contents_button()
        reader_on_chapter.open_table_of_contents()
        reader_on_chapter.capture_screenshot("TOC Loaded")


  
    def test_toc_navigation(self, reader_on_chapter):
        logger.info("\nTest Case 5: Table of Contents Navigation")
        reader.open_table_of_contents()
        reader.capture_screenshot("TOC Loaded")
        reader.click_toc_chapter("Part 2")
        reader.capture_screenshot("TOC Chapter 2 Loaded")
        reader.verify_chapter_heading("Preparing for the Course")
        reader.capture_screenshot("chapter_2_loaded")



