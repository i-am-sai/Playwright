import pytest
from playwright.sync_api import expect
from pages.shelf_page import ShelfPage
from pages.reader_page import ReaderPage
from utils.config_reader import ConfigReader
from utils.logger import logger

def test_toc_navigation(logged_in_page):
    shelf = ShelfPage(logged_in_page)

    logger.info("\nTest Case 1: Chapter Navigation Verified")    

    shelf.capture_screenshot("New State after Login")
    shelf.open_bookshelf()
    reader = shelf.click_read_online()
    reader.verify_reader_loaded()
    reader.capture_screenshot("Reader Loaded")

    reader.open_table_of_contents()
    reader.capture_screenshot("TOC Loaded")
    reader.click_toc_chapter("Part 2")
    reader.capture_screenshot("TOC Chapter 2 Loaded")
    reader.verify_chapter_heading("Preparing for the Course")

    reader.capture_screenshot("chapter_2_loaded")


