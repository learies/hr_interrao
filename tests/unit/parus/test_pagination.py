import math

import pytest

from app.blueprints.parus.pagination import Pagination


@pytest.mark.parametrize(
    ("total", "per_page", "expected_pages"),
    [
        (100, 10, 10),
        (25, 10, 3),
        (0, 10, 0),
        (1, 10, 1),
        (10, 0, 0),
    ],
)
def test_pages_calculates_page_count(
    total: int, per_page: int, expected_pages: int
) -> None:
    """Проверяет расчёт количества страниц."""
    pagination = Pagination(items=(), page=1, per_page=per_page, total=total)

    assert pagination.pages == expected_pages
    if per_page:
        assert pagination.pages == math.ceil(total / per_page)


def test_iter_pages_shows_edges_and_current_window() -> None:
    """Проверяет номера страниц в начале, конце и вокруг текущей."""
    pagination = Pagination(items=(), page=10, per_page=10, total=200)

    assert list(pagination.iter_pages()) == [
        1,
        None,
        8,
        9,
        10,
        11,
        12,
        None,
        20,
    ]


def test_iter_pages_returns_all_pages_when_few() -> None:
    """Проверяет вывод всех страниц без пропусков."""
    pagination = Pagination(items=(), page=2, per_page=10, total=30)

    assert list(pagination.iter_pages()) == [1, 2, 3]


def test_iter_pages_on_first_page() -> None:
    """Проверяет вывод страниц для первой страницы."""
    pagination = Pagination(items=(), page=1, per_page=10, total=200)

    assert list(pagination.iter_pages()) == [1, 2, 3, None, 20]


def test_iter_pages_on_last_page() -> None:
    """Проверяет вывод страниц для последней страницы."""
    pagination = Pagination(items=(), page=20, per_page=10, total=200)

    assert list(pagination.iter_pages()) == [1, None, 18, 19, 20]


def test_iter_pages_returns_empty_when_no_pages() -> None:
    """Проверяет пустой итератор при отсутствии страниц."""
    pagination = Pagination(items=(), page=1, per_page=10, total=0)

    assert list(pagination.iter_pages()) == []


def test_iter_pages_single_page() -> None:
    """Проверяет вывод единственной страницы."""
    pagination = Pagination(items=(), page=1, per_page=10, total=5)

    assert list(pagination.iter_pages()) == [1]


def test_iter_pages_respects_custom_window() -> None:
    """Проверяет настройку окна вокруг текущей страницы."""
    pagination = Pagination(items=(), page=10, per_page=10, total=200)

    assert list(
        pagination.iter_pages(
            left_edge=1,
            left_current=1,
            right_current=1,
            right_edge=1,
        )
    ) == [1, None, 9, 10, None, 20]
