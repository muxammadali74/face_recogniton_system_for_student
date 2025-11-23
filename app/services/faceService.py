import logging
import pickle
import numpy as np
from fastapi import Depends
from datetime import datetime
from sqlalchemy import select
from app.database import get_db
from app.models.models import StudentFace
from app.services import FaceRecognition
from typing import Tuple, Optional
from sqlalchemy.ext.asyncio import AsyncSession

class FaceService:
    def __init__(self, db: AsyncSession):
        self.faceRecognition = FaceRecognition(threshold=0.65)
        self.logger = logging.getLogger(__name__)
        self.db = db

    async def register_face(self, student_id, image_bytes:bytes) -> Tuple[bool, str]:
        try:
            embedding = await self._extract_face_embedding(image_bytes)
            if embedding is None:
                return False, "No face found in image"

            success = await self._save_embedding(student_id, embedding)
            message = None

            if success:
                message = "New face registered for student"
                self.logger.info(f"{message} {student_id}")
            else:
                message = f"Student {student_id} already registered - skipping"
                self.logger.info(message)

            return success, message

        except Exception as e:
            error_msg = f"Registration error: {e}"
            self.logger.error(error_msg)
            return False, error_msg


    async def _extract_face_embedding(self, image_bytes: bytes):
        try:
            embedding = self.faceRecognition.get_face_embedding(image_bytes)
            return embedding

        except Exception as e:
            self.logger.error(f"Error in _extract_face_embedding: {e}")


    async def _save_embedding(self, student_id: int, embedding):
        try:
            embedding_bytes = pickle.dumps(embedding)

            result = await self.db.execute(
                select(StudentFace).where(StudentFace.student_id == student_id)  # ← ИСПРАВЬ!
            )
            existing_face = result.scalar_one_or_none()

            if existing_face:
                existing_face.face_embedding = embedding_bytes
                existing_face.updated_at = datetime.utcnow()
                self.logger.info(f"Face embedding updated for student {student_id}")
            else:
                face_record = StudentFace(
                    student_id =student_id,
                    face_embedding =embedding_bytes
                )
                self.db.add(face_record)
                self.logger.info(f"Face embedding saved for student {student_id}")

            await self.db.commit()
            return True

        except Exception as e:
            self.logger.error(f"Error saving embedding: {e}")
            return False


    async def delete_face(self, student_id: int) -> bool:
        try:
            result = await self.db.execute(
                select(StudentFace).where(StudentFace.student_id == student_id)
            )
            face_record = result.scalar_one_or_none()
            if not face_record:
                self.logger.warning(f"Face data not found for student {student_id}")
                return False
            await self.db.delete(face_record)
            await self.db.commit()
            self.logger.info(f"Face data deleted for student {student_id}")
            return True

        except Exception as e:
            self.logger.error(f"Error deleting face data for student {student_id}: {str(e)}")
            await self.db.rollback()
            return False

    async def verify_face(self, student_id, image_bytes):
        try:
            emb1 = await self._extract_face_embedding(image_bytes)
            if emb1 is None:
                return 0.0, False

            emb2 = await self._load_embedding(student_id)
            if emb2 is None:
                return 0.0, False

            similarity, is_match = self.faceRecognition.compare_faces(emb1, emb2)
            return similarity, is_match

        except Exception as e:
            self.logger.error(f"Error in verify_face: {str(e)}")
            return 0.0, False

    async def _load_embedding(self, student_id: int) -> Optional[np.ndarray]:

        try:
            result = await self.db.execute(
                select(StudentFace).where(StudentFace.student_id == student_id)
            )
            face_record = result.scalar_one_or_none()

            if face_record and face_record.face_embedding:
                return pickle.loads(face_record.face_embedding)

            return None

        except Exception as e:
            self.logger.error(f"Error loading embedding for student {student_id}: {str(e)}")
            return None