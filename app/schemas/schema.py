from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RegistrationRequest(BaseModel):
    student_id: int

class VerifyRequest(BaseModel):
    student_id: int

class DeleteRequest(BaseModel):
    student_id: int


class RegistrationResponse(BaseModel):
    success: bool
    student_id: int
    message: str
    confidence: Optional[float] = None

class VerifyResponse(BaseModel):
    success: bool
    student_id: int
    is_verified: bool
    confidence: float
    message: str

class DeleteResponse(BaseModel):
    success: bool
    student_id: int
    message: str


class IdentifyResponse(BaseModel):
    success: bool
    student_id: Optional[int] = None
    confidence: Optional[int] = None
    message: str



class StudentFaceBase(BaseModel):
    student_id: int


class StudentFaceResponse(StudentFaceBase):
    id:int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True






