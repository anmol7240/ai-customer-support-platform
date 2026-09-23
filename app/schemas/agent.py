from pydantic import BaseModel, EmailStr, ConfigDict


class AgentCreate(BaseModel):
    name: str
    email: EmailStr


class AgentResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)