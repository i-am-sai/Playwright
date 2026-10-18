from playwright.sync_api import expect
from pages.base_page import BasePage
from pages.reader_page import ReaderPage
from utils.logger import logger


class ShelfPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        
        self.automation_shelf = page.get_by_role("button", name="bookshelf; Automation Testing")
        #  self.default_shelf = page.get_by_role("button", name="bookshelf; Default Shelf")        Need to change locator for default shelf
       
        self.read_online_button = page.locator('a[href="/epubreader/basic-life-support-instructor-manual"][aria-label="Read Online"]') # BLS
        # self.read_online_button = page.locator('a[href="/epubreader/acls-provider-manual-ebook-individual"][aria-label="Read Online"]') # ACLS
        
        self.title_heading = page.get_by_role("heading",name="Basic Life Support Instructor")
        # self.title_heading = page.get_by_role("heading", name="Advanced Cardiovascular Life")
        

    def open_bookshelf(self):
        logger.info("Opening Bookshelf")
        self.automation_shelf.click()

    def click_read_online(self):     # Method to click read online and opening reader in new tab in same window
        self.capture_screenshot("shelf_before_scroll")
        logger.info("Scrolling to locate Read Online button")   
        self.scroll_infinite_page(self.read_online_button)

        logger.info("Opening book in Reader")
        with self.page.expect_popup() as popup_info:
            self.read_online_button.click()

        popup_page = popup_info.value # New Tab object
        popup_page.wait_for_load_state()
        return ReaderPage(popup_page)
   

    def verify_reader_loaded(self):
        logger.info("Verifying Reader loaded")
        expect(self.title_heading).to_be_visible()

    

       