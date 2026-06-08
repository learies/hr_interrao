from app.blueprints.parus.pagination import Pagination


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
