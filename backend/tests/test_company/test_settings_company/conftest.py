import pytest


@pytest.fixture(scope="function", autouse=True)
def data_get_settings_update() -> dict:
    return {
        "name": "Gazprom",
        "email": "Gazprom@email.ru",
        "phone": "+79129320403",
        "address": "Moscow",
        "slugBookingUrl": "qweqwe",
        "description": "new_description",
    }


@pytest.fixture(scope="function", autouse=True)
def data_login_company_after_update_settings() -> dict:
    return {
        "email": "Gazprom@email.ru",
        "password": "Pass312!",
    }
