from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional

class ProductRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    presentation: Optional[str] = None
    description: Optional[str] = None
    brand_id: int = Field(..., gt=0)
    categorie_id: int = Field(..., gt=0)


class ProductResponse(BaseModel):
    id: int
    name: str
    presentation: Optional[str] = None
    description: Optional[str] = None
    brand_id: int
    categorie_id: int

    model_config = ConfigDict(from_attributes=True)