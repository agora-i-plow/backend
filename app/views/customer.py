from fastapi import Query
from pydantic import BaseModel, Field


class SearchIn(BaseModel):
    search_query: str = Query(..., description="Search query")


class ReferencesOut(BaseModel):
    references: list[dict] = Field([], description="List of references")


class ItemsOut(BaseModel):
    items: list[dict] = Field([], description="List of items")


class MatchedOut(BaseModel):
    items: list[dict] = Field(
        [], example=[{"id": "", "reference_id": ""}, {"id": "", "reference_id": ""}]
    )
