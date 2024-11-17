import pytest

@pytest.fixture(scope="session")
def config():
    return {
        "base_url": "https://www.screener.in/"  # Replace with your app's URL
    }
