from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from . import models, schemas

def create_client(db: Session, data: schemas.ClientCreate):
    c = models.Client(**data.model_dump())
    db.add(c); db.commit(); db.refresh(c)
    return c

def list_clients(db: Session):
    return db.query(models.Client).order_by(models.Client.id.desc()).all()

def create_team_member(db: Session, data: schemas.TeamMemberCreate):
    m = models.TeamMember(**data.model_dump())
    db.add(m); db.commit(); db.refresh(m)
    return m

def list_team_members(db: Session):
    return db.query(models.TeamMember).order_by(models.TeamMember.id.desc()).all()

def create_case(db: Session, data: schemas.CaseCreate):
    exists = db.query(models.Case).filter(models.Case.case_number == data.case_number).first()
    if exists:
        raise HTTPException(status_code=409, detail="Ya existe un caso con ese número/código.")
    client = db.get(models.Client, data.client_id)
    if not client:
        raise HTTPException(status_code=400, detail="client_id inválido (cliente no existe).")
    case = models.Case(**data.model_dump())
    db.add(case); db.commit(); db.refresh(case)
    return case

def list_cases(db: Session, client_id: int | None = None, status: str | None = None):
    q = db.query(models.Case)
    if client_id is not None:
        q = q.filter(models.Case.client_id == client_id)
    if status is not None:
        q = q.filter(models.Case.status == status)
    return q.order_by(models.Case.id.desc()).all()

def get_case_detail(db: Session, case_id: int):
    case = db.get(models.Case, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Caso no encontrado.")
    deadlines = db.query(models.Deadline).filter(models.Deadline.case_id == case_id).order_by(models.Deadline.due_date.asc()).all()
    tasks = db.query(models.Task).filter(models.Task.case_id == case_id).order_by(models.Task.due_date.asc()).all()
    return case, deadlines, tasks

def create_deadline(db: Session, data: schemas.DeadlineCreate):
    case = db.get(models.Case, data.case_id)
    if not case:
        raise HTTPException(status_code=400, detail="case_id inválido (caso no existe).")
    d = models.Deadline(**data.model_dump())
    db.add(d); db.commit(); db.refresh(d)
    return d

def list_deadlines(db: Session, case_id: int | None = None):
    q = db.query(models.Deadline)
    if case_id is not None:
        q = q.filter(models.Deadline.case_id == case_id)
    return q.order_by(models.Deadline.due_date.asc()).all()

def create_task(db: Session, data: schemas.TaskCreate):
    case = db.get(models.Case, data.case_id)
    if not case:
        raise HTTPException(status_code=400, detail="case_id inválido (caso no existe).")
    if data.assigned_to_id is not None:
        member = db.get(models.TeamMember, data.assigned_to_id)
        if not member:
            raise HTTPException(status_code=400, detail="assigned_to_id inválido (miembro no existe).")
    t = models.Task(**data.model_dump(), completed_at=None)
    db.add(t); db.commit(); db.refresh(t)
    return t

def update_task_status(db: Session, task_id: int, status: str):
    t = db.get(models.Task, task_id)
    if not t:
        raise HTTPException(status_code=404, detail="Tarea no encontrada.")
    t.status = status
    if status == "COMPLETADA":
        t.completed_at = datetime.now().isoformat(timespec="seconds")
    db.commit(); db.refresh(t)
    return t

def list_tasks(db: Session, case_id: int | None = None, status: str | None = None):
    q = db.query(models.Task)
    if case_id is not None:
        q = q.filter(models.Task.case_id == case_id)
    if status is not None:
        q = q.filter(models.Task.status == status)
    return q.order_by(models.Task.due_date.asc()).all()

def get_task_detail(db: Session, task_id: int):
    t = db.get(models.Task, task_id)
    if not t:
        raise HTTPException(status_code=404, detail="Tarea no encontrada.")
    ev = db.query(models.TaskEvidence).filter(models.TaskEvidence.task_id == task_id).order_by(models.TaskEvidence.id.desc()).all()
    return t, ev

def add_task_evidence(db: Session, data: schemas.TaskEvidenceCreate):
    t = db.get(models.Task, data.task_id)
    if not t:
        raise HTTPException(status_code=400, detail="task_id inválido (tarea no existe).")
    e = models.TaskEvidence(
        task_id=data.task_id,
        filename=data.filename,
        url=data.url,
        notes=data.notes,
        created_at=datetime.now().isoformat(timespec="seconds")
    )
    db.add(e); db.commit(); db.refresh(e)
    return e

def portal_cases_for_client(db: Session, client_id: int):
    client = db.get(models.Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado.")
    return client, list_cases(db, client_id=client_id)

def portal_case_detail(db: Session, case_id: int):
    return get_case_detail(db, case_id)
