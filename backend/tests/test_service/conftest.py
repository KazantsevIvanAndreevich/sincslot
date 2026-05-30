import pytest


@pytest.fixture(scope="function", autouse=True)
def data_create_service() -> dict:
    return {
        "name": "my_service1",
        "price": 100,
        "duration": 20,
        "description": "description",
    }


@pytest.fixture(scope="function", autouse=True)
def data_create_services() -> list[dict]:
    return [
        {
            "name": "my_service2",
            "price": 100,
            "duration": 20,
            "description": "description",
        },
        {
            "name": "my_service2",
            "price": 120,
            "duration": 30,
            "description": "description",
        },
        {
            "name": "my_service3",
            "price": 140,
            "duration": 50,
            "description": "description",
        },
        {
            "name": "my_service4",
            "price": 1000,
            "duration": 100,
            "description": "description",
        },
    ]


@pytest.fixture(scope="function", autouse=True)
def data_update_service() -> dict:
    return {
        "name": "my_service_to_update",
        "price": 10000,
        "duration": 1000,
        "description": "description_my_service_to_update",
    }


@pytest.fixture(scope="function", autouse=True)
def data_remove_service() -> dict:
    return {
        "name": "my_service_to_remove",
        "price": 10000,
        "duration": 1000,
        "description": "description_my_service_to_update",
    }
