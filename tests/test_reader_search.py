import pytest
from utils.logger import logger
from pages.reader_search_page import ReaderSearchPage


class TestReaderSearch:

  
    def test_search_result_shows_highlight_snippet_and_chapter(self, reader_search_page):
        logger.info("\nTest Case 5: Reader Search Result Verified")
        reader_search_page.search_for("Heart")
        reader_search_page.capture_screenshot("Search Results")
        reader_search_page.verify_first_result("Heart") 

