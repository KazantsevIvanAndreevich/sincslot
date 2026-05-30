import pytest


@pytest.fixture(scope="function", autouse=True)
def data_recover_password():
    return {"email": "SteveJobs123@example.com"}


@pytest.fixture(scope="function", autouse=True)
def data_recover_password_not_exist_company():
    return {"email": "qwe@example.com"}


@pytest.fixture(scope="function", autouse=True)
def data_login_company():
    return {
        "email": "SteveJobs123@example.com",
        "password": "Pass123!",
    }


@pytest.fixture(scope="function", autouse=True)
def data_login_company_when_company_not_exist():
    return {
        "email": "NotExistEmail@example.com",
        "password": "Pass123!",
    }


@pytest.fixture(scope="function", autouse=True)
def data_register_company():
    return {
        "name": "Apple",
        "address": "string",
        "email": "SteveJobs123@example.com",
        "phone": "+79126329303",
        "password": "Pass123!",
        "repeatPassword": "Pass123!",
    }


@pytest.fixture(scope="function", autouse=True)
def data_register_company_with_incorrect_email():
    return {
        "name": "Apple",
        "address": "string",
        "email": "incorrect_email.com",
        "phone": "+79126329303",
        "password": "Pass123!",
        "repeatPassword": "Pass123!",
    }


@pytest.fixture(scope="function", autouse=True)
def data_register_company_with_incorrect_password():
    return {
        "name": "Apple",
        "address": "string",
        "email": "SteveJobs123@example.com",
        "phone": "+79126329303",
        "password": "1",
        "repeatPassword": "1",
    }


@pytest.fixture(scope="function", autouse=True)
def data_register_company_when_password_do_not_match():
    return {
        "name": "Apple",
        "address": "string",
        "email": "SteveJobs123@example.com",
        "phone": "+79126329303",
        "password": "Pass123!",
        "repeatPassword": "Pass124!",
    }
