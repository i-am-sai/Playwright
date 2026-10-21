Create Virtual Environment: python3 -m venv venv(name of virt env)
activate venv: source venv/bin/activate
Install python Libraries: pip install -r requirement.txt or python -m pip install -r requirements.txt

This install all the below required python libraries:
python-dotenv
allure-pytest
pytest-html
pytest
playwright
pytest-playwright

playwright install: Command to install Playwrigt browser binaries (Connects Playwright with pytest and adds --browser, --headed, --tracing, etc.)

Installs the Ubuntu system libraries required to run those browsers: sudo /mnt/e/Playwright/venv/bin/playwright install-deps


Flow: 
Your Playwright test
       ↓
Python Playwright package
       ↓
Playwright browser
(Chromium / Firefox / WebKit)
       ↓
Ubuntu system libraries
       ↓
Linux kernel / hardware

Create .env file and add credentials for testing: 
TEST_USERNAME=example@yopmail.com
TEST_PASSWORD=Test@123