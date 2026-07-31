from urllib import response
import pytest
from typing import Generator
from playwright.sync_api import APIRequestContext ,Playwright
import time
from utils.logger import getloggings
import random
import os
import allure
import json
from config.config import Backend_Base_Url
Backend_url = Backend_Base_Url
logger = getloggings(__name__)

@allure.epic("Note Application")
@allure.feature("Notes API")
@allure.story("Get Notes")
@allure.title("Verify GET /notes returns all notes successfully")
@allure.description(
    "Verify that the GET /notes endpoint returns a successful response "
    "containing a list of notes."
)
@pytest.mark.api
def test_get_notes(auth_request):

    logger.debug("Testing GET /notes response")

    with allure.step("Send GET /notes request"):
        response = auth_request.get("notes")

    with allure.step("Attach API response"):
        allure.attach(
            json.dumps(response.json(), indent=4),
            name="GET Notes Response",
            attachment_type=allure.attachment_type.JSON
        )

    with allure.step("Verify response status code is 200"):
        assert response.status == 200

    body = response.json()

    with allure.step("Verify response contains the 'data' field"):
        assert "data" in body

    with allure.step("Verify 'data' is a list"):
        assert isinstance(body["data"], list)

    logger.info("Notes are accessible")
    
    
@allure.story("New User Notes")
@allure.title("Verify GET /notes returns an empty list for a newly registered user")
@allure.description(
    "Verify that a newly registered user has no notes and that the "
    "GET /notes endpoint returns an empty list."
)
@pytest.mark.api
# TC-10: Verify GET /notes returns an empty array for a new user
def test_new_user_notes(playwright: Playwright):

    logger.debug("Testing GET /notes for a new user")

    req = playwright.request.new_context()

    rand = random.randint(1000, 99999)
    email = f"sapellysaivivek{rand}@gmail.com"
    password = "142536475869"

    with allure.step("Register a new user"):
        register_response = req.post(
            "https://practice.expandtesting.com/notes/api/users/register",
            data={
                "name": f"Bot User {rand}",
                "email": email,
                "password": password
            }
        )

        allure.attach(
            register_response.text(),
            name="Register Response",
            attachment_type=allure.attachment_type.JSON
        )

        assert register_response.status == 201

    with allure.step("Login with the newly registered user"):
        login_response = req.post(
            "https://practice.expandtesting.com/notes/api/users/login",
            data={
                "email": email,
                "password": password
            }
        )

        allure.attach(
            login_response.text(),
            name="Login Response",
            attachment_type=allure.attachment_type.JSON
        )

        assert login_response.status == 200

    token = login_response.json()["data"]["token"]

    with allure.step("Send GET /notes request"):
        notes_response = req.get(
            "https://practice.expandtesting.com/notes/api/notes",
            headers={
                "x-auth-token": token
            }
        )

        allure.attach(
            notes_response.text(),
            name="GET Notes Response",
            attachment_type=allure.attachment_type.JSON
        )

        assert notes_response.status == 200

    notes_json = notes_response.json()

    with allure.step("Verify the new user has no notes"):
        assert notes_json["data"] == []

    req.dispose()
