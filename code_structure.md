config.json: 
->  "Store environment-level configuration that may change between environments (QA, UAT, Prod) without changing the code"
-> A central configuration file that every part of the framework can read.

utils/config_reader.py
-> Read configuration and credentials from a single place.
-> Separate public config (config.json) from secret data (.env)
-> Keep secrets outside the codebase and load them from environment variables.

utils/logger.py
-> Provide one common logger for the entire framework.
-> Configure logging once and reuse it everywhere.

utils/screenshot_helper.py
-> Save screenshots to a common location.
-> A reusable helper function independent of any test or page.
-> Playwright provides page.screenshot(). Wrap it in a helper if multiple tests use the same logic.

pages/base_page.py
-> Provide common functionality that every page object can reuse. Inheritance — all page classes inherit from BasePage.

tests/conftest.py
-> Share pytest fixtures across all test files.
-> A special pytest file that provides reusable setup and teardown.
-> Avoid duplicate setup code. Share browser/page/login fixtures. Pytest discovers it automatically.
-> Keep reusable fixtures in conftest.py. Pytest automatically makes them available to all tests in that folder.



Mapping each concept:

1. Modules (utils/logger.py, utils/config_reader.py)
Every .py file with standalone reusable functions/classes is a module. You'll import from these constantly across every test file — this is the "write once, use everywhere" principle in practice.

2. Packages (pages/, utils/, tests/ — each with __init__.py)
Any folder grouping related modules becomes a package, letting you write clean imports like from pages.login_page import LoginPage instead of one giant messy file.

3. Utility classes (utils/logger.py, utils/config_reader.py, utils/screenshot_helper.py)
This is same as modules but wrapped in a class instead of loose functions used when reusable logic needs to hold onto some state (data that persists across multiple calls) rather than just running one calculation and returning.

5. Exception Handling — lives inside pages/*.py methods (catching Playwright timeouts) and inside utils/config_reader.py (catching bad JSON/missing files).

6. JSON + Reading config files — config/config.json holds base_url, timeout, browser settings; ConfigReader (a utility class) loads it once.

7. sys.exit() — never called by you directly; pytest handles this automatically and GitHub Actions (ci.yml) reads that exit code.

8. OOP / Page Object Model (pages/base_page.py → children) — coming up right now, this is the backbone connecting everything above.

Rules:
1. // Never put actual email/password in config.json — that file will get committed to Git. 
// Credentials go in environment variables instead (ties back to what we covered with os.environ.get()):