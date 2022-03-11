from datetime import date, timedelta
from freezegun import freeze_time  # type: ignore
from backend_engineer_interview import __version__
from backend_engineer_interview.handlers import split_start_end_dates


class TestSplitDates:
    def test_dates_exclusively_after_split(self):
        with freeze_time("2021-06-14"):
            split_on_date = date.today()
            start_date = split_on_date + timedelta(days=10)
            end_date = split_on_date + timedelta(days=20)
            dates_before, dates_after = split_start_end_dates(
                start_date, end_date, split_on_date
            )
            assert dates_before is None
            assert dates_after is not None
            assert dates_after.start_date == start_date
        assert dates_after.end_date == end_date

    def test_dates_exclusively_before_split(self):
        with freeze_time("2021-06-14"):
            split_on_date = date.today()
            start_date = split_on_date - timedelta(days=20)
            end_date = split_on_date - timedelta(days=10)
            dates_before, dates_after = split_start_end_dates(
                start_date, end_date, split_on_date
            )

            assert dates_after is None
            assert dates_before is not None
            assert dates_before.start_date == start_date
            assert dates_before.end_date == end_date

    def test_start_date_equals_split_date(self):
        with freeze_time("2021-06-14"):
            split_on_date = date.today()
            start_date = split_on_date
            end_date = split_on_date + timedelta(days=20)
            dates_before, dates_after = split_start_end_dates(
                start_date, end_date, split_on_date
            )

            assert dates_before is not None
            assert dates_before.start_date == start_date
            assert dates_before.end_date == start_date
            assert dates_after is not None
            assert dates_after.start_date == split_on_date + timedelta(days=1)
            assert dates_after.end_date == end_date

    def test_end_date_equals_split_date(self):
        with freeze_time("2021-06-14"):
            split_on_date = date.today()
            start_date = split_on_date - timedelta(days=10)
            end_date = end_date = split_on_date
            dates_before, dates_after = split_start_end_dates(
                start_date, end_date, split_on_date
            )

            assert dates_before is not None
            assert dates_before.start_date == start_date
            assert dates_before.end_date == end_date
            assert dates_after is None


class TestGetEmployee:
    def test_get_employee_endpoint_200(self, test_client):
        response = test_client.get("/v1/employee/1")
        assert response.status_code == 200
        employee_data = response.get_json()
        assert employee_data["id"] == 1
        assert employee_data["first_name"] == "John"
        assert employee_data["last_name"] == "Lennon"
        assert employee_data["date_of_birth"] == "1940-10-04"
        assert "secret" not in employee_data

    def test_get_employee_endpoint_404(self, test_client):
        response = test_client.get("/v1/employee/99")
        assert response.status_code == 404
        assert response.get_json()["message"] == "No such employee"


class TestPatchEmployee:
    def test_patch_employee_valid(self, test_client):
        current_response = test_client.get("/v1/employee/2")
        assert current_response.get_json()["first_name"] == "Rino"
        assert current_response.get_json()["last_name"] == "Star"
        patch_response = test_client.patch(
            "/v1/employee/2", json={"first_name": "Ringo", "last_name": "Starr"}
        )
        assert patch_response.status_code == 204
        updated_response = test_client.get("/v1/employee/2")
        assert updated_response.get_json()["first_name"] == "Ringo"
        assert updated_response.get_json()["last_name"] == "Starr"

    def test_patch_employee_endpoint_404(self, test_client):
        response = test_client.patch(
            "/v1/employee/99", json={"first_name": "Ringo", "last_name": "Starr"}
        )
        assert response.status_code == 404
        assert response.get_json()["message"] == "No such employee"

    def test_patch_employee_invalid(self, test_client):
        patch_response = test_client.patch("/v1/employee/10", json={"last_name": ""})
        assert patch_response.status_code == 400
        assert patch_response.get_json()["message"] == "last_name cannot be blank"


class TestPostApplication:
    def test_post_application_valid(self, test_client):
        application_response = test_client.post(
            "/v1/application",
            json={
                "leave_start_date": "2021-01-01",
                "leave_end_date": "2021-02-01",
                "employee_id": 1,
            },
        )
        assert application_response.status_code == 200
        application = application_response.get_json()
        assert application["leave_start_date"] == "2021-01-01"
        assert application["leave_end_date"] == "2021-02-01"
        assert application["employee"]["first_name"] == "John"
        assert application["id"] is not None

    def test_post_application_invalid(self, test_client):
        application_response = test_client.post(
            "/v1/application",
            json={
                "employee_id": 1,
            },
        )
        assert application_response.status_code == 400
        assert (
            application_response.get_json()["message"]
            == "leave_start_date is missing;leave_end_date is missing"
        )


def test_version():
    assert __version__ == "0.1.0"
