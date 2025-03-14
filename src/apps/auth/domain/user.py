import uuid
from typing import Protocol, Self

import bcrypt

from apps.auth.domain.refresh_jwt import RefreshJwt
from core.config import settings as st
from core.exceptions import BaseError

SPEC_SYM = {
    "!", "@", "#", "$", "%", "^",
    "&", "*", "(", ")", "-", "_",
    "+", "=", ">", "<", "?", ":",
}

class UserDomainError(BaseError): ...
class ValidationError(UserDomainError): ...


class User:
    def __init__(
            self: Self,
            id: uuid.UUID,  # noqa: A002
            username: str,
            email: str | None,
            password: bytes | str,
            token_list: list[RefreshJwt] | None = None,
    ) -> None:
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.token_list = token_list


    def swapsert_jwt(self: Self, token: RefreshJwt) -> RefreshJwt | None:
        """
            Replace oldest_token if lenth of oldest_list > settings value
            else just append token into token_list
        """
        if self.token_list is None:
            raise UserDomainError("token list is None")
        if len(self.token_list) >= st.auth.MAX_NUM_OF_REFRESH_JWT:
            older_token = min(self.token_list, key=lambda tok: tok.token_expire)
            self.token_list[self.token_list.index(older_token)] = token
            return older_token
        self.token_list.append(token)


    @property
    def username(self: Self) -> str:
        return self._username

    @username.setter
    def username(self: Self, name: str) -> None:
        if len(name) < st.auth.MIN_USERNAME_LENGTH:
            raise ValidationError(
                detail=f"username should be greater than {st.auth.MIN_USERNAME_LENGTH} characters",
                status_code=401,
            )
        self._username = name


    def _validate_password(self: Self, password: str) -> None:
        """
            Password validator by validations which choosen in settings
        """
        validations = {
            f"Password should be greater than {st.auth.MIN_PASSWORD_LENGTH} characters": \
                len(password) >= st.auth.MIN_PASSWORD_LENGTH,
            "Password should have at least one upper character": \
                any(sym.isupper() for sym in password) if st.auth.REQUIRED_UPPER_SYM else True,
            "Password should have at least one digit": \
                any(sym.isdigit() for sym in password) if st.auth.REQUIRED_DIGIT else True,
            f"Password should have at least one {SPEC_SYM!r} symbol": \
                any(sym in SPEC_SYM for sym in password) if st.auth.REQUIRED_SPEC_SYM else True,
        }

        if not all(validations.values()):
            raise ValidationError(
                detail=[msg for msg, passed in validations.items() if not passed],
                status_code=401,
            )


    @property
    def password(self: Self) -> bytes:
        return self._password


    @password.setter
    def password(self: Self, password: bytes | str) -> None:
        if isinstance(password, str):
            self._validate_password(password)
            self._password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        else:
            self._password = password










