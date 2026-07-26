from conftest import auth_page
from pages.notePage import NotePage
import pytest
import time
import random
import string
import allure
from playwright.sync_api import expect
from utils.logger import getloggings
logger = getloggings(__name__)
#Tc-06 creating note with all details
@allure.epic("Note Application")
@allure.feature("Notes")
@allure.story("Create Note")
@allure.title("Verify user can create a new note")
@allure.description(
    "Verify that a user can successfully create a new note and that it is displayed in the notes list."
)
@pytest.mark.ui
def test_note_creation(auth_page):

    notepage = NotePage(auth_page)

    rand = random.randint(0, 1000)
    title = f"Title{rand}"

    with allure.step("Create a new note"):
        logger.debug("Adding new note")
        notepage.addNote(title, "this is just a random content")

    with allure.step("Verify the created note is visible"):
        expect(
            auth_page.locator('[data-testid="note-card"]').filter(has_text=title)
        ).to_be_visible()

    with allure.step("Delete the created note"):
        notepage.deleteNote(title)

    with allure.step("Attach page HTML"):
        allure.attach(
            auth_page.content(),
            name="Notes Page",
            attachment_type=allure.attachment_type.HTML
        )
# TC-07 creating a note with only title

@pytest.mark.ui
@allure.story("Note Validation")
@allure.title("Verify note cannot be created with only a title")
@allure.description(
    "Verify that the application displays a validation message when a user attempts to create a note without providing a description."
)
def test_note_with_only_title(auth_page):

    notePage = NotePage(auth_page)

    rand = random.randint(0, 1000)
    title = f"title{rand}"

    with allure.step("Attempt to create a note with only a title"):
        logger.debug("Creating note with only title")
        notePage.addNote(title, "")

    with allure.step("Verify description validation message is displayed"):
        expect(
            auth_page.get_by_text("Description is required")
        ).to_be_visible()

    with allure.step("Attach page HTML"):
        allure.attach(
            auth_page.content(),
            name="Note Validation Page",
            attachment_type=allure.attachment_type.HTML
        )
# TC-08 New note appears in UI without refresh
@allure.story("Real-Time Note Visibility")
@allure.title("Verify newly created note appears without refreshing the page")
@allure.description(
    "Verify that a newly created note is immediately visible in the notes list without requiring a page refresh."
)
@pytest.mark.ui
def test_note_appears_without_refresh(auth_page):

    notePage = NotePage(auth_page)

    rand = random.randint(0, 1000)
    title = f"title{rand}"

    with allure.step("Create a new note"):
        logger.debug("Testing whether a note appears without refresh")
        notePage.addNote(title, "A random description")
        logger.debug("New note was successfully created")

    with allure.step("Verify the note is visible without refreshing the page"):
        expect(auth_page.get_by_text(title)).to_be_visible()

    with allure.step("Attach page HTML"):
        allure.attach(
            auth_page.content(),
            name="Notes Page After Creation",
            attachment_type=allure.attachment_type.HTML
        )

    with allure.step("Delete the created note"):
        notePage.deleteNote(title)
        
@allure.story("Note Validation")
@allure.title("Verify note cannot be created with an empty title")
@allure.description(
    "Verify that the application displays a validation message when a user attempts to create a note without providing a title."
)
@pytest.mark.ui
# TC-19: Testing note creation with an empty title
def test_empty_title(auth_page):

    notepage = NotePage(auth_page)

    with allure.step("Attempt to create a note with an empty title"):
        logger.critical("Testing creation of note with empty title")
        notepage.addNote("", "this is some random description")

    with allure.step("Verify title validation message is displayed"):
        expect(
            auth_page.get_by_text("Title is required")
        ).to_be_visible()

    with allure.step("Attach page HTML"):
        allure.attach(
            auth_page.content(),
            name="Empty Title Validation",
            attachment_type=allure.attachment_type.HTML
        )
        
@allure.story("Note Validation")
@allure.title("Verify note cannot be created with a blank title")
@allure.description(
    "Verify that the application displays a validation message when a user attempts to create a note with a title containing only blank spaces."
)
@pytest.mark.ui
# TC-19: Testing note creation with a blank space title
def test_blank_title(auth_page):

    notePage = NotePage(auth_page)

    with allure.step("Attempt to create a note with a blank title"):
        logger.critical("Testing note creation with a blank title")
        notePage.addNote("      ", "this is some random description")

    with allure.step("Verify title length validation message is displayed"):
        expect(
            auth_page.get_by_text("Title must be between 4 and 100 characters")
        ).to_be_visible()

    with allure.step("Attach page HTML"):
        allure.attach(
            auth_page.content(),
            name="Blank Title Validation",
            attachment_type=allure.attachment_type.HTML
        )
    
@allure.epic("Note Application")
@allure.feature("Notes")
@allure.story("Special Characters")
@allure.title("Verify note can be created with special characters in the title")
@allure.description(
    "Verify that a user can successfully create a note with special characters in the title and that the note is displayed correctly."
)
@pytest.mark.ui
def test_speacial_chars__as_title(auth_page):

    notepage = NotePage(auth_page)
    title = "$@!<!>[#"

    with allure.step("Create a note with special characters in the title"):
        notepage.addNote(title, "this is the description")

    with allure.step("Verify the note is displayed with the special character title"):
        expect(
            auth_page.get_by_text(title)
        ).to_be_visible()

    with allure.step("Delete the created note"):
        notepage.deleteNote(title)

    with allure.step("Attach page HTML"):
        allure.attach(
            auth_page.content(),
            name="Special Character Title",
            attachment_type=allure.attachment_type.HTML
        )
@allure.story("Note Validation")
@allure.title("Verify note cannot be created with a title exceeding the maximum length")
@allure.description(
    "Verify that the application displays a validation message when a user attempts to create a note with a title longer than the allowed maximum length."
)
@pytest.mark.ui
def test_title_with_large_title(auth_page):

    notePage = NotePage(auth_page)

    rand = random.randint(0, 1000)
    random_string = ''.join(
        random.choices(string.ascii_letters + string.digits, k=1000)
    )

    with allure.step("Attempt to create a note with a title exceeding the maximum length"):
        notePage.addNote(random_string, f"this is description{rand}")

    with allure.step("Verify title length validation message is displayed"):
        expect(
            auth_page.get_by_text("Title should be between 4 and")
        ).to_be_visible()

    with allure.step("Attach page HTML"):
        allure.attach(
            auth_page.content(),
            name="Large Title Validation",
            attachment_type=allure.attachment_type.HTML
        )
    