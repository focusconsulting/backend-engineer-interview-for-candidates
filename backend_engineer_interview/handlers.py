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

# Helpers
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


def get_request():
    return connexion.request


@dataclass
class StartEndDates:
    start_date: date
    end_date: date



# Implement

def split_start_end_dates(start_date: date, end_date: date, split_date: date):
    pass


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
    pass


def patch_employee(id):
    pass


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
