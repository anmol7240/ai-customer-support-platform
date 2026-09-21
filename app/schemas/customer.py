from pydantic import BaseModel, EmailStr, ConfigDict


class CustomerCreate(BaseModel):
    name: str
    email: EmailStr

class CustomerResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)