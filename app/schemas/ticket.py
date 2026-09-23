from pydantic import BaseModel, Field


class TicketCreate(BaseModel):
    message: str
    customer_id: int


class TicketResponse(BaseModel):
    id: int
    message: str
    category: str | None
    priority: str | None
    status: str
    customer_id: int

    # Assigned support agent
    agent_id: int | None = None

    resolution_notes: str | None = None
    customer_rating: int | None = None
    customer_feedback: str | None = None

    model_config = {
        "from_attributes": True
    }


class TicketUpdate(BaseModel):
    message: str | None = None
    category: str | None = None
    priority: str | None = None
    status: str | None = None
    resolution_notes: str | None = None

    customer_rating: int | None = Field(
        default=None,
        ge=1,
        le=5
    )

    customer_feedback: str | None = None

class TicketAssign(BaseModel):
    agent_id: int