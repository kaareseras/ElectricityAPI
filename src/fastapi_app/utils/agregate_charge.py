from datetime import datetime
from typing import Optional

from src.fastapi_app.models.charge import Charge


def aggregate_charges(charges: list[Charge]) -> Optional[Charge]:
    if not charges:
        return None

    # Base fields from the first charge
    first = charges[0]

    aggregated = Charge(
        id=None,  # Assuming this is auto-generated
        chargeowner_id=first.chargeowner_id,
        charge_type=first.charge_type,
        charge_type_code=first.charge_type_code,
        note=" | ".join(filter(None, [c.note for c in charges])),
        description=" | ".join(filter(None, [c.description for c in charges])),
        valid_from=max(c.valid_from for c in charges if c.valid_from),
        valid_to=min(c.valid_to for c in charges if c.valid_to),
        created_at=datetime.now(),  # or leave as None if unused
    )

    # Dynamically set price1 to price24
    for i in range(1, 25):
        total = sum(getattr(c, f"price{i}", 0.0) or 0.0 for c in charges)
        setattr(aggregated, f"price{i}", total)

    return aggregated
