import math
from collections.abc import Iterator, Sequence
from typing import Generic, TypeVar

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

    def iter_pages(
        self,
        *,
        left_edge: int = 1,
        left_current: int = 2,
        right_current: int = 3,
        right_edge: int = 1,
    ) -> Iterator[int | None]:
        """Итератор номеров страниц с пропусками для шаблона."""
        last_page = 0
        for page_num in range(1, self.pages + 1):
            if (
                page_num <= left_edge
                or (
                    page_num > self.page - left_current - 1
                    and page_num < self.page + right_current
                )
                or page_num > self.pages - right_edge
            ):
                if last_page + 1 != page_num:
                    yield None
                yield page_num
                last_page = page_num
