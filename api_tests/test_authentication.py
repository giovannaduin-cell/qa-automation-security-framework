import requests
import pytest


BASE_URL = "https://restful-booker.herokuapp.com"
AUTH_ENDPOINT = "/auth"


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


def test_authentication_with_valid_credentials(base_url):
    """
    Validates successful authentication with valid credentials.
    """
    payload = {
        "username": "admin",
        "password": "password123"
    }

    response = requests.post(f"{base_url}{AUTH_ENDPOINT}", json=payload)

    assert response.status_code == 200, "Expected HTTP 200 for valid authentication"
    assert "token" in response.json(), "Authentication token not found in response"


def test_authentication_with_invalid_credentials(base_url):
    """
    Validates authentication failure with invalid credentials.
    """
    payload = {
        "username": "invalid_user",
        "password": "wrong_password"
    }

    response = requests.post(f"{base_url}{AUTH_ENDPOINT}", json=payload)

    assert response.status_code == 200, "API returns 200 even for invalid auth"
    assert "token" not in response.json(), "Token should not be returned for invalid auth"


def test_authentication_with_missing_fields(base_url):
    """
    Validates authentication behavior when required fields are missing.
    """
    payload = {
        "username": "admin"
    }

    response = requests.post(f"{base_url}{AUTH_ENDPOINT}", json=payload)

    assert response.status_code in [200, 400], "Unexpected status code for invalid payload"
