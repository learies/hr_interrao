import math
from typing import Generic, Sequence, TypeVar

T = TypeVar("T")


class Pagination(Generic[T]):
    """Класс для пагинации."""

    def __init__(
        self, items: Sequence[T], page: int, per_page: int, total: int
    ) -> None:
        """Инициализация класса."""
        self.items: Sequence[T] = items
        self.page: int = page
        self.per_page: int = per_page
        self.total: int = total

    @property
    def pages(self) -> int:
        """Количество страниц."""
        return math.ceil(self.total / self.per_page) if self.per_page else 0
