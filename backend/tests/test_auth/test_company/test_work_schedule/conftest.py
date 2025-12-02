import pytest


@pytest.fixture(scope="session")
def data_work_schedule():
    return {
        "workSchedule": [
            {
                "dayOfWeek": 1,
                "workStart": "09:00",
                "workEnd": "18:00"
            },
            {
                "dayOfWeek": 2,
                "workStart": "09:00",
                "workEnd": "18:00"
            },
            {
                "dayOfWeek": 3,
                "workStart": "09:00",
                "workEnd": "18:00"
            },
            {
                "dayOfWeek": 4,
                "workStart": "09:00",
                "workEnd": "18:00"
            },
            {
                "dayOfWeek": 5,
                "workStart": "09:00",
                "workEnd": "18:00"
            }
        ]
    }
