from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass(frozen=True, slots=True)
class Product:
    id: int
    name: str
    brand_id: int
    categorie_id: int
    create_by: str
    active: bool
    create_at: Optional[datetime] = None
    update_at: Optional[datetime] = None
    presentation: Optional[str] = None
    description: Optional[str] = None