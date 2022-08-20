from fastapi import Depends
from uuid import UUID
from pydantic import BaseModel, Field
from app.models.base.base_user import Roles
from app.utils.auth import get_current_user

class ItemIn(BaseModel):
    product_id: str = Field(..., description='Id продукта')