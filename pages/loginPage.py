from utils.logger import getloggings
from config.config import Base_url
from playwright.sync_api import expect

class LoginPage():
    def __init__(self, page):
        self.page = page
        self.logger = getloggings(self.__class__.__name__)
    
    username_input = "login-email"
    password_input = "login-password"
    login_button = "login-submit"
    url = f"{Base_url}/login"

    def navigate_to_login_page(self):
        self.logger.debug(f"Navigating to login page: {self.url}")
        self.page.goto(self.url)
    def fill_email(self, email):
        self.logger.debug(f"Filling in email: {email}")
        self.page.get_by_test_id(self.username_input).fill(email)
        self.logger.critical("filled in successfully")
    def fill_password(self, password):
        self.logger.debug(f"Filling in password: {password}")
        self.page.get_by_test_id(self.password_input).fill(password)
    def click_login_button(self):
        self.logger.debug("Clicking the login button")
        self.page.get_by_test_id(self.login_button).click()

    def login(self, email, password):
        self.logger.debug("Starting login process")
        self.navigate_to_login_page()
        self.fill_email(email)
        self.fill_password(password)
        self.click_login_button()
        self.logger.debug("Login process completed")
    