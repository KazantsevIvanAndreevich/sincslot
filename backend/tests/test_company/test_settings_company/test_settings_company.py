import time
from fastapi import status


async def test_get_settings_company_by_id(
    client, auth_header, data_get_settings_update
):
    resp = client.get("/api/v1/company/settings/", headers=auth_header)

    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()["name"] == "Tesla"
    assert resp.json()["address"] == "string"
    assert resp.json()["email"] == "ElonMask123@example.com"
    assert resp.json()["phone"] == "+79126329304"
    assert resp.json()["slugBookingUrl"] is not None


async def test_update_settings_company(client, auth_header, data_get_settings_update):
    resp = client.patch(
        "/api/v1/company/settings", json=data_get_settings_update, headers=auth_header
    )

    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()["name"] == data_get_settings_update["name"]
    assert resp.json()["address"] == data_get_settings_update["address"]
    assert resp.json()["email"] == data_get_settings_update["email"]
    assert resp.json()["phone"] == data_get_settings_update["phone"]
    assert resp.json()["description"] == data_get_settings_update["description"]
    assert resp.json()["slugBookingUrl"] is not None


async def test_login_company_after_update_settings(
    client, data_login_company_after_update_settings
):
    time.sleep(1)
    resp = client.post(
        "/api/v1/company/auth/login", json=data_login_company_after_update_settings
    )

    assert resp.status_code == status.HTTP_201_CREATED
    assert resp.json().get("accessToken") is not None
    assert resp.cookies.get("refreshToken") is not None
