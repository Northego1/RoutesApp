import uuid
from datetime import datetime
from typing import Self

from core.config import JwtType


class Token:
    def __init__(
            self: Self,
            id: uuid.UUID,
            user_id: uuid.UUID,
            token: str,
            token_expire: datetime,
            type: JwtType = JwtType.REFRESH,
    ) -> None:
        self.id = id
        self.user_id = user_id
        self.token = token
        self.token_expire = token_expire
        self.type = type
