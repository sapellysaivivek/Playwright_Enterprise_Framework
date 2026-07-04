import re
import pytest
from playwright.sync_api import Page , expect
def test_example(page: Page):
    context = page.context
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    expect(page).to_have_title(re.compile("OrangeHRM"))
    