from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database.database import get_db
from app.database import models
from app.schemas.agent import AgentCreate, AgentResponse


router = APIRouter(
    prefix="/agents",
    tags=["Agents"]
)


@router.post(
    "",
    response_model=AgentResponse
)
def create_agent(
    agent: AgentCreate,
    db: Session = Depends(get_db)
):
    # Check if agent email already exists
    existing_agent = db.execute(
        select(models.Agent).where(
            models.Agent.email == agent.email
        )
    ).scalar_one_or_none()

    if existing_agent:
        raise HTTPException(
            status_code=400,
            detail="Agent with this email already exists"
        )

    new_agent = models.Agent(
        name=agent.name,
        email=agent.email
    )

    db.add(new_agent)
    db.commit()
    db.refresh(new_agent)

    return new_agent


@router.get(
    "",
    response_model=list[AgentResponse]
)
def get_agents(
    db: Session = Depends(get_db)
):
    result = db.execute(
        select(models.Agent)
    )

    return result.scalars().all()


@router.get(
    "/{agent_id}",
    response_model=AgentResponse
)
def get_agent(
    agent_id: int,
    db: Session = Depends(get_db)
):
    agent = db.get(
        models.Agent,
        agent_id
    )

    if agent is None:
        raise HTTPException(
            status_code=404,
            detail="Agent not found"
        )

    return agent