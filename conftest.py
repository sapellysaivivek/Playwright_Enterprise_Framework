from collections.abc import Generator
from playwright.sync_api import sync_playwright, Page , Playwright , APIRequestContext ,Browser
from utils.logger import getloggings
import pytest
import os 
import allure
from dotenv import load_dotenv
load_dotenv()
from config.config import Base_url
token = os.getenv("token")
Back_end_url = os.getenv("BASE_URL")


logger = getloggings(__name__)

@pytest.fixture
def page(page : Page):
    yield page
    logger.debug("ending page")
@pytest.fixture

def auth_page(browser):
    context = browser.new_context(storage_state="state.json")
    page = context.new_page()

    yield page

    context.close()

@pytest.fixture
def auth_request(playwright : Playwright) -> Generator[APIRequestContext , 0 ,0]:
    header = {
        "x-auth-token" : f"{token}"
    }
    logger.critical(f"backend_url:{Back_end_url}")
    req = playwright.request.new_context(base_url=Back_end_url , extra_http_headers=header)
    yield req
    req.dispose()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:

        page = item.funcargs.get("page") or item.funcargs.get("auth_page")

        if page:
            os.makedirs("screenshots", exist_ok=True)

            screenshot = f"screenshots/{item.name}.png"

            page.screenshot(
                path=screenshot,
                full_page=True
            )

            allure.attach.file(
                screenshot,
                name="Failure Screenshot",
                attachment_type=allure.attachment_type.PNG
            )

            allure.attach(
                page.content(),
                name="Page Source",
                attachment_type=allure.attachment_type.HTML
            )