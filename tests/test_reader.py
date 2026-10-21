import pytest
from playwright.sync_api import expect
from pages.shelf_page import ShelfPage
from pages.reader_page import ReaderPage
from utils.config_reader import ConfigReader
from utils.logger import logger


class TestReaderUI:

    def test_readerUI(self, reader_on_chapter):
        logger.info("\nTest Case 3: Reader UI Elements Verified")    
        # reader_on_chapter.verify_reader_loaded()
        reader_on_chapter.capture_screenshot("Reader Loaded")
        reader_on_chapter.verify_back_to_shelf_button()
        reader_on_chapter.verify_table_of_contents_button()
        reader_on_chapter.verify_all_reader_ui_elements()



