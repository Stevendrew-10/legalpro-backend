from pydantic import BaseModel, Field
from typing import Optional, List, Literal

CaseStatus = Literal["ABIERTO","EN_PROCESO","CERRADO"]
DeadlineStatus = Literal["PENDIENTE","CUMPLIDO","VENCIDO"]
TaskStatus = Literal["PENDIENTE","EN_PROCESO","COMPLETADA"]

class ClientCreate(BaseModel):
    full_name: str
    email: Optional[str] = None
    phone: Optional[str] = None

class ClientOut(ClientCreate):
    id: int
    class Config:
        from_attributes = True

class TeamMemberCreate(BaseModel):
    full_name: str
    role: Optional[str] = None

class TeamMemberOut(TeamMemberCreate):
    id: int
    class Config:
        from_attributes = True

class CaseCreate(BaseModel):
    case_number: str = Field(..., description="Código/número de caso único")
    client_id: int
    case_type: str
    start_date: str = Field(..., description="ISO YYYY-MM-DD")
    details: Optional[str] = None
    status: CaseStatus = "ABIERTO"

class CaseOut(CaseCreate):
    id: int
    class Config:
        from_attributes = True

class DeadlineCreate(BaseModel):
    case_id: int
    title: str
    due_date: str = Field(..., description="ISO YYYY-MM-DD")
    kind: str
    notes: Optional[str] = None
    remind_days_before: int = Field(3, ge=0)
    status: DeadlineStatus = "PENDIENTE"

class DeadlineOut(DeadlineCreate):
    id: int
    class Config:
        from_attributes = True

class TaskCreate(BaseModel):
    case_id: int
    assigned_to_id: Optional[int] = None
    title: str
    description: Optional[str] = None
    priority: int = Field(2, ge=1, le=3, description="1 alta, 2 media, 3 baja")
    due_date: str = Field(..., description="ISO YYYY-MM-DD")
    status: TaskStatus = "PENDIENTE"

class TaskOut(TaskCreate):
    id: int
    completed_at: Optional[str] = None
    class Config:
        from_attributes = True

class TaskEvidenceCreate(BaseModel):
    task_id: int
    filename: Optional[str] = None
    url: Optional[str] = None
    notes: Optional[str] = None

class TaskEvidenceOut(TaskEvidenceCreate):
    id: int
    created_at: str
    class Config:
        from_attributes = True

class CaseDetail(BaseModel):
    case: CaseOut
    deadlines: List[DeadlineOut]
    tasks: List[TaskOut]

class TaskDetail(BaseModel):
    task: TaskOut
    evidences: List[TaskEvidenceOut]
