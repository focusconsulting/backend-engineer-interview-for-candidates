from contextlib import contextmanager
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Generator, Optional
from flask import g
import flask
import pydantic
from sqlalchemy.orm import Session
import connexion  # type: ignore

from backend_engineer_interview.models import Employee


class PydanticBaseModel(pydantic.BaseModel):
    class Config:
        orm_mode = True


@contextmanager
def db_session() -> Generator[Session, None, None]:
    """Get a plain SQLAlchemy Session."""
    session = g.get("db")
    if session is None:
        raise Exception("No database session available in application context")

    yield session


@dataclass
class StartEndDates:
    start_date: date
    end_date: date


"""
In Person Exercise

Instructions:
# TODO
"""


def split_start_end_dates(start_date: date, end_date: date, split_date: date):
    # ANSWER
    if start_date > split_date and end_date > split_date:
        return (None, StartEndDates(start_date, end_date))
    elif start_date <= split_date and end_date <= split_date:
        return (StartEndDates(start_date, end_date), None)
    elif start_date == split_date:
        return (
            StartEndDates(start_date, start_date),
            StartEndDates(start_date + timedelta(days=1), end_date),
        )
    else:
        return (
            StartEndDates(start_date, split_date),
            StartEndDates(split_date + timedelta(days=1), end_date),
        )


def status():
    with db_session() as session:
        session.execute("SELECT 1;").one()
        return flask.make_response(flask.jsonify({"status": "up"}), 200)


class EmployeeResponse(PydanticBaseModel):
    id: int
    first_name: str
    last_name: str
    date_of_birth: date


def get_employee(id):
    # ANSWER
    with db_session() as session:

        employee = session.query(Employee).filter(Employee.id == id).one_or_none()

        if not employee:
            return flask.make_response(
                flask.jsonify({"message": "No such employee"}), 404
            )

        return flask.make_response(
            flask.jsonify(EmployeeResponse.from_orm(employee).dict()), 200
        )


# Answer
class PatchEmployeeRequest(PydanticBaseModel):
    first_name: Optional[str]
    last_name: Optional[str]


def patch_employee(id):
    # Answer
    with db_session() as session:
        employee: Employee = (
            session.query(Employee).filter(Employee.id == id).one_or_none()
        )
        if not employee:
            return flask.make_response(
                flask.jsonify({"message": "No such employee"}), 404
            )

        request_body = PatchEmployeeRequest.parse_obj(connexion.request.json)

        if request_body.last_name is not None and request_body.last_name == "":
            return flask.make_response(
                flask.jsonify({"message": "last_name cannot be blank"}), 400
            )
        else:
            employee.last_name = request_body.last_name

        if request_body.first_name is not None and request_body.first_name == "":
            return flask.make_response(
                flask.jsonify({"message": "first_name cannot be blank"}), 400
            )
        else:
            employee.first_name = request_body.first_name

        session.flush()

        return flask.make_response("", 204)


def post_application():
    """
    Accepts a leave_start_date, leave_end_date, employee_id and creates an Application
    with those properties.  It should then return the new application with a status code of 200.

    If any of the properties are missing in the request body, it should return the new application
    with a status code of 400.

    Verify the handler using the test cases in TestPostApplication.  Add any more tests you think
    are necessary.
    """
    pass
