from fastapi import APIRouter, HTTPException, File, UploadFile, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services import FaceService
from app.schemas import RegistrationResponse, DeleteResponse

router = APIRouter(
    tags=['Register Users']
)

@router.post('/register')
async def register_user(student_id:int,
                        photo: UploadFile=File(...),
                        db: AsyncSession = Depends(get_db)
                        ):
    try:
        if not photo.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")

        image_bytes = await photo.read()

        face_service = FaceService(db)

        success, message = await face_service.register_face(
            student_id,
            image_bytes
        )
        return RegistrationResponse(
            success=success,
            student_id=student_id,
            message=message,
            confidence=None
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete('/delete')
async def delete_user(student_id,
                      db: AsyncSession = Depends(get_db)):
    try:
        face_service = FaceService(db)

        success = await face_service.delete_face(student_id)

        return DeleteResponse(
            success = success,
            student_id=student_id,
            message=f"Student {student_id} {'deleted' if success else 'not found'}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

