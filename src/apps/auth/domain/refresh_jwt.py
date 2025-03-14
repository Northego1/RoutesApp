from datetime import datetime
from typing import Self
import uuid


class RefreshJwt:
    def __init__(
            self: Self,
            id: uuid.UUID,
            user_id: uuid.UUID,
            token: str,
            token_expire: datetime,
    ) -> None:
        self.id = id
        self.user_id = user_id
        self.token = token
        self.token_expire = token_expire
