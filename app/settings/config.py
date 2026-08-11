import os
import secrets
from collections.abc import Mapping


class Config:
    """Конфигурация приложения"""

    DEBUG: bool = False
    TESTING: bool = False
    SECRET_KEY: str

    SQLALCHEMY_DATABASE_URI: str
    SQLALCHEMY_DATABASE_AUTHORIZATION_URI: str
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_ECHO: bool = False

    SQLALCHEMY_BINDS: Mapping[str, str] = {}


class ProductionConfig(Config):
    """Конфигурация для производства"""

    DEBUG: bool = False
    SECRET_KEY: str = "PROD_SECRET_KEY"
    SQLALCHEMY_DATABASE_URI: str = "PROD_SQLALCHEMY_DATABASE_URI"
    SQLALCHEMY_DATABASE_AUTHORIZATION_URI: str = (
        "PROD_SQLALCHEMY_DATABASE_AUTHORIZATION_URI"
    )


class DevelopmentConfig(Config):
    """Конфигурация для разработки"""

    DEBUG: bool = True
    SECRET_KEY: str = "DEV_SECRET_KEY"
    SQLALCHEMY_DATABASE_URI: str = "DEV_SQLALCHEMY_DATABASE_URI"
    SQLALCHEMY_DATABASE_AUTHORIZATION_URI: str = (
        "DEV_SQLALCHEMY_DATABASE_AUTHORIZATION_URI"
    )


class TestingConfig(Config):
    """Конфигурация для тестирования"""

    TESTING: bool = True
    SECRET_KEY: str = "TEST_SECRET_KEY"
    SQLALCHEMY_DATABASE_URI: str = "TEST_SQLALCHEMY_DATABASE_URI"
    SQLALCHEMY_DATABASE_AUTHORIZATION_URI: str = (
        "TEST_SQLALCHEMY_DATABASE_AUTHORIZATION_URI"
    )


def _load_secret_key(secret_key_env_name: str, env_vars: Mapping[str, str]) -> str:
    """Загрузка секретного ключа из переменных окружения"""
    return env_vars.get(secret_key_env_name, secrets.token_hex(32))


def _load_sqlalchemy_database_uri(
    sqlalchemy_database_uri_env_name: str, env_vars: Mapping[str, str]
) -> str:
    """Загрузка URI базы данных из переменных окружения"""
    return env_vars.get(sqlalchemy_database_uri_env_name, "sqlite:///:memory:")


def load_config(
    config_class: type[Config], *, env: Mapping[str, str] | None = None
) -> Config:
    """Загрузка конфигурации"""
    # Получение переменных окружения
    env_vars: Mapping[str, str] = env or os.environ

    # Создание конфигурации
    config = config_class()

    # Загрузка секретного ключа
    config.SECRET_KEY = _load_secret_key(config.SECRET_KEY, env_vars)

    # Загрузка URI базы данных
    config.SQLALCHEMY_DATABASE_URI = _load_sqlalchemy_database_uri(
        config.SQLALCHEMY_DATABASE_URI, env_vars
    )
    # Загрузка URI базы данных авторизации
    config.SQLALCHEMY_DATABASE_AUTHORIZATION_URI = _load_sqlalchemy_database_uri(
        config.SQLALCHEMY_DATABASE_AUTHORIZATION_URI, env_vars
    )
    config.SQLALCHEMY_BINDS = {
        "authorization": config.SQLALCHEMY_DATABASE_AUTHORIZATION_URI
    }

    return config
