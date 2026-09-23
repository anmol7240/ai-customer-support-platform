from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text, select, func
from sqlalchemy.orm import Session
from typing import List

from app.database.database import Base, engine, get_db
from app.core.security import get_current_user, require_role
from app.database import models

from app.schemas.customer import CustomerCreate, CustomerResponse
from app.schemas.ticket import (
    TicketCreate,
    TicketResponse,
    TicketUpdate,
    TicketAssign
)

from app.services.classifier import predict_category
from app.services.priority import detect_priority

from app.api.agents import router as agents_router
from app.api.auth import router as auth_router


# =========================================================
# DATABASE TABLES
# =========================================================

Base.metadata.create_all(bind=engine)


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="AI Customer Support Intelligence Platform",
    description=(
        "An AI-powered customer support platform "
        "for ticket classification, priority detection, "
        "resolution tracking and customer feedback."
    ),
    version="1.0.0"
)


# =========================================================
# ROUTERS
# =========================================================

app.include_router(agents_router)
app.include_router(auth_router)


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():
    return {
        "message": "Customer Support API is running"
    }


# =========================================================
# DATABASE HEALTH
# =========================================================

@app.get("/db-health")
def database_health(
    db: Session = Depends(get_db)
):
    try:
        db.execute(text("SELECT 1"))

        return {
            "status": "success",
            "message": "Database connected successfully"
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Database connection failed"
        )


# =========================================================
# CUSTOMER APIs
# =========================================================

@app.post("/customers")
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db)
):
    new_customer = models.Customer(
        name=customer.name,
        email=customer.email
    )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer


@app.get(
    "/customers",
    response_model=List[CustomerResponse]
)
def get_customers(
    db: Session = Depends(get_db)
):
    result = db.execute(
        select(models.Customer)
    )

    customers = result.scalars().all()

    return customers


@app.get(
    "/customers/{customer_id}",
    response_model=CustomerResponse
)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):
    customer = db.get(
        models.Customer,
        customer_id
    )

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer


# =========================================================
# CREATE TICKET
# CUSTOMER ONLY
# =========================================================

@app.post(
    "/tickets",
    response_model=TicketResponse
)
def create_ticket(
    ticket: TicketCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("customer"))
):
    # Customer can only create tickets for their own account
    if current_user.customer_id != ticket.customer_id:
        raise HTTPException(
            status_code=403,
            detail="You can only create tickets for your own account"
        )

    customer = db.get(
        models.Customer,
        ticket.customer_id
    )

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    # AI category prediction
    predicted_category = predict_category(
        ticket.message
    )

    # AI priority detection
    predicted_priority = detect_priority(
        ticket.message
    )

    new_ticket = models.Ticket(
        message=ticket.message,
        category=predicted_category,
        priority=predicted_priority,
        status="OPEN",
        customer_id=current_user.customer_id
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return new_ticket


# =========================================================
# GET ALL / OWN TICKETS
# =========================================================

@app.get(
    "/tickets",
    response_model=list[TicketResponse]
)
def get_tickets(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # Customer can see ONLY their own tickets
    if current_user.role == "customer":

        if current_user.customer_id is None:
            raise HTTPException(
                status_code=400,
                detail="Customer account is not linked to a customer"
            )

        result = db.execute(
            select(models.Ticket).where(
                models.Ticket.customer_id
                == current_user.customer_id
            )
        )

        return result.scalars().all()

    # Agent can see ALL tickets
    if current_user.role == "agent":

        result = db.execute(
            select(models.Ticket)
        )

        return result.scalars().all()

    raise HTTPException(
        status_code=403,
        detail="Invalid user role"
    )


# =========================================================
# GET SINGLE TICKET
# =========================================================

@app.get(
    "/tickets/{ticket_id}",
    response_model=TicketResponse
)
def get_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    ticket = db.get(
        models.Ticket,
        ticket_id
    )

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    # Customer can ONLY view their own ticket
    if current_user.role == "customer":

        if ticket.customer_id != current_user.customer_id:
            raise HTTPException(
                status_code=403,
                detail="You can only access your own tickets"
            )

    # Only customer or agent
    if current_user.role not in [
        "customer",
        "agent"
    ]:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission"
        )

    return ticket


# =========================================================
# DELETE TICKET
# AGENT ONLY
# =========================================================

@app.delete("/tickets/{ticket_id}")
def delete_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("agent"))
):
    ticket = db.get(
        models.Ticket,
        ticket_id
    )

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    db.delete(ticket)
    db.commit()

    return {
        "message": "Ticket deleted successfully",
        "ticket_id": ticket_id
    }


# =========================================================
# UPDATE TICKET
# AGENT ONLY
# =========================================================

