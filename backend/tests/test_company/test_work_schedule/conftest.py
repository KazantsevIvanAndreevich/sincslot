import pytest


@pytest.fixture(scope="session")
def data_create_work_schedule():
    return {
        "workSchedule": [
            {"dayOfWeek": 1, "workStart": "09:00", "workEnd": "18:00"},
            {"dayOfWeek": 2, "workStart": "09:00", "workEnd": "18:00"},
            {"dayOfWeek": 3, "workStart": "09:00", "workEnd": "18:00"},
            {"dayOfWeek": 4, "workStart": "09:00", "workEnd": "18:00"},
            {"dayOfWeek": 5, "workStart": "09:00", "workEnd": "18:00"},
        ]
    }


@pytest.fixture(scope="session")
def data_update_work_schedule():
    return {
        "workSchedule": [
            {"dayOfWeek": 1, "workStart": "12:00", "workEnd": "17:00"},
            {"dayOfWeek": 5, "workStart": "10:00", "workEnd": "14:00"},
        ]
    }
