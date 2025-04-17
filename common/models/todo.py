import datetime
from dataclasses import dataclass
from typing import Optional
from rococo.models import VersionedModel
from dataclasses import field

@dataclass(repr=False)
class Todo(VersionedModel):
    title: str = field(default=None)
    description: Optional[str] = field(default=None)
    person_id: str = field(default=None)
    is_completed: bool = field(default=False)
    completed_at: Optional[datetime] = field(default=None)

