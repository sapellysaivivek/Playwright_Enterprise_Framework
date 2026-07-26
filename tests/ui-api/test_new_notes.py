import pytest
import random
from pages.notePage import NotePage
from utils.logger import getloggings
import allure
logger = getloggings(__name__)
import json

@allure.epic("Note Application")
@allure.feature("UI_API_INTERACTION")
@allure.story("Testing UI and API interactions")
@pytest.mark.ui_api
@allure.title("UI created note appears in API")
@allure.description("Create a note using the UI and verify it is available through the GET /notes API.")

def test_UI_created_note_appears_in_Api(auth_page, auth_request):

    notepage = NotePage(auth_page)
    rand = random.randint(0, 1000)

    title = f"title{rand}"
    description = "this is random description"

    with allure.step("Create a note using the UI"):
        notepage.addNote(title, description)

    with allure.step("Attach page HTML after note creation"):
        allure.attach(
            auth_page.content(),
            name="Page HTML",
            attachment_type=allure.attachment_type.HTML
        )

    with allure.step("Call GET /notes API"):
        response = auth_request.get("notes")

    with allure.step("Attach API Response"):
        allure.attach(
            json.dumps(response.json(), indent=4),
            name="GET Notes Response",
            attachment_type=allure.attachment_type.JSON
        )

    with allure.step("Verify status code"):
        assert response.status == 200

    with allure.step("Verify note exists in API"):
        assert any(
            note.get("title") == title
            for note in response.json().get("data", [])
        )

    with allure.step("Delete the created note"):
        notepage.deleteNote(title)
#TC-14 testing note is not visible after API Deletion
@pytest.mark.testu
@allure.story("Delete note using API")
@allure.title("Verify note is not visible in UI after API deletion")
@allure.description(
    "Create a note using the API, verify it is visible in the UI, "
    "delete it using the API, and verify it disappears from the UI."
)
def test_Note_not_visible_after_api_deletion(auth_page, auth_request):

    rand = random.randint(0, 1000)
    title = f"title{rand}"

    with allure.step("Create a note using API"):
        response = auth_request.post(
            "notes",
            data={
                "title": title,
                "description": "avjlqhbrvq;kv",
                "category": "Home"
            }
        )

        allure.attach(
            json.dumps(response.json(), indent=4),
            name="Create Note Response",
            attachment_type=allure.attachment_type.JSON
        )

        assert response.status == 200

    note_id = response.json()["data"]["id"]

    notePage = NotePage(auth_page)

    with allure.step("Verify note is visible in UI"):
        assert notePage.is_note_present(title)
        logger.info("Note is visible in UI")

    with allure.step("Delete note using API"):
        del_res = auth_request.delete(f"notes/{note_id}")

        allure.attach(
            json.dumps(del_res.json(), indent=4),
            name="Delete Note Response",
            attachment_type=allure.attachment_type.JSON
        )

        assert del_res.status == 200
        logger.info("Note deleted successfully")

    with allure.step("Verify note is no longer visible in UI"):
        assert not notePage.is_note_present(title)

    with allure.step("Attach final page HTML"):
        allure.attach(
            auth_page.content(),
            name="Final Page HTML",
            attachment_type=allure.attachment_type.HTML
        )
    