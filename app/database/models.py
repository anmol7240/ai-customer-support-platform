
from sqlalchemy import String, Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False
    )

    tickets = relationship(
        "Ticket",
        back_populates="customer"
    )


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    category: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    priority: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    status: Mapped[str] = mapped_column(
    String(20),
    default="OPEN",
    nullable=False
    )

    resolution_notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    customer_rating: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    customer_feedback: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id"),
        nullable=False
    )

    customer = relationship(
        "Customer",
        back_populates="tickets"
    )