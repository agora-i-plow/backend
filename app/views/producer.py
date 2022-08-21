from pydantic import BaseModel, Field


class ItemIn(BaseModel):
    product_id: str = Field(..., description="Id продукта")