@allure.story("Get Note by ID")
@allure.title("Verify GET /notes/{id} returns the correct note")
@allure.description(
    "Verify that the GET /notes/{id} endpoint returns the details of an existing note "
    "when a valid note ID is provided."
)
@pytest.mark.api
# TC-12: Testing GET /notes/{id}
def test_notes_by_api(auth_request):

    logger.fatal("Testing GET /notes/{id} endpoint")
    rand = random.randint(0, 1000)

    with allure.step("Create a new note using the API"):
        response = auth_request.post(
            "notes",
            data={
                "title": f"title{rand}",
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

    with allure.step("Send GET /notes/{id} request"):
        get_res = auth_request.get(f"notes/{note_id}")

        allure.attach(
            json.dumps(get_res.json(), indent=4),
            name="GET Note by ID Response",
            attachment_type=allure.attachment_type.JSON
        )

        assert get_res.status == 200

    with allure.step("Verify the returned note ID matches the created note"):
        assert get_res.json()["data"]["id"] == note_id

    with allure.step("Delete the created note"):
        delete_res = auth_request.delete(f"notes/{note_id}")

        allure.attach(
            json.dumps(delete_res.json(), indent=4),
            name="Delete Note Response",
            attachment_type=allure.attachment_type.JSON
        )

        assert delete_res.status == 200
@allure.story("Delete Note")
@allure.title("Verify deleting an already deleted note returns 404")
@allure.description(
    "Verify that attempting to delete a note that has already been deleted "
    "returns a 404 Not Found status code."
)
@pytest.mark.api
# TC-13: Verify deleting an already deleted note returns 404
def test_deleting_deleted_note(auth_request):

    logger.critical("Testing that deleting a deleted note returns status code 404")
    rand = random.randint(0, 1000)

    with allure.step("Create a new note using the API"):
        response = auth_request.post(
            "notes",
            data={
                "title": f"title{rand}",
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

    with allure.step("Delete the created note"):
        del_res = auth_request.delete(f"notes/{note_id}")

        allure.attach(
            json.dumps(del_res.json(), indent=4),
            name="First Delete Response",
            attachment_type=allure.attachment_type.JSON
        )

        assert del_res.status == 200

    with allure.step("Attempt to delete the same note again"):
        del_twice = auth_request.delete(f"notes/{note_id}")

        allure.attach(
            json.dumps(del_twice.json(), indent=4),
            name="Second Delete Response",
            attachment_type=allure.attachment_type.JSON
        )

        assert del_twice.status == 404
@allure.story("Performance Testing")
@allure.title("Verify GET /notes average response time is under 2 seconds")
@allure.description(
    "Verify that the average response time of the GET /notes endpoint "
    "over five consecutive requests is less than 2000 milliseconds."
)
@pytest.mark.api
# TC-14: Testing response time for GET /notes
def test_notes_responce_time(auth_request):

    logger.debug("Testing GET /notes response time")

    sum_res = 0
    response_times = []

    with allure.step("Send five GET /notes requests and measure response time"):

        for i in range(5):

            logger.debug(f"Making request {i + 1} to /notes endpoint")

            start = time.perf_counter()

            response = auth_request.get("notes")

            end = time.perf_counter()

            assert response.status == 200

            response_time = (end - start) * 1000

            response_times.append(
                f"Request {i + 1}: {response_time:.2f} ms"
            )

            sum_res += response_time

    avg_res = sum_res / 5

    with allure.step("Attach response time measurements"):
        allure.attach(
            "\n".join(response_times),
            name="Response Times",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("Verify average response time is below 2000 ms"):
        allure.attach(
            f"Average Response Time: {avg_res:.2f} ms",
            name="Average Response Time",
            attachment_type=allure.attachment_type.TEXT
        )

        logger.info(f"Average response time: {avg_res:.2f} ms")

        assert avg_res < 2000
@pytest.mark.api
#TC-15 testing post/Notes response time is under 2s
@allure.story("Performance Testing")
@allure.title("Verify POST /notes average response time is under 2 seconds")
@allure.description(
    "Verify that the average response time of the POST /notes endpoint "
    "over five consecutive requests is less than 2000 milliseconds."
)
@pytest.mark.api
# TC-15: Testing response time for POST /notes
def test_restime_postnotes(auth_request):

    logger.critical("Testing POST /notes response time")

    total_response_time = 0
    response_times = []

    with allure.step("Send five POST /notes requests and measure response time"):

        for i in range(5):

            rand = random.randint(0, 1000)

            start = time.perf_counter()

            response = auth_request.post(
                "notes",
                data={
                    "title": f"title{rand}",
                    "description": "avjlqhbrvq;kv",
                    "category": "Home"
                }
            )

            end = time.perf_counter()

            assert response.status == 200

            response_time = (end - start) * 1000

            response_times.append(
                f"Request {i + 1}: {response_time:.2f} ms"
            )

            total_response_time += response_time

            note_id = response.json()["data"]["id"]

            auth_request.delete(f"notes/{note_id}")

    average_response_time = total_response_time / 5

    with allure.step("Attach response time measurements"):
        allure.attach(
            "\n".join(response_times),
            name="POST Response Times",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("Verify average response time is below 2000 ms"):

        allure.attach(
            f"Average Response Time: {average_response_time:.2f} ms",
            name="Average Response Time",
            attachment_type=allure.attachment_type.TEXT
        )

        logger.info(
            f"Average response time for POST /notes: {average_response_time:.2f} ms"
        )

        assert average_response_time < 2000
    
#TC-17 testing response time for delete/id
@allure.story("Performance Testing")
@allure.title("Verify DELETE /notes average response time is under 2 seconds")
@allure.description(
    "Verify that the average response time of the DELETE /notes endpoint "
    "over five consecutive requests is less than 2000 milliseconds."
)
@pytest.mark.api
# TC-16: Testing response time for DELETE /notes
def test_deletion_res_time(auth_request):

    logger.critical("Testing DELETE /notes response time")

    note_ids = []
    response_times = []
    total_response_time = 0

    with allure.step("Create five notes for deletion testing"):

        for i in range(5):

            rand = random.randint(0, 1000)

            res = auth_request.post(
                "notes",
                data={
                    "title": f"title{rand}",
                    "description": "avjlqhbrvq;kv",
                    "category": "Home"
                }
            )

            assert res.status == 200

            note_ids.append(res.json()["data"]["id"])

    with allure.step("Delete the created notes and measure response time"):

        for index, note_id in enumerate(note_ids, start=1):

            start = time.perf_counter()

            res = auth_request.delete(f"notes/{note_id}")

            end = time.perf_counter()

            assert res.status == 200

            response_time = (end - start) * 1000

            response_times.append(
                f"Request {index}: {response_time:.2f} ms"
            )

            total_response_time += response_time

    average_response_time = total_response_time / 5

    with allure.step("Attach response time measurements"):
        allure.attach(
            "\n".join(response_times),
            name="DELETE Response Times",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("Verify average response time is below 2000 ms"):

        allure.attach(
            f"Average Response Time: {average_response_time:.2f} ms",
            name="Average Response Time",
            attachment_type=allure.attachment_type.TEXT
        )

        logger.info(
            f"Average DELETE response time: {average_response_time:.2f} ms"
        )

        assert average_response_time < 2000
@allure.story("Unauthorized Access")
@allure.title("Verify unauthenticated users cannot access GET /notes")
@allure.description(
    "Verify that an unauthenticated user attempting to access the "
    "GET /notes endpoint receives a 401 Unauthorized response."
)
@pytest.mark.api
# TC-18: Verify unauthenticated users cannot access GET /notes
def test_accessing_notes_without_authentication(playwright: Playwright):

    logger.critical("Testing access to GET /notes without authentication")

    with allure.step("Create an unauthenticated API request context"):
        req = playwright.request.new_context(base_url=Backend_url)

    try:
        with allure.step("Send GET /notes request without authentication"):

            response = req.get("notes")

            allure.attach(
                response.text(),
                name="Unauthorized Response",
                attachment_type=allure.attachment_type.JSON
            )

            assert response.status == 401

    finally:
        with allure.step("Dispose the API request context"):
            req.dispose()
    
@allure.story("Unauthorized Access")
@allure.title("Verify unauthenticated users cannot delete a note")
@allure.description(
    "Verify that an unauthenticated user attempting to delete an existing "
    "note receives a 401 Unauthorized response."
)
@pytest.mark.api
# TC-19: Verify DELETE /notes/{id} without authentication
def test_delete_with_auth_token(auth_request, playwright: Playwright):

    with allure.step("Create a note using an authenticated request"):

        res = auth_request.post(
            "notes",
            data={
                "title": "Title",
                "description": "avjlqhbrvq;kv",
                "category": "Home"
            }
        )

        allure.attach(
            json.dumps(res.json(), indent=4),
            name="Create Note Response",
            attachment_type=allure.attachment_type.JSON
        )

        assert res.status == 200

    note_id = res.json()["data"]["id"]

    with allure.step("Create an unauthenticated API request context"):

        req = playwright.request.new_context(base_url=Backend_url)

    try:
        with allure.step("Attempt to delete the note without authentication"):

            response = req.delete(f"notes/{note_id}")

            allure.attach(
                response.text(),
                name="Unauthorized Delete Response",
                attachment_type=allure.attachment_type.JSON
            )

            assert response.status == 401

    finally:
        with allure.step("Delete the note using the authenticated request"):
            auth_request.delete(f"notes/{note_id}")

        with allure.step("Dispose the API request context"):
            req.dispose()
    
