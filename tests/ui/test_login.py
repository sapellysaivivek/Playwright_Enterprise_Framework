from pages.loginPage import LoginPage
import pytest
import time
from playwright.sync_api import expect
from utils.logger import getloggings
logger = getloggings(__name__)
import allure
from config.config import Base_url



@allure.epic("Note Application")
@allure.feature("Authentication")
@allure.story("Valid Login")
@allure.title("Verify user can login with valid credentials")
#Tc-01 test login with valid credentials
@allure.description(
    "Verify that a registered user can successfully log in and is redirected to the Notes page."
)
@pytest.mark.ui
def test_login(page):

    login_page = LoginPage(page)

    email = "saiviveksapelly@gmail.com"
    password = "142536475869"

    with allure.step("Open Login Page"):
        page.goto(Base_url)

    with allure.step("Enter valid credentials and click Login"):
        login_page.login(email, password)

    with allure.step("Verify Add Note button is visible"):
        expect(page.get_by_test_id("add-new-note")).to_be_visible(timeout=5000)

    with allure.step("Save authentication state"):
        page.context.storage_state(path="state.json")

    with allure.step("Attach page HTML"):
        allure.attach(
            page.content(),
            name="Page HTML",
            attachment_type=allure.attachment_type.HTML
        )
#Tc-03 test login with invalid password   

#TC-04 test login with unregistered email
@allure.story("Invalid Login")
@allure.title("Verify login fails with invalid credentials")
@allure.description(
    "Verify that the application displays an error message when the user attempts to log in with invalid credentials."
)
@pytest.mark.ui
@pytest.mark.parametrize(
    "email,password",
    [
        ("saiviveksapelly@gmail.com", "1455636475869"),
        ("saisaiiii@gmail.com", "142536475869"),
    ],
    ids=[
        "invalid_password",
        "unregistered_user",
    ]
)
def test_invalid_credentials(page, email, password):

    login_page = LoginPage(page)

    with allure.step(f"Login using email: {email}"):
        login_page.login(email, password)

    with allure.step("Verify error message is displayed"):
        expect(page.get_by_test_id("alert-message")).to_be_visible()

    with allure.step("Attach page HTML"):
        allure.attach(
            page.content(),
            name="Invalid Login Page",
            attachment_type=allure.attachment_type.HTML
        )
#TC-05 test Login with empty credentials
@allure.story("Empty Credentials")
@allure.title("Verify login fails with empty credentials")
@allure.description(
    "Verify that validation messages are displayed when the user attempts to log in without entering an email or password."
)
@pytest.mark.ui
def test_empty_crendentials(page):

    loginpage = LoginPage(page)

    with allure.step("Attempt to login with empty email and password"):
        logger.debug("Trying to login with empty credentials")
        loginpage.login("", "")

    with allure.step("Verify email validation message is displayed"):
        expect(page.locator(".invalid-feedback").nth(0)).to_be_visible(timeout=5000)

    with allure.step("Verify password validation message is displayed"):
        expect(page.locator(".invalid-feedback").nth(1)).to_be_visible(timeout=5000)

    with allure.step("Attach page HTML"):
        allure.attach(
            page.content(),
            name="Empty Credentials Page",
            attachment_type=allure.attachment_type.HTML
        )

