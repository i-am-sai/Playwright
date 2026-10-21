from logging import config
import playwright
import pytest
import shutil # inbuilt lib no need to install
import base64
from pathlib import Path
from playwright.sync_api import expect
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.shelf_page import ShelfPage
from pages.annotation_page import AnnotationPage
from utils.config_reader import ConfigReader
from utils.screenshot_helper import take_screenshot
from utils.logger import logger
from pytest_html import extras

@pytest.fixture(scope="session", autouse=True)  # Fixture to clear screenshots before starring each session
def clean_reports():
    shutil.rmtree("reports/screenshots", ignore_errors=True)
    # shutil.rmtree("reports/logs", ignore_errors=True)
    yield


@pytest.fixture(scope="session") # Fixture for storing authentication state for a every session
def authenticated_state(browser):
    config = ConfigReader()
    context = browser.new_context()
    page = context.new_page()
    login_page = LoginPage(page)

    logger.info("Performing one-time login for session")
    login_page.navigate(config.get("base_url"))
    login_page.accept_cookies()
    login_page.click_login()
    login_page.accept_cookies()
    login_page.enter_credentials(config.username, config.password)
    login_page.click_signin()

    login_page.capture_screenshot("After clicking Sign In")
    expect(page).to_have_url(config.get("bookshelf_url"))
    expect(page.get_by_text("Please login")).not_to_be_visible()   # explicit negative check
    
   # Let any trailing redirects/cookie-setting requests fully settle
    page.wait_for_load_state("networkidle")
    
    cookies = context.cookies()
    auth_cookie = next((c for c in cookies if c["name"] == "SimpleSAMLAuthToken"), None) # List Comphrension

    if not auth_cookie:
        raise Exception(
            "Login flow completed but SimpleSAMLAuthToken cookie was not set — "
            "authentication state is invalid, refusing to save storage_state."
        )

    logger.info(f"SimpleSAMLAuthToken confirmed present, saving storage state {auth_cookie}")
    state = context.storage_state(path="reports/.auth/auth_state.json")
    context.close()
    return state

@pytest.fixture    # Fixture that maintains the logged in state of the site and returns raw playwright page object
def logged_in_page(browser, authenticated_state):
    config = ConfigReader()
    context = browser.new_context(storage_state="reports/.auth/auth_state.json")
    context.tracing.start(
      screenshots=True,
        snapshots=True,        sources=True     )
    page = context.new_page()
    page.goto(config.get("bookshelf_url"))
    yield page

    context.tracing.stop(
        path="reports/traces/trace.zip"
    )
    context.close()

# @pytest.fixture
# def logged_in_page(browser, playwright, authenticated_state):
#     config = ConfigReader()
#     pixel_7 = playwright.devices["Pixel 7"]
#     context = browser.new_context(storage_state="reports/.auth/auth_state.json", **pixel_7)
#     page = context.new_page()
#     page.goto(config.get("bookshelf_url"))
#     yield page
#     context.close()


@pytest.hookimpl(hookwrapper=True) # Hook to generate reports 
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("logged_in_page")
        if page:
            try: 
                screenshot_name = f"{item.name}_FAILURE"
                take_screenshot(page, screenshot_name)  # reuses your existing function

                screenshot_path = Path("reports/screenshots") / f"{screenshot_name}.png"
                if screenshot_path.exists():
                        with open(screenshot_path, "rb") as f:
                            screenshot_bytes = f.read()

                    # pytest-html (self-contained mode) needs base64 STRING, not raw bytes
                        encoded_screenshot = base64.b64encode(screenshot_bytes).decode("utf-8")

                        report.extras = getattr(report, "extras", [])
                        report.extras.append(extras.image(encoded_screenshot, mime_type="image/png"))

                logger.info(f"Failure screenshot saved and attached: {screenshot_path}")
            except Exception as e:
                logger.warning(f"Failed to capture/attach failure screenshot: {e}")

# logged_in_page: is already the real Playwright page, not a wrapper object.
# It is already a: page = context.new_page() and not logged_in_page.page

@pytest.fixture       # Fixture to load reader from shelf after login with already authenticated state.
def reader_on_chapter(logged_in_page):
    """
    Navigates from bookshelf -> reader -> opens TOC -> lands on a specific chapter.
    Returns a ready-to-use ReaderPage positioned on that chapter, so annotation/
    highlight tests can start directly from content interaction without repeating
    navigation steps.
    """
    shelf = ShelfPage(logged_in_page)
    shelf.capture_screenshot("New State after Login")
    shelf.open_bookshelf()

    reader = shelf.click_read_online()
    reader.verify_reader_loaded()
    reader.capture_screenshot("Reader Loaded")
    reader.open_table_of_contents()
    reader.capture_screenshot("TOC Loaded")
    
    reader.click_toc_chapter("Part 4")
    reader.capture_screenshot("TOC Chapter 4 Loaded")
    reader.verify_chapter_heading("Testing")
    # reader.verify_chapter_content("aha1418")
    # logger.info("Chapter content 1418 present ")

    return reader

@pytest.fixture
def annotation_page(reader_on_chapter):
    return AnnotationPage(reader_on_chapter.page)


# import shutil — Python's built-in module for higher-level file operations; os can delete single files, but shutil is what you use for deleting entire folders and their contents at once.

# @pytest.fixture(scope="session", autouse=True) — two things happening here:

# scope="session" means this runs once for the entire test run, not once per test — you want cleanup to happen a single time, at the very start, not repeated before every individual test.
# autouse=True means every test automatically triggers this fixture without needing to list it as a parameter — you'll never write def test_login(clean_reports, page):, it just happens silently in the background for the whole session.
# yield — this is the same pattern from your browser/page fixtures. Everything before yield runs as setup (the cleanup, in this case), and since there's no code after yield, there's no teardown step — the fixture just finishes once the whole session ends.

# tests/conftest.py
# No custom fixtures needed yet.
# pytest-playwright already provides:
# browser
# context
# page

# Why return AnnotationPage(reader_on_chapter.page)
# Here:

# reader_on_chapter is a page object instance of ReaderPage.

# So:

# reader_on_chapter is not the raw browser page
# it is an object that wraps a Playwright page
# reader_on_chapter.page means: “give me the underlying Playwright Page inside that reader object”



# You have two layers:

# Page Object layer

# ReaderPage
# AnnotationPage
# Playwright browser layer

# the actual Page object
# reader_on_chapter = object representing the reader page
# reader_on_chapter.page = the real browser page inside that object

# so, both points to same browser page context
# reader_on_chapter.page
# annotation_page.page


# So:

# the browser page is reused for the test session
# but each test gets its own fresh fixture-created page object instance
# the underlying browser page is still the same logged-in page context for that fixture lifecycle
