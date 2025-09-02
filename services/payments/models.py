from sqlalchemy import Column, Integer, String

from .database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    status = Column(String, default="pending")
