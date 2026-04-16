from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any
from uuid import UUID


@dataclass(frozen=True, slots=True)
class UserResponseDTO:
    """DTO для ответа на запрос списка пользователей."""

    id: UUID
    is_admin: bool
    last_login: datetime | None

    def to_dict(self) -> dict[str, Any]:
        """Преобразование в словарь."""
        return asdict(self)
