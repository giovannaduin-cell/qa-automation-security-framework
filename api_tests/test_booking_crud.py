import requests
import pytest

BASE_URL = "https://restful-booker.herokuapp.com"


@pytest.fixture(scope="session")
def auth_token():
    payload = {
        "username": "admin",
        "password": "password123"
    }
    response = requests.post(f"{BASE_URL}/auth", json=payload)
    assert response.status_code == 200
    return response.json()["token"]


@pytest.fixture
def auth_headers(auth_token):
    return {
        "Content-Type": "application/json",
        "Cookie": f"token={auth_token}"
    }


@pytest.fixture
def booking_payload():
    return {
        "firstname": "Giovanna",
        "lastname": "Duin",
        "totalprice": 180,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-03-01",
            "checkout": "2026-03-05"
        },
        "additionalneeds": "Breakfast"
    }


def test_booking_crud_flow(auth_headers, booking_payload):
    # CREATE
    create_response = requests.post(
        f"{BASE_URL}/booking",
        json=booking_payload,
        headers=auth_headers
    )
    assert create_response.status_code == 200
    booking_id = create_response.json()["bookingid"]

    # READ
    read_response = requests.get(f"{BASE_URL}/booking/{booking_id}")
    assert read_response.status_code == 200
    assert read_response.json()["firstname"] == booking_payload["firstname"]

    # UPDATE
    booking_payload["lastname"] = "Updated"
    update_response = requests.put(
        f"{BASE_URL}/booking/{booking_id}",
        json=booking_payload,
        headers=auth_headers
    )
    assert update_response.status_code == 200
    assert update_response.json()["lastname"] == "Updated"

    # DELETE
    delete_response = requests.delete(
        f"{BASE_URL}/booking/{booking_id}",
        headers=auth_headers
    )
    assert delete_response.status_code in [200, 201]
