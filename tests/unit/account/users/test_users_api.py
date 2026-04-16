from http import HTTPStatus


def test_get_users_route_is_registered(client) -> None:
    """Тест на регистрацию маршрута получения списка пользователей."""
    response = client.get("/api/v1/users")

    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == {"message": "Hello, World!"}
