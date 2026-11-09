from pydantic import BaseModel, ConfigDict


class UserRead(BaseModel):
    # параметр позволяет получать значения из атрибутов Python-объекта
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
