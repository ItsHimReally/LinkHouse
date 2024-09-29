from pydantic import BaseModel

class UserData(BaseModel):
    table_number: int
    field_name: str
    field_value: str
    uid: str
