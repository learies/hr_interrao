from typing import Any, ClassVar, Mapping, Self


class WorkerQuery:
    """Запрос на получение сотрудников по фильтрам."""

    PAGE: ClassVar[int] = 1
    MIN_PER_PAGE: ClassVar[int] = 1
    DEFAULT_PER_PAGE: ClassVar[int] = 20
    MAX_PER_PAGE: ClassVar[int] = 50

    def __init__(
        self,
        page: int,
        per_page: int,
        active: bool | None = True,
    ) -> None:
        """Инициализация запроса."""
        self._page: int = page
        self._per_page: int = per_page
        self._active: bool | None = active

    @property
    def page(self) -> int:
        """Получение страницы."""
        return self._page

    @property
    def per_page(self) -> int:
        """Получение количества элементов на странице."""
        return self._per_page

    @property
    def active(self) -> bool | None:
        """Получение флага активности."""
        return self._active

    @property
    def offset(self) -> int:
        """Получение смещения."""
        return (self._page - 1) * self._per_page

    @property
    def limit(self) -> int:
        """Получение лимита."""
        return self._per_page

    @classmethod
    def from_request(cls, args: Mapping[str, Any]) -> Self:
        """Создание класса из HTTP-запроса."""
        active = cls._parse_bool(args.get("is_active", "true"))
        return cls(
            page=int(args.get("page", cls.PAGE)),
            per_page=int(args.get("per_page", cls.DEFAULT_PER_PAGE)),
            active=active,
        )

    @staticmethod
    def _parse_bool(value: str | None) -> bool | None:
        """Парсинг boolean из query string."""
        if value:
            return value.lower() in ("true", "1", "yes")

    def _validate_page(self, page: int) -> int:
        """Валидация страницы."""
        return max(self.PAGE, page)

    def _validate_per_page(self, per_page: int) -> int:
        """Валидация количества элементов на странице."""
        return max(self.MIN_PER_PAGE, min(per_page, self.MAX_PER_PAGE))
