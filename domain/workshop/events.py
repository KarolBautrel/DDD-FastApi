from pydantic import BaseModel


class PartChanged(BaseModel):
    part_name: str
    computer_ref: str
    part_ref: str
