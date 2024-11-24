import pytest
from datetime import datetime
import os

@pytest.fixture(scope="session")
def config():
    # Configuration details for the base URL
    return {
        "base_url": "https://www.screener.in/"  # Replace with your app's URL
    }


# Hook to configure pytest-html reports and create output directories
@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    # Create a reports directory
    report_dir = "Report"
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)

    # Generate timestamped HTML report
    report_file = os.path.join(report_dir, f"Test_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")
    config.option.htmlpath = report_file

# Hook to add final session details after the tests complete
@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    print("\nExecution completed. Check the generated HTML report for details.\n")

# Hook to capture screenshots for failed tests and enrich the HTML report
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Hook to add screenshots only on test failures
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver", None)
        if driver:
            # Create a directory for screenshots if not already present
            screenshot_dir = "Report/screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)

            # Save a screenshot with the test name and timestamp
            screenshot_path = os.path.join(
                screenshot_dir, f"{item.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            )
            driver.save_screenshot(screenshot_path)

            # Add the screenshot to the report
            if hasattr(report, "extra"):
                from pytest_html import extras
                report.extra = getattr(report, "extra", [])
                report.extra.append(extras.image(screenshot_path, name="Failure Screenshot"))
