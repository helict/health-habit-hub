# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.classify_context_in import ClassifyContextIn  # noqa: F401
from openapi_server.models.classify_context_out import ClassifyContextOut  # noqa: F401
from openapi_server.models.http_validation_error import HTTPValidationError  # noqa: F401


def test_classify_context_classify_context_post(client: TestClient):
    """Test case for classify_context_classify_context_post

    Determine the context of the sentence describing the habit entered by the user
    """
    classify_context_in = {"habit":"habit","language":"en","uuid":"046b6c7f-0b8a-43b9-b35d-6489e6daee91"}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/classify_context",
    #    headers=headers,
    #    json=classify_context_in,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

