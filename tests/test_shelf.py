import pytest
from playwright.sync_api import expect
from pages.shelf_page import ShelfPage
from utils.config_reader import ConfigReader
from utils.logger import logger

@pytest.mark.smoke
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






