from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from .database import Base

class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    cases = relationship("Case", back_populates="client")

class TeamMember(Base):
    __tablename__ = "team_members"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    role = Column(String, nullable=True)
    tasks = relationship("Task", back_populates="assigned_to")

class Case(Base):
    __tablename__ = "cases"
    id = Column(Integer, primary_key=True, index=True)
    case_number = Column(String, nullable=False, unique=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id", ondelete="RESTRICT"), nullable=False)
    case_type = Column(String, nullable=False)
    start_date = Column(String, nullable=False)
    details = Column(String, nullable=True)
    status = Column(String, nullable=False, default="ABIERTO")
    __table_args__ = (CheckConstraint("status IN ('ABIERTO','EN_PROCESO','CERRADO')", name="ck_case_status"),)
    client = relationship("Client", back_populates="cases")
    deadlines = relationship("Deadline", back_populates="case", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="case", cascade="all, delete-orphan")

class Deadline(Base):
    __tablename__ = "deadlines"
    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    due_date = Column(String, nullable=False)
    kind = Column(String, nullable=False)
    notes = Column(String, nullable=True)
    remind_days_before = Column(Integer, nullable=False, default=3)
    status = Column(String, nullable=False, default="PENDIENTE")
    __table_args__ = (
        CheckConstraint("remind_days_before >= 0", name="ck_deadline_remind_nonneg"),
        CheckConstraint("status IN ('PENDIENTE','CUMPLIDO','VENCIDO')", name="ck_deadline_status"),
    )
    case = relationship("Case", back_populates="deadlines")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id", ondelete="CASCADE"), nullable=False)
    assigned_to_id = Column(Integer, ForeignKey("team_members.id", ondelete="SET NULL"), nullable=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    priority = Column(Integer, nullable=False, default=2)
    due_date = Column(String, nullable=False)
    status = Column(String, nullable=False, default="PENDIENTE")
    completed_at = Column(String, nullable=True)
    __table_args__ = (
        CheckConstraint("priority IN (1,2,3)", name="ck_task_priority"),
        CheckConstraint("status IN ('PENDIENTE','EN_PROCESO','COMPLETADA')", name="ck_task_status"),
        UniqueConstraint("case_id", "title", "due_date", name="uq_task_case_title_due"),
    )
    case = relationship("Case", back_populates="tasks")
    assigned_to = relationship("TeamMember", back_populates="tasks")
    evidences = relationship("TaskEvidence", back_populates="task", cascade="all, delete-orphan")

class TaskEvidence(Base):
    __tablename__ = "task_evidences"
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    filename = Column(String, nullable=True)
    url = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    created_at = Column(String, nullable=False)
    task = relationship("Task", back_populates="evidences")
