from flask import g

from .services import WorkerService, build_worker_service


def get_worker_service() -> WorkerService:
    """Получение сервиса для работы с сотрудниками."""
    services = g.setdefault("_services", {})
    if "parus.workers" not in services:
        services["parus.workers"] = build_worker_service()
    return services["parus.workers"]
