from typing import ClassVar, Mapping, Self


class WorkerQuery:
    """Запрос на получение сотрудников по фильтрам."""

    PAGE: ClassVar[int] = 1
    MIN_PER_PAGE: ClassVar[int] = 1
    DEFAULT_PER_PAGE: ClassVar[int] = 20
    MAX_PER_PAGE: ClassVar[int] = 50
    SEARCH_BY: ClassVar[frozenset[str]] = frozenset({"name", "email"})
    FILTER_BY: ClassVar[frozenset[str]] = frozenset({"is_active"})

    def __init__(
        self,
        page: int,
        per_page: int,
        search_by: str | None = None,
        search: str | None = None,
        filter_by: str | None = None,
        filter: bool | None = None,
    ) -> None:
        """Инициализация запроса."""
        self._page: int = self._validate_page(page)
        self._per_page: int = self._validate_per_page(per_page)
        self._search_by: str | None = self._validate_search_by(search_by)
        self._search: str | None = self._validate_search(search)
        self._filter_by: str | None = self._validate_filter_by(filter_by)
        self._filter: bool | None = self._validate_filter(filter)

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
    def search_by(self) -> str | None:
        """Получение способа поиска."""
        return self._search_by

    @property
    def search(self) -> str | None:
        """Получение поискового запроса."""
        return self._search

    @property
    def filter_by(self) -> str | None:
        """Получение фильтрации."""
        return self._filter_by

    @property
    def filter(self) -> bool | None:
        """Получение флага активности."""
        return self._filter

    @classmethod
    def from_request(cls, args: Mapping[str, str]) -> Self:
        """Создание класса из HTTP-запроса."""
        return cls(
            page=int(args.get("page", cls.PAGE)),
            per_page=int(args.get("per_page", cls.DEFAULT_PER_PAGE)),
            search_by=args.get("search_by"),
            search=args.get("search"),
            filter_by=args.get("filter_by"),
            filter=cls._parse_bool(args.get("filter")),
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

    def _validate_search_by(self, search_by: str | None) -> str | None:
        """Валидация способа поиска."""
        if search_by and search_by.lower() in self.SEARCH_BY:
            return search_by.lower()

    def _validate_search(self, search: str | None) -> str | None:
        """Валидация поискового запроса."""
        if search and len(search) >= 3:
            return search.strip().lower()

    def _validate_filter_by(self, filter_by: str | None) -> str | None:
        """Валидация фильтрации."""
        if filter_by and filter_by.lower() in self.FILTER_BY:
            return filter_by.lower()

    def _validate_filter(self, filter: bool | None) -> bool | None:
        """Валидация фильтрации."""
        if filter is not None:
            return filter
        return True
