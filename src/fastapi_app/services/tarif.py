from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy import and_, or_

from src.fastapi_app.config.config import get_settings
from src.fastapi_app.models.tarif import Tarif
from src.fastapi_app.responses.tarif import TarifResponse

settings = get_settings()


async def fetch_tarif_details(data, session):
    tarif = session.query(Tarif).filter(Tarif.id == data).first()
    _error = ""
    if not tarif:
        raise HTTPException(status_code=404, detail="Tarif not found.")

    my_tarif = TarifResponse(
        id=tarif.id,
        valid_from=tarif.valid_from,
        valid_to=tarif.valid_to,
        nettarif=tarif.nettarif,
        systemtarif=tarif.systemtarif,
        includingVAT=tarif.includingVAT,
        created_at=tarif.created_at,
        error=_error,
    )

    return my_tarif


async def fetch_tarif_by_date(qdate, session):
    tarif = session.query(Tarif).filter(and_(Tarif.valid_from <= qdate, Tarif.valid_to > qdate)).first()
    _error = ""
    if not tarif:
        raise HTTPException(status_code=404, detail="Tarif not found.")

    my_tarif = TarifResponse(
        id=tarif.id,
        valid_from=tarif.valid_from,
        valid_to=tarif.valid_to,
        nettarif=tarif.nettarif,
        systemtarif=tarif.systemtarif,
        includingVAT=tarif.includingVAT,
        created_at=tarif.created_at,
        error=_error,
    )

    return my_tarif


async def fetch_tarifs(session):
    tarifs = session.query(Tarif).all()
    _error = ""
    if not tarifs:
        raise HTTPException(status_code=404, detail="Tarif not found.")

    my_tarifs = []
    for tarif in tarifs:
        my_tarif = TarifResponse(
            id=tarif.id,
            valid_from=tarif.valid_from,
            valid_to=tarif.valid_to,
            nettarif=tarif.nettarif,
            systemtarif=tarif.systemtarif,
            includingVAT=tarif.includingVAT,
            created_at=tarif.created_at,
            error=_error,
        )
        my_tarifs.append(my_tarif)

    return my_tarifs


async def delete_tarif(data, session):
    tarif = session.query(Tarif).filter(Tarif.id == data).first()
    if not tarif:
        raise HTTPException(status_code=404, detail="Tarif not found.")
    session.delete(tarif)
    session.commit()
    return {"message": "Tarif deleted successfully."}


async def add_tarif(data, session):
    existing_tarif = (
        session.query(Tarif)
        .filter(
            or_(
                and_(Tarif.valid_from <= data.valid_from, Tarif.valid_to > data.valid_from),
                and_(Tarif.valid_from < data.valid_to, Tarif.valid_to >= data.valid_to),
            )
        )
        .first()
    )

    if existing_tarif:
        raise HTTPException(status_code=404, detail="A tarif already exists within the specified date range.")

    tarif = Tarif()
    tarif.valid_from = data.valid_from
    tarif.valid_to = data.valid_to
    tarif.nettarif = data.nettarif
    tarif.systemtarif = data.systemtarif
    tarif.includingVAT = data.includingVAT
    tarif.created_at = datetime.now(timezone.utc)
    session.add(tarif)
    session.commit()
    session.refresh(tarif)

    return await fetch_tarif_details(tarif.id, session)
