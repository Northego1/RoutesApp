import random
import uuid
from typing import Callable

import pytest

from apps.auth.domain.user import User, UserDomainError
from core.config import settings


def generate_string(
        length: int,
        uppers: bool = True,
        digits: bool = True,
        spec_sym: bool = True,
    ) -> str:
    base_chars = "abcdefghijklmnopqrstuvwxyz"

    password = []
    password.append("A") if uppers else None
    password.append("1") if digits else None
    password.append("!") if spec_sym else None

    if length - len(password) > 0:
        password.extend(
            random.choice(base_chars) for _ in range(length - len(password))
        )
    return "".join(password)


def create_user() -> User:
    return User(
        id=uuid.uuid4(),
        username=generate_string(settings.auth.MIN_USERNAME_LENGTH),
        password=generate_string(settings.auth.MIN_PASSWORD_LENGTH),
        email=None,
    )

def username_lenght_test() -> None:
    with pytest.raises(UserDomainError):
        create_user().username = generate_string(settings.auth.MIN_USERNAME_LENGTH - 1)


def password_length_test() -> None:
    with pytest.raises(UserDomainError):
        create_user().password = generate_string(settings.auth.MIN_PASSWORD_LENGTH - 1)


def required_digit_test() -> None:
    with pytest.raises(UserDomainError):
        create_user().password = generate_string(
            settings.auth.MIN_PASSWORD_LENGTH,
            digits=False,
        )


def required_upper_case_test() -> None:
    with pytest.raises(UserDomainError):
        create_user().password = generate_string(
            settings.auth.MIN_PASSWORD_LENGTH,
            uppers=False,
        )

def required_spec_sym_test() -> None:
    with pytest.raises(UserDomainError):
        create_user().password = generate_string(
            settings.auth.MIN_PASSWORD_LENGTH,
            spec_sym=False,
        )


tests = []
tests.append(password_length_test)
tests.append(username_lenght_test)

if settings.auth.REQUIRED_UPPER_SYM:
    tests.append(required_upper_case_test)
if settings.auth.REQUIRED_SPEC_SYM:
    tests.append(required_spec_sym_test)
if settings.auth.REQUIRED_DIGIT:
    tests.append(required_digit_test)


@pytest.mark.parametrize(
        "test_func",
        tests,
)
def test_user(
    test_func: Callable[..., None],
) -> None:
    test_func()

