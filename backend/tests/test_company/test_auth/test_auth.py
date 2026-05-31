import time
from fastapi import status


#################### Register company ####################


async def test_register(client, data_register_company):
    resp = client.post("/api/v1/company/auth/register", json=data_register_company)

    assert resp.status_code == status.HTTP_201_CREATED
    assert resp.json().get("accessToken") is not None
    assert resp.cookies.get("refreshToken") is not None


async def test_register_when_exists(client, data_register_company):
    resp = client.post("/api/v1/company/auth/register", json=data_register_company)

    assert resp.status_code == status.HTTP_409_CONFLICT
    assert resp.json().get("accessToken") is None
    assert resp.cookies.get("refreshToken") is None


async def test_register_when_incorrect_email(
    client, data_register_company_with_incorrect_email
):
    resp = client.post(
        "/api/v1/company/auth/register", json=data_register_company_with_incorrect_email
    )

    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert resp.json().get("accessToken") is None
    assert resp.cookies.get("refreshToken") is None


async def test_register_when_incorrect_password(
    client, data_register_company_with_incorrect_password
):
    resp = client.post(
        "/api/v1/company/auth/register",
        json=data_register_company_with_incorrect_password,
    )

    assert resp.status_code == status.HTTP_409_CONFLICT
    assert resp.json().get("accessToken") is None
    assert resp.cookies.get("refreshToken") is None


async def test_register_when_password_do_not_match(
    client, data_register_company_when_password_do_not_match
):
    resp = client.post(
        "/api/v1/company/auth/register",
        json=data_register_company_when_password_do_not_match,
    )

    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp.json().get("accessToken") is None
    assert resp.cookies.get("refreshToken") is None


#################### Login company ####################


async def test_login(client, data_login_company):
    time.sleep(1)
    resp = client.post("/api/v1/company/auth/login", json=data_login_company)

    assert resp.status_code == status.HTTP_201_CREATED
    assert resp.json().get("accessToken") is not None
    assert resp.cookies.get("refreshToken") is not None


async def test_login_when_company_not_exist(
    client, data_login_company_when_company_not_exist
):
    resp = client.post(
        "/api/v1/company/auth/login", json=data_login_company_when_company_not_exist
    )

    assert resp.status_code == status.HTTP_404_NOT_FOUND
    assert resp.json().get("accessToken") is None
    assert resp.cookies.get("refreshToken") is None


#################### Recover password ####################


async def test_recover_password(client, data_recover_password):
    resp = client.post("/api/v1/company/auth/recover", json=data_recover_password)

    assert resp.status_code == status.HTTP_200_OK


async def test_recover_password_not_exist_company(
    client, data_recover_password_not_exist_company
):
    resp = client.post(
        "/api/v1/company/auth/recover", json=data_recover_password_not_exist_company
    )

    assert resp.status_code == status.HTTP_404_NOT_FOUND
