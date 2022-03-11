import pytest
from backend_engineer_interview.app import create_app


@pytest.fixture
def test_client():
    return create_app().app.test_client()
