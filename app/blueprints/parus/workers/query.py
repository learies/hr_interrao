from typing import ClassVar, Mapping, Self


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
        search: str | None = None,
        is_active: bool | None = None,
        is_admin: bool | None = None,
    ) -> None:
        """Инициализация запроса."""
        self._page: int = self._validate_page(page)
        self._per_page: int = self._validate_per_page(per_page)
        self._search: str | None = self._validate_search(search)
        self._is_active: bool | None = is_active
        self._is_admin: bool | None = is_admin

    @property
    def page(self) -> int:
        """Получение страницы."""
        return self._page

    @property
    def per_page(self) -> int:
        """Получение количества элементов на странице."""
        return self._per_page

    @property
    def offset(self) -> int:
        """Получение смещения."""
        return (self._page - 1) * self._per_page

    @property
    def limit(self) -> int:
        """Получение лимита."""
        return self._per_page

    @property
    def search(self) -> str | None:
        """Получение поискового запроса."""
        return self._search

    @property
    def is_active(self) -> bool | None:
        """Получение флага активности."""
        return self._is_active

    @property
    def is_admin(self) -> bool | None:
        """Получение флага администратора."""
        return self._is_admin

    @classmethod
    def from_request(cls, args: Mapping[str, str]) -> Self:
        """Создание класса из HTTP-запроса."""
        return cls(
            page=int(args.get("page", cls.PAGE)),
            per_page=int(args.get("per_page", cls.DEFAULT_PER_PAGE)),
            search=args.get("search"),
            is_active=cls._parse_bool(args.get("is_active")),
            is_admin=cls._parse_bool(args.get("is_admin")),
        )

    @staticmethod
    def _parse_bool(value: str | None) -> bool | None:
        """Парсинг boolean из query string."""
        return value.lower() in ("true", "1", "yes") if value else None

    def _validate_page(self, page: int) -> int:
        """Валидация страницы."""
        return max(self.PAGE, page)

    def _validate_per_page(self, per_page: int) -> int:
        """Валидация количества элементов на странице."""
        return max(self.MIN_PER_PAGE, min(per_page, self.MAX_PER_PAGE))

    def _validate_search(self, search: str | None) -> str | None:
        """Валидация поискового запроса."""
        if search and len(search) >= 3:
            return search.strip().lower()
