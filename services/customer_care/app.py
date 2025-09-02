from datetime import datetime
from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base, relationship, sessionmaker
from services.common.logging import get_logger

logger = get_logger("customer-care-service")
app = FastAPI()

DATABASE_URL = "sqlite:///./customer_care.db"
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"))
    role = relationship("Role")


class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    status = Column(String, default="open")
    created_by = Column(Integer, ForeignKey("users.id"))
    interactions = relationship("Interaction", back_populates="ticket")


class Interaction(Base):
    __tablename__ = "interactions"
    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    ticket = relationship("Ticket", back_populates="interactions")


def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(Role).count() == 0:
            roles = {name: Role(name=name) for name in ["admin", "agent", "viewer"]}
            db.add_all(roles.values())
            db.flush()
            db.add_all(
                [
                    User(username="alice", role=roles["admin"]),
                    User(username="bob", role=roles["agent"]),
                    User(username="carol", role=roles["viewer"]),
                ]
            )
            db.commit()
    finally:
        db.close()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(x_user: str = Header(...), db: Session = Depends(get_db)) -> User:
    user = db.query(User).filter_by(username=x_user).first()
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user


def require_roles(*roles):
    def checker(user: User = Depends(get_current_user)) -> User:
        if user.role.name not in roles:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user

    return checker


class TicketCreate(BaseModel):
    title: str
    description: str


class StatusUpdate(BaseModel):
    status: str


class InteractionCreate(BaseModel):
    message: str


@app.get("/")
async def root():
    logger.info("root accessed", extra={"service": "customer_care"})
    return {"service": "customer_care", "message": "Hello World"}


@app.post("/tickets")
def create_ticket(
    ticket: TicketCreate,
    user: User = Depends(require_roles("admin", "agent", "viewer")),
    db: Session = Depends(get_db),
):
    db_ticket = Ticket(
        title=ticket.title, description=ticket.description, created_by=user.id
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return {"id": db_ticket.id, "status": db_ticket.status}


@app.patch("/tickets/{ticket_id}/status")
def update_status(
    ticket_id: int,
    update: StatusUpdate,
    user: User = Depends(require_roles("admin", "agent")),
    db: Session = Depends(get_db),
):
    ticket = db.query(Ticket).filter_by(id=ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    ticket.status = update.status
    db.commit()
    return {"id": ticket.id, "status": ticket.status}


@app.post("/tickets/{ticket_id}/interactions")
def add_interaction(
    ticket_id: int,
    interaction: InteractionCreate,
    user: User = Depends(require_roles("admin", "agent", "viewer")),
    db: Session = Depends(get_db),
):
    ticket = db.query(Ticket).filter_by(id=ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    db_interaction = Interaction(
        ticket_id=ticket_id, user_id=user.id, message=interaction.message
    )
    db.add(db_interaction)
    db.commit()
    return {"id": db_interaction.id, "message": db_interaction.message}


init_db()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
