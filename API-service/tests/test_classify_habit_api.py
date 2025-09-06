# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.http_validation_error import HTTPValidationError  # noqa: F401
from openapi_server.models.habit_in import HabitIn  # noqa: F401
from openapi_server.models.habit_out import HabitOut  # noqa: F401


def test_classify_habit_classify_habit_post(client: TestClient):
    """Test case for classify_habit_classify_habit_post

    Determine whether the sentence entered by the user is a habit
    """
    habit_in = {"habit":"habit","language":"language","uuid":"uuid"}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/classify_habit",
    #    headers=headers,
    #    json=habit_in,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

