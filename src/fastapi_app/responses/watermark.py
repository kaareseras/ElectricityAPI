from datetime import datetime

from src.fastapi_app.responses.base import BaseResponse


class WatermarkResponse(BaseResponse):
    spotprices_max_date: datetime
    charges_max_date: datetime
    taxes_max_date: datetime
    tarifs_max_date: datetime
