from dotenv import load_dotenv


def init_env() -> None:
    """Инициализация переменных окружения."""
    load_dotenv(override=True)
