import os
import secrets
from typing import Mapping


class Config:
    """Конфигурация приложения"""

    DEBUG: bool = False
    TESTING: bool = False
    SECRET_KEY_ENV_NAME: str = ""


class ProductionConfig(Config):
    """Конфигурация для производства"""

    DEBUG: bool = False
    SECRET_KEY_ENV_NAME: str = "PROD_SECRET_KEY"


class DevelopmentConfig(Config):
    """Конфигурация для разработки"""

    DEBUG: bool = True
    SECRET_KEY_ENV_NAME: str = "DEV_SECRET_KEY"


class TestingConfig(Config):
    """Конфигурация для тестирования"""

    TESTING: bool = True
    SECRET_KEY_ENV_NAME: str = "TEST_SECRET_KEY"


def _load_secret_key(secret_key_env_name: str, env_vars: Mapping[str, str]) -> str:
    """Загрузка секретного ключа из переменных окружения"""
    return env_vars.get(secret_key_env_name, secrets.token_hex(32))


def load_config(
    config_class: type[Config], *, env: Mapping[str, str] | None = None
) -> Config:
    """Загрузка конфигурации"""
    # Получение переменных окружения
    env_vars: Mapping[str, str] = env or os.environ

    # Создание конфигурации
    config = config_class()

    # Загрузка секретного ключа
    config.SECRET_KEY_ENV_NAME = _load_secret_key(config.SECRET_KEY_ENV_NAME, env_vars)

    return config
