from typing import TypeVar

from ..settings.database import BaseModel

Model = TypeVar("Model", bound=BaseModel)
