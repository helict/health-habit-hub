# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.health_status import HealthStatus  # noqa: F401


def test_health_health_get(client: TestClient):
    """Test case for health_health_get

    Health Check
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/health",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

