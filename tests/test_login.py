import pytest
from playwright.sync_api import expect
from pages.login_page import LoginPage
from utils.config_reader import ConfigReader
from utils.logger import logger

@pytest.mark.smoke
@pytest.mark.sanity
@pytest.mark.regression
@pytest.mark.order(-1) 
def test_logout(logged_in_page):
    config = ConfigReader()
    login_page = LoginPage(logged_in_page)

    logger.info("\nTest Case 3: Logging Out")    

    logged_in_page.goto(config.get("bookshelf_url"))
    login_page.capture_screenshot("after_login")
    logger.info("Successfully Logged In")
    login_page.click_usermenu()
    login_page.capture_screenshot("about_to_logout")
    login_page.click_logout()
    login_page.capture_screenshot("after_logout")
    login_page.verify_logged_out
    logger.info("Successfully Logged Out")
    # Pending: Logout Assertion










# import re
# import pytest
# from playwright.sync_api import expect
# from pages.login_page import LoginPage
# from utils.config_reader import ConfigReader
# from utils.logger import logger


# def test_login_flow(page):
#     config = ConfigReader()
#     login_page = LoginPage(page)

#     logger.info("Starting Login Flow Test")

#     login_page.navigate(config.get("base_url"))
#     login_page.capture_screenshot("after_navigate")
#     login_page.accept_cookies()  # first OneTrust banner, on base site
#     login_palge.capture_screenshot("after_cookies")
#     login_page.click_login()
 
#     # expect(page).to_have_url(config.get("sso_login_url"))
#     logger.info("SSO Login Page loaded successfully")
#     login_page.capture_screenshot("SSO Page")
#     login_page.accept_cookies()
    
#     login_page.enter_credentials(config.username, config.password)
#     login_page.click_signin()
     
#     expect(page).to_have_url(config.get("bookshelf_url"))
#     login_page.capture_screenshot("Login Completed")
#     logger.info("Bookshelf page loaded successfully: Login Flow Complete")

#     # logger.info("Starting Logout Flow Test")
#     # logger.info("User Menu Link Found")
#     # login_page.capture_screenshot("User menu photo")
#     # login_page.click_usermenu()
    
#     # login_page.click_logout()
#     # login_page.capture_screenshot("Logout Completed")
#     # logger.info("Logout Flow Complete")

# def test_logout(logged_in_page):
#     config = ConfigReader()
#     login_page = LoginPage(logged_in_page)
    
#     logged_in_page.goto(config.get("bookshelf_url"))
#     login_page.click_usermenu()
#     login_page.click_logout()

#     expect(logged_in_page).to_have_url(config.get("base_url"))
     


























