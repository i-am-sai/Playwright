import pytest
from datetime import datetime
from utils.logger import logger
from pages.bookmark_page import BookmarkPage


class TestBookmark:
    
    def test_add_bookmark_and_verify_in_listing(self, reader_on_chapter, bookmark_page):
        logger.info("\nTest Case 8: Bookmark Added and Listed")
        reader_on_chapter.open_table_of_contents()
        reader_on_chapter.click_toc_chapter("Part 4")
        reader_on_chapter.verify_chapter_heading("Testing")

        name = f"Test{datetime.now().strftime('%H%M%S')}"

        bookmark_page.add_bookmark(name)
        bookmark_page.open_bookmark_listing()
        bookmark_page.capture_screenshot("Bookmark Listing")

        bookmark_page.verify_bookmark_name(name)
        bookmark_page.verify_bookmark_date(name)