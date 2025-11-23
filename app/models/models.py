from sqlalchemy import Column, String, Integer, DateTime, LargeBinary, BigInteger
from datetime import datetime
from app.database import Base

class StudentFace(Base):
    __tablename__ = "student_faces"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(BigInteger, unique=True, index=True, nullable=False)
    face_embedding = Column(LargeBinary, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)