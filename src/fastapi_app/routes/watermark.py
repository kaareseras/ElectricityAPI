from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.fastapi_app.config.database import get_db_session
from src.fastapi_app.config.security import get_current_admin
from src.fastapi_app.responses.watermark import WatermarkResponse
from src.fastapi_app.services import watermark

watermark_router = APIRouter(
    prefix="/watermark",
    tags=["Watermark"],
    responses={404: {"description": "Not found"}},
)


@watermark_router.get("", status_code=status.HTTP_200_OK, response_model=WatermarkResponse)
async def get_watermark_info(session: Session = Depends(get_db_session), user=Depends(get_current_admin)):
    return await watermark.fetch_watermark(session)
