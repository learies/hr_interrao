class Config:
    """Конфигурация приложения"""

    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    """Конфигурация для производства"""

    DEBUG = False


class DevelopmentConfig(Config):
    """Конфигурация для разработки"""

    DEBUG = True


class TestingConfig(Config):
    """Конфигурация для тестирования"""

    TESTING = True


def load_config(config_class: type[Config]) -> Config:
    """Загрузка конфигурации"""
    config = config_class()

    return config
