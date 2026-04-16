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

    def test_sqlalchemy_database_uri(self) -> None:
        """Тест для URI базы данных"""
        config = load_config(TestingConfig, env={})
        assert config.SQLALCHEMY_DATABASE_URI is not None
        assert config.SQLALCHEMY_DATABASE_URI != ""

    def test_sqlalchemy_database_authorization_uri(self) -> None:
        """Тест для URI базы данных авторизации"""
        config = load_config(TestingConfig, env={})
        assert config.SQLALCHEMY_DATABASE_AUTHORIZATION_URI is not None
        assert config.SQLALCHEMY_DATABASE_AUTHORIZATION_URI != ""

    def test_sqlalchemy_bin(self) -> None:
        """Тест для биндов базы данных"""
        config = load_config(TestingConfig, env={})
        assert config.SQLALCHEMY_BINDS is not None
        assert config.SQLALCHEMY_BINDS != {}
        assert config.SQLALCHEMY_BINDS["authorization"] is not None
        assert (
            config.SQLALCHEMY_BINDS["authorization"]
            == config.SQLALCHEMY_DATABASE_AUTHORIZATION_URI
        )


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

    def test_sqlalchemy_database_authorization_uri(self) -> None:
        """Тест для URI базы данных авторизации"""
        config = load_config(DevelopmentConfig, env={})
        assert config.SQLALCHEMY_DATABASE_AUTHORIZATION_URI is not None
        assert config.SQLALCHEMY_DATABASE_AUTHORIZATION_URI != ""

    def test_sqlalchemy_bin(self) -> None:
        """Тест для биндов базы данных"""
        config = load_config(DevelopmentConfig, env={})
        assert config.SQLALCHEMY_BINDS is not None
        assert config.SQLALCHEMY_BINDS != {}
        assert config.SQLALCHEMY_BINDS["authorization"] is not None
        assert (
            config.SQLALCHEMY_BINDS["authorization"]
            == config.SQLALCHEMY_DATABASE_AUTHORIZATION_URI
        )


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

    def test_sqlalchemy_database_authorization_uri(self) -> None:
        """Тест для URI базы данных авторизации"""
        config = load_config(ProductionConfig, env={})
        assert config.SQLALCHEMY_DATABASE_AUTHORIZATION_URI is not None
        assert config.SQLALCHEMY_DATABASE_AUTHORIZATION_URI != ""

    def test_sqlalchemy_bin(self) -> None:
        """Тест для биндов базы данных"""
        config = load_config(ProductionConfig, env={})
        assert config.SQLALCHEMY_BINDS is not None
        assert config.SQLALCHEMY_BINDS != {}
        assert config.SQLALCHEMY_BINDS["authorization"] is not None
        assert (
            config.SQLALCHEMY_BINDS["authorization"]
            == config.SQLALCHEMY_DATABASE_AUTHORIZATION_URI
        )


class TestLoadConfig:
    """Тесты для загрузки конфигурации"""

    def test_load_secret_key_from_env(self) -> None:
        """Тест для загрузки секретного ключа из переменных окружения"""
        config = load_config(
            DevelopmentConfig,
            env={"DEV_SECRET_KEY": "my-dev-secret"},
        )
        assert config.SECRET_KEY == "my-dev-secret"

    def test_load_database_uri_from_env(self) -> None:
        """Тест для загрузки URI основной базы данных из переменных окружения"""
        config = load_config(
            TestingConfig,
            env={"TEST_SQLALCHEMY_DATABASE_URI": "postgresql://main-db"},
        )
        assert config.SQLALCHEMY_DATABASE_URI == "postgresql://main-db"

    def test_load_authorization_database_uri_from_env(self) -> None:
        """Тест для загрузки URI базы авторизации из переменных окружения"""
        config = load_config(
            TestingConfig,
            env={
                "TEST_SQLALCHEMY_DATABASE_AUTHORIZATION_URI": (
                    "postgresql://authorization-db"
                )
            },
        )
        assert (
            config.SQLALCHEMY_DATABASE_AUTHORIZATION_URI
            == "postgresql://authorization-db"
        )
        assert config.SQLALCHEMY_BINDS["authorization"] == "postgresql://authorization-db"

    def test_load_database_uris_and_binds_from_env(self) -> None:
        """Тест для загрузки обоих URI базы данных и биндов из переменных окружения"""
        config = load_config(
            TestingConfig,
            env={
                "TEST_SQLALCHEMY_DATABASE_URI": "postgresql://main-db",
                "TEST_SQLALCHEMY_DATABASE_AUTHORIZATION_URI": (
                    "postgresql://authorization-db"
                ),
            },
        )
        assert config.SQLALCHEMY_DATABASE_URI == "postgresql://main-db"
        assert (
            config.SQLALCHEMY_DATABASE_AUTHORIZATION_URI
            == "postgresql://authorization-db"
        )
        assert config.SQLALCHEMY_BINDS["authorization"] == "postgresql://authorization-db"

    def test_generate_secret_key_if_env_not_exists(self) -> None:
        """Тест для генерации секретного ключа если переменная окружения не существует"""
        config = load_config(DevelopmentConfig, env={})
        assert isinstance(config.SECRET_KEY, str)
        assert config.SECRET_KEY != ""
        assert len(config.SECRET_KEY) == 64  # token_hex(32)

    def test_returns_config_instance(self) -> None:
        """Тест для возврата экземпляра конфигурации"""
        config = load_config(TestingConfig, env={})
        assert isinstance(config, TestingConfig)

    def test_sqlalchemy_database_uri(self) -> None:
        """Тест для URI базы данных"""
        config = load_config(TestingConfig, env={})
        assert config.SQLALCHEMY_DATABASE_URI is not None
        assert config.SQLALCHEMY_DATABASE_URI != ""

    def test_sqlalchemy_database_authorization_uri(self) -> None:
        """Тест для URI базы данных авторизации"""
        config = load_config(TestingConfig, env={})
        assert config.SQLALCHEMY_DATABASE_AUTHORIZATION_URI is not None
        assert config.SQLALCHEMY_DATABASE_AUTHORIZATION_URI != ""

    def test_sqlalchemy_bin(self) -> None:
        """Тест для биндов базы данных"""
        config = load_config(TestingConfig, env={})
        assert config.SQLALCHEMY_BINDS is not None
        assert config.SQLALCHEMY_BINDS != {}
        assert config.SQLALCHEMY_BINDS["authorization"] is not None
