from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import Base, engine, get_db
from . import schemas, crud

Base.metadata.create_all(bind=engine)

app = FastAPI(title="LegalPro - Gestión de Casos (SGLPWEB)", version="1.0.0")

@app.get("/health")
def health():
    return {"status": "ok"}

# Clientes
@app.post("/clients", response_model=schemas.ClientOut, status_code=201)
def create_client(payload: schemas.ClientCreate, db: Session = Depends(get_db)):
    return crud.create_client(db, payload)

@app.get("/clients", response_model=list[schemas.ClientOut])
def list_clients(db: Session = Depends(get_db)):
    return crud.list_clients(db)

# Equipo
@app.post("/team-members", response_model=schemas.TeamMemberOut, status_code=201)
def create_team_member(payload: schemas.TeamMemberCreate, db: Session = Depends(get_db)):
    return crud.create_team_member(db, payload)

@app.get("/team-members", response_model=list[schemas.TeamMemberOut])
def list_team_members(db: Session = Depends(get_db)):
    return crud.list_team_members(db)

# Casos
@app.post("/cases", response_model=schemas.CaseOut, status_code=201)
def create_case(payload: schemas.CaseCreate, db: Session = Depends(get_db)):
    return crud.create_case(db, payload)

@app.get("/cases", response_model=list[schemas.CaseOut])
def list_cases(client_id: int | None = None, status: str | None = None, db: Session = Depends(get_db)):
    return crud.list_cases(db, client_id=client_id, status=status)

@app.get("/cases/{case_id}", response_model=schemas.CaseDetail)
def case_detail(case_id: int, db: Session = Depends(get_db)):
    case, deadlines, tasks = crud.get_case_detail(db, case_id)
    return {"case": case, "deadlines": deadlines, "tasks": tasks}

# Plazos / calendario
@app.post("/deadlines", response_model=schemas.DeadlineOut, status_code=201)
def create_deadline(payload: schemas.DeadlineCreate, db: Session = Depends(get_db)):
    return crud.create_deadline(db, payload)

@app.get("/deadlines", response_model=list[schemas.DeadlineOut])
def list_deadlines(case_id: int | None = None, db: Session = Depends(get_db)):
    return crud.list_deadlines(db, case_id=case_id)

# Tareas
@app.post("/tasks", response_model=schemas.TaskOut, status_code=201)
def create_task(payload: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db, payload)

@app.get("/tasks", response_model=list[schemas.TaskOut])
def list_tasks(case_id: int | None = None, status: str | None = None, db: Session = Depends(get_db)):
    return crud.list_tasks(db, case_id=case_id, status=status)

@app.put("/tasks/{task_id}/status/{new_status}", response_model=schemas.TaskOut)
def update_task_status(task_id: int, new_status: str, db: Session = Depends(get_db)):
    if new_status not in ("PENDIENTE","EN_PROCESO","COMPLETADA"):
        raise HTTPException(status_code=400, detail="new_status inválido. Use: PENDIENTE, EN_PROCESO, COMPLETADA")
    return crud.update_task_status(db, task_id, new_status)

@app.post("/task-evidences", response_model=schemas.TaskEvidenceOut, status_code=201)
def add_evidence(payload: schemas.TaskEvidenceCreate, db: Session = Depends(get_db)):
    return crud.add_task_evidence(db, payload)

@app.get("/tasks/{task_id}", response_model=schemas.TaskDetail)
def task_detail(task_id: int, db: Session = Depends(get_db)):
    t, ev = crud.get_task_detail(db, task_id)
    return {"task": t, "evidences": ev}

# Portal cliente (solo lectura)
@app.get("/portal/clients/{client_id}/cases")
def portal_cases(client_id: int, db: Session = Depends(get_db)):
    client, cases = crud.portal_cases_for_client(db, client_id)
    return {"client": client, "cases": cases}

@app.get("/portal/cases/{case_id}", response_model=schemas.CaseDetail)
def portal_case_detail(case_id: int, db: Session = Depends(get_db)):
    case, deadlines, tasks = crud.portal_case_detail(db, case_id)
    return {"case": case, "deadlines": deadlines, "tasks": tasks}
