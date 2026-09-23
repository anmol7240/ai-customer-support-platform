from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database.database import get_db
from app.database import models
from app.schemas.agent import AgentCreate, AgentResponse
from app.core.security import hash_password


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
    # Check existing Agent email
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

    # Check existing User email
    existing_user = db.execute(
        select(models.User).where(
            models.User.email == agent.email
        )
    ).scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists"
        )

    # Create Agent
    new_agent = models.Agent(
        name=agent.name,
        email=agent.email
    )

    db.add(new_agent)
    db.flush()

    # Create login User
    new_user = models.User(
        email=agent.email,
        password_hash=hash_password(agent.password),
        role="agent",
        agent_id=new_agent.id
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_agent)
    db.refresh(new_user)

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