from enum import Enum
from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")
D = TypeVar("D")

class Status(str, Enum):
    SUCCESS = "SUCCES"
    FAILURE = "FAILURE"


class ApiResponse(BaseModel, Generic[T, D]):
    status: Status = Field(examples=["SUCCESS | FAILURE"], default=Status.SUCCESS)
    detail: D | None = None
    data: T | None = None



class ValidationResponseDetails(BaseModel):
    loc: list[str | int]
    msg: str
    type: str


