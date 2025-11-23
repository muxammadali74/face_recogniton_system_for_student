from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import VerifyResponse
from app.services import FaceService
from app.database import get_db


router = APIRouter(
    tags=["Authentication User"]
)


@router.post('/verify', response_model=VerifyResponse)
async def verify_user(student_id: int,
                      photo: UploadFile = File(...),
                      db: AsyncSession = Depends(get_db)):
    try:
        if not photo.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")

        face_service = FaceService(db)
        image_bytes = await photo.read()

        # Отладка
        print(f"DEBUG: Calling verify_face for student {student_id}")
        similarity, is_match = await face_service.verify_face(student_id, image_bytes)
        print(f"DEBUG: Result - similarity={similarity}, is_match={is_match}")

        # Проверка на None
        if similarity is None or is_match is None:
            raise HTTPException(status_code=400, detail="Face verification failed")

        return VerifyResponse(
            success=True,
            student_id=student_id,
            is_verified=is_match,
            confidence=similarity,
            message="Verification completed successfully" if is_match else "Verification failed"
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"ERROR in verify_user: {str(e)}")  # Отладка
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")