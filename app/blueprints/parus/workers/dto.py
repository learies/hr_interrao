from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any
from uuid import UUID


@dataclass(frozen=True, slots=True)
class WorkerResponseDTO:
    """DTO для ответа на запрос списка сотрудников."""

    id: UUID
    name: str
    email: str
    is_active: bool
    is_admin: bool = False
    last_login: datetime | None = None

    def to_dict(self) -> dict[str, Any]:
        """Преобразование в словарь."""
        return asdict(self)
