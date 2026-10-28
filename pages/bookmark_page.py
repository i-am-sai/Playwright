from playwright.sync_api import expect
from pages.base_page import BasePage
from datetime import datetime
from utils.logger import logger

class BookmarkPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

        self.bookmark_button = page.get_by_role("button", name="bookmark", exact=True)
        self.bookmarked_button = page.get_by_role("button", name="bookmarked", exact=True)
        self.add_bookmark_button = page.locator("button.addBookmark", has_text="Add Bookmark")
        self.name_field = page.get_by_role("textbox", name="Bookmark Name")
        self.save_button = page.get_by_role("button", name="Save", exact=True)
        self.ok_button = page.get_by_role("button", name="OK", exact=True)
        self.go_to_bookmarks_button = page.get_by_role("button", name="Go To Bookmarks")

        # Listing page
        self.bookmark_cards = page.locator("div.booktextbox")

    def add_bookmark(self, bookmark_name: str):
        logger.info(f"Adding bookmark '{bookmark_name}'")
        self.bookmark_button.click()
        self.page.mouse.move(0, 300)
        self.add_bookmark_button.click()
        self.name_field.fill(bookmark_name)
        self.save_button.click()
        self.ok_button.click()
        self.refresh()
        

    def open_bookmark_listing(self):
        logger.info("Opening bookmark listing")
        self.bookmarked_button.click()
        self.go_to_bookmarks_button.click()

    def get_bookmark_card(self, bookmark_name: str):
        return self.bookmark_cards.filter(has_text=bookmark_name)

    def verify_bookmark_name(self, bookmark_name: str):
        logger.info(f"Verifying bookmark name '{bookmark_name}' in listing")
        card = self.get_bookmark_card(bookmark_name)
        expect(card.locator("a.bookmarktext")).to_have_text(bookmark_name)

    def verify_bookmark_date(self, bookmark_name: str):
        today = datetime.now().strftime("%b-%d-%Y")     # e.g. Oct-22-2026
        logger.info(f"Verifying bookmark date is {today}")
        card = self.get_bookmark_card(bookmark_name)
        expect(card.locator("span.px-0")).to_have_text(today)

    def refresh(self):
        logger.info("Reloading page to force fresh annotation state")
        self.page.reload()
        self.page.wait_for_load_state("networkidle")