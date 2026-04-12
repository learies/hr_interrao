from app.settings.config import (
    Config,
    DevelopmentConfig,
    ProductionConfig,
    TestingConfig,
    load_config,
)


class TestConfig:
    """Тесты для конфигурации"""

    def test_debug(self) -> None:
        """Тест для режима отладки"""
        config = load_config(TestingConfig, env={})
        assert config.DEBUG is False

    def test_testing(self) -> None:
        """Тест для режима тестирования"""
        config = load_config(TestingConfig, env={})
        assert config.TESTING is True


class TestDevelopmentConfig:
    """Тесты для конфигурации для разработки"""

    def test_debug(self) -> None:
        """Тест для режима отладки"""
        config = load_config(DevelopmentConfig, env={})
        assert config.DEBUG is True

    def test_testing(self) -> None:
        """Тест для режима тестирования"""
        config = load_config(DevelopmentConfig, env={})
        assert config.TESTING is False


class TestProductionConfig:
    """Тесты для конфигурации для производства"""

    config: Config = load_config(ProductionConfig)

    def test_debug(self) -> None:
        """Тест для режима отладки"""
        config = load_config(ProductionConfig, env={})
        assert config.DEBUG is False

    def test_testing(self) -> None:
        """Тест для режима тестирования"""
        config = load_config(ProductionConfig, env={})
        assert config.TESTING is False


class TestLoadConfig:
    """Тесты для загрузки конфигурации"""

    def test_load_secret_key_from_env(self) -> None:
        """Тест для загрузки секретного ключа из переменных окружения"""
        config = load_config(
            DevelopmentConfig,
            env={"DEV_SECRET_KEY": "my-dev-secret"},
        )
        assert config.SECRET_KEY_ENV_NAME == "my-dev-secret"

    def test_generate_secret_key_if_env_not_exists(self) -> None:
        """Тест для генерации секретного ключа если переменная окружения не существует"""
        config = load_config(DevelopmentConfig, env={})
        assert isinstance(config.SECRET_KEY_ENV_NAME, str)
        assert config.SECRET_KEY_ENV_NAME != ""
        assert len(config.SECRET_KEY_ENV_NAME) == 64  # token_hex(32)

    def test_returns_config_instance(self) -> None:
        """Тест для возврата экземпляра конфигурации"""
        config = load_config(TestingConfig, env={})
        assert isinstance(config, TestingConfig)
