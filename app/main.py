from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import List
from fastapi import Path
from sqlalchemy import select
from sqlalchemy import func


from app.database.database import Base, engine, get_db
from app.database import models
from app.schemas.customer import CustomerCreate, CustomerResponse

from app.schemas.customer import CustomerCreate
from app.schemas.ticket import TicketCreate, TicketResponse, TicketUpdate

from app.services.classifier import predict_category
from app.services.priority import detect_priority

# Database tables create karna
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Customer Support Intelligence Platform",
    description=(
        "An AI-powered customer support platform "
        "for ticket classification, priority detection, "
        "resolution tracking and customer feedback."
    ),
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "Customer Support API is running"
    }

@app.get("/db-health")
def database_health(db: Session = Depends(get_db)):
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
def get_customers(db: Session = Depends(get_db)):
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

@app.post(
    "/tickets",
    response_model=TicketResponse
)
def create_ticket(
    ticket: TicketCreate,
    db: Session = Depends(get_db)
):
    customer = db.get(
        models.Customer,
        ticket.customer_id
    )

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    # ML model se category predict
    predicted_category = predict_category(
        ticket.message
    )

    predicted_priority = detect_priority(
        ticket.message
    )

    new_ticket = models.Ticket(
        message=ticket.message,
        category=predicted_category,
        priority=predicted_priority,
        status="OPEN",
        customer_id=ticket.customer_id
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return new_ticket

@app.get(
    "/tickets",
    response_model=list[TicketResponse]
)
def get_tickets(db: Session = Depends(get_db)):
    result = db.execute(
        select(models.Ticket)
    )

    tickets = result.scalars().all()

    return tickets

@app.get(
    "/tickets/{ticket_id}",
    response_model=TicketResponse
)
def get_ticket(
    ticket_id: int,
    db: Session = Depends(get_db)
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

    return ticket

@app.delete("/tickets/{ticket_id}")
def delete_ticket(
    ticket_id: int,
    db: Session = Depends(get_db)
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

@app.put(
    "/tickets/{ticket_id}",
    response_model=TicketResponse
)
def update_ticket(
    ticket_id: int,
    ticket_data: TicketUpdate,
    db: Session = Depends(get_db)
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

    if ticket_data.message is not None:
        ticket.message = ticket_data.message

    if ticket_data.category is not None:
        ticket.category = ticket_data.category

    if ticket_data.priority is not None:
        ticket.priority = ticket_data.priority

    if ticket_data.status is not None:
        ticket.status = ticket_data.status

    if ticket_data.resolution_notes is not None:
       ticket.resolution_notes = ticket_data.resolution_notes

    if ticket_data.customer_rating is not None:
        ticket.customer_rating = ticket_data.customer_rating

    if ticket_data.customer_feedback is not None:
        ticket.customer_feedback = ticket_data.customer_feedback

    db.commit()
    db.refresh(ticket)

    return ticket

@app.get("/analytics/tickets")
def ticket_analytics(
    db: Session = Depends(get_db)
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

@app.post("/predict-category")
def predict_ticket_category(message: str):
    category = predict_category(message)

    return {
        "message": message,
        "predicted_category": category
    }



