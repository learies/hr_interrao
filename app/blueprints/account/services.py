from app.core.services import BaseService, Repository
from app.core.types import Model


class AccountService(BaseService[Model, Repository]):
    """Базовый сервис для работы с данными из аккаунта."""
