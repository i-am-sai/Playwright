from playwright.sync_api import expect
from utils.screenshot_helper import take_screenshot
from utils.logger import logger

class BasePage:
    def __init__(self, page): # Constructor, page → Playwright Page object.
        self.page = page # Stores the page so every method can use it.
        self.accept_cookies_button = page.locator("#onetrust-accept-btn-handler") # Locator for accept cookies pop up


    def navigate(self, url): # Method to navigate to particulat url
        self.page.goto(url)

    def accept_cookies(self): # Method to accept cookies when popped up
        try:
            self.accept_cookies_button.click(timeout=5000)
        except Exception:
            pass  # banner didn't appear, nothing to do
    
    def capture_screenshot(self, name): # Generic screenshot method available to every page.
        take_screenshot(self.page, name)

    def scroll_infinite_page(self, locator, max_attempts=30, scroll_amount=1000): # To Scroll till element is visible for actions
        previous_height = 0

        for attempt in range(max_attempts):
            if locator.count() > 0 and locator.first.is_visible():
                logger.info(f"Target element found after {attempt} scroll(s)")
                return

            self.page.mouse.wheel(0, scroll_amount)
            self.page.wait_for_timeout(1000)

            current_height = self.page.evaluate("document.body.scrollHeight")
            logger.info(f"Scroll attempt {attempt}: page height = {current_height}")
            
            if current_height == previous_height:
                logger.info("Reached bottom of page, no more content loading")
                break
            previous_height = current_height

        raise Exception(
            f"Target element never appeared after {max_attempts} scroll attempts. "
            f"Final page height: {previous_height}"
        )
    
    def _verify_ready(self, locator, name: str):
        logger.info(f"Verifying '{name}' is visible and enabled")
        expect(locator).to_be_visible()
        expect(locator).to_be_enabled()


# ✅ Keep only generic methods here.
# ✅ All page classes should inherit BasePage.
# ✅ Reuse helpers instead of duplicating code.







# class BasePage:
#     def __init__(self, page):
#         self.page = page

#     def navigate(self, url):
#         self.page.goto(url)