@app.put(
    "/tickets/{ticket_id}",
    response_model=TicketResponse
)
def update_ticket(
    ticket_id: int,
    ticket_data: TicketUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("agent"))
):
    ticket = db.get(
        models.Ticket,
        ticket_id
    )

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    # Agent can update message
    if ticket_data.message is not None:
        ticket.message = ticket_data.message

    # Agent can update category
    if ticket_data.category is not None:
        ticket.category = ticket_data.category

    # Agent can update priority
    if ticket_data.priority is not None:
        ticket.priority = ticket_data.priority

    # Agent can update status
    if ticket_data.status is not None:

        allowed_statuses = [
            "OPEN",
            "IN_PROGRESS",
            "RESOLVED"
        ]

        if ticket_data.status not in allowed_statuses:
            raise HTTPException(
                status_code=400,
                detail="Invalid status. Use OPEN, IN_PROGRESS or RESOLVED"
            )

        ticket.status = ticket_data.status

    # Agent can add resolution notes
    if ticket_data.resolution_notes is not None:
        ticket.resolution_notes = (
            ticket_data.resolution_notes
        )

    # IMPORTANT:
    # customer_rating and customer_feedback
    # are NOT updated here.

    db.commit()
    db.refresh(ticket)

    return ticket


# =========================================================
# CUSTOMER FEEDBACK / RATING
# CUSTOMER ONLY
# =========================================================

@app.put(
    "/tickets/{ticket_id}/feedback",
    response_model=TicketResponse
)
def submit_feedback(
    ticket_id: int,
    ticket_data: TicketUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("customer"))
):
    ticket = db.get(
        models.Ticket,
        ticket_id
    )

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    # Customer can only give feedback
    # on their own ticket
    if ticket.customer_id != current_user.customer_id:
        raise HTTPException(
            status_code=403,
            detail="You can only give feedback on your own tickets"
        )

    # Feedback should be given after resolution
    if ticket.status != "RESOLVED":
        raise HTTPException(
            status_code=400,
            detail="Feedback can only be submitted after ticket is resolved"
        )

    # Rating
    if ticket_data.customer_rating is not None:

        if not 1 <= ticket_data.customer_rating <= 5:
            raise HTTPException(
                status_code=400,
                detail="Rating must be between 1 and 5"
            )

        ticket.customer_rating = (
            ticket_data.customer_rating
        )

    # Feedback
    if ticket_data.customer_feedback is not None:
        ticket.customer_feedback = (
            ticket_data.customer_feedback
        )

    # At least one feedback field required
    if (
        ticket_data.customer_rating is None
        and ticket_data.customer_feedback is None
    ):
        raise HTTPException(
            status_code=400,
            detail="Please provide rating or feedback"
        )

    db.commit()
    db.refresh(ticket)

    return ticket


# =========================================================
# ASSIGN TICKET
# AGENT ONLY
# =========================================================

@app.put(
    "/tickets/{ticket_id}/assign",
    response_model=TicketResponse
)
def assign_ticket(
    ticket_id: int,
    assignment: TicketAssign,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("agent"))
):
    # Check ticket
    ticket = db.get(
        models.Ticket,
        ticket_id
    )

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    # Check agent
    agent = db.get(
        models.Agent,
        assignment.agent_id
    )

    if agent is None:
        raise HTTPException(
            status_code=404,
            detail="Agent not found"
        )

    # Assign ticket to agent
    ticket.agent_id = agent.id

    # Automatically move ticket to IN_PROGRESS
    if ticket.status == "OPEN":
        ticket.status = "IN_PROGRESS"

    db.commit()
    db.refresh(ticket)

    return ticket


# =========================================================
# ANALYTICS
# AGENT ONLY
# =========================================================

@app.get("/analytics/tickets")
def ticket_analytics(
    db: Session = Depends(get_db),
    current_user=Depends(require_role("agent"))
):
    total_tickets = db.query(
        func.count(models.Ticket.id)
    ).scalar()

    high_priority = db.query(
        func.count(models.Ticket.id)
    ).filter(
        models.Ticket.priority == "HIGH"
    ).scalar()

    critical_priority = db.query(
        func.count(models.Ticket.id)
    ).filter(
        models.Ticket.priority == "CRITICAL"
    ).scalar()

    open_tickets = db.query(
        func.count(models.Ticket.id)
    ).filter(
        models.Ticket.status == "OPEN"
    ).scalar()

    resolved_tickets = db.query(
        func.count(models.Ticket.id)
    ).filter(
        models.Ticket.status == "RESOLVED"
    ).scalar()

    return {
        "total_tickets": total_tickets,
        "high_priority_tickets": high_priority,
        "critical_priority_tickets": critical_priority,
        "open_tickets": open_tickets,
        "resolved_tickets": resolved_tickets
    }


# =========================================================
# AI CATEGORY PREDICTION
# =========================================================

@app.post("/predict-category")
def predict_ticket_category(
    message: str
):
    category = predict_category(message)

    return {
        "message": message,
        "predicted_category": category
    }