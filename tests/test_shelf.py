import pytest
from playwright.sync_api import expect
from pages.shelf_page import ShelfPage
from utils.config_reader import ConfigReader
from utils.logger import logger


def test_readerloading(logged_in_page):
   
    shelf = ShelfPage(logged_in_page)
    logger.info("\nTest Case 2: Shelf and Reader Loaded")    
    shelf.open_bookshelf()
    logger.info("Bookshelf Loaded")
    shelf.capture_screenshot("Bookshelf Loaded")
    reader = shelf.click_read_online()
    logger.info("Reader Loaded after click")
    reader.verify_reader_loaded()
    reader.capture_screenshot("Reader Loaded")
    reader.click_back_to_shelf()


def test_headless_check(page):
    resp = page.goto("https://aha-redesign.ipublishcentral.com/")
    print("status:", resp.status)
    print("UA:", page.evaluate("navigator.userAgent"))
    print("webdriver:", page.evaluate("navigator.webdriver"))
    print("title:", page.title())
    print(page.content()[:600])
    page.screenshot(path="headless.png", full_page=True)



