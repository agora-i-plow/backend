from pydantic import BaseModel, Field


class DuplicatesCounter(BaseModel):
    duplicates: int = Field(0, description="Number of duplicates")


class ErrorsCounter(BaseModel):
    errors: int = Field(0, description="Number of errors")
