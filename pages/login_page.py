from playwright.sync_api import expect
from pages.base_page import BasePage
from utils.logger import logger
from utils.config_reader import ConfigReader

class LoginPage(BasePage):

    def __init__(self, page):
        super().__init__(page) ## runs BasePage.__init__, sets self.page and self.accept_cookies_button
        
        config = ConfigReader() # object
        self.login_link = page.get_by_role("link", name="Login")
        self.username_field = page.get_by_role("textbox", name="Username / Email")
        self.password_field = page.get_by_role("textbox", name="Password")
        self.show_password_button = page.get_by_test_id("show-password-button")
        self.signin_button = page.get_by_role("button", name="Sign In")
        self.verify_shelf = page.get_by_role("heading", name="My Shelf")
        self.usermenu_field = page.get_by_role("link", name= config.username)
        self.logout_link = page.get_by_role("link", name="Log out")

    def click_login(self):
        logger.info("Clicking Login Link")
        self.login_link.click()
    
    def enter_credentials(self, username, password):
        logger.info(f"Entering credentials for user: {username}")
        print("username_field:", type(self.username_field))
        print("username_field:", self.username_field)
        self.username_field.click()
        self.username_field.fill(username)
        self.username_field.press("Tab")
        self.password_field.fill(password)
        

    def click_signin(self):
        logger.info("Clicking Sign In")
        self.signin_button.click()
    
    def login(self, username, password): # Login Complete flow
        self.click_login()
        self.enter_credentials(username, password)
        self.click_signin()

    def click_usermenu(self):
        logger.info("Clicked User Menu")
        self.usermenu_field.click()

    def click_logout(self):
        logger.info("Clicked Log Out")
        self.logout_link.click()
    
    def logout(self):   # Logout Complete flow
        logger.info("Clicked User Menu")
        self.click_usermenu()
        self.click_logout()

    def verify_logged_out(self, timeout: int = 10000):
        logger.info("Verifying logout completed")
        expect(self.login_link).to_be_visible(timeout=timeout)
        logger.info("Logout confirmed — login link visible")


