from app.blueprints.parus.workers.query import WorkerQuery


def test_worker_query_uses_default_values_when_request_args_are_empty() -> None:
    """Проверяет значения по умолчанию для пустого query string."""
    query = WorkerQuery.from_request({})

    assert query.page == 1
    assert query.per_page == 20
    assert query.offset == 0
    assert query.limit == 20
    assert query.search is None
    assert query.is_active is None
    assert query.is_admin is None


def test_worker_query_calculates_offset_and_limit_from_page_and_per_page() -> None:
    """Проверяет расчет offset и limit по page и per_page."""
    query = WorkerQuery.from_request({"page": "2", "per_page": "10"})

    assert query.page == 2
    assert query.per_page == 10
    assert query.offset == 10
    assert query.limit == 10
