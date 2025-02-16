# Pydantic models for structured responses.
from pydantic import BaseModel

class ParentSequence(BaseModel):
    sequence: str

class Variant(BaseModel):
    id: str
    mutation: str
    position: int
    wild_type: str
    mutant: str
    properties: dict[str, float | None]  # Property values are numeric or None.

class PropertiesList(BaseModel):
    properties: list[str]