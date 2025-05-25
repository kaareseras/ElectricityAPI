from src.fastapi_app.models.charge import Charge


def compare_charges(charge1: Charge, charge2: Charge) -> bool:
    """
    Compare two Charge objects for equality based on their attributes.

    Args:
        charge1 (Charge): The first Charge object to compare.
        charge2 (Charge): The second Charge object to compare.

    Returns:
        bool: True if all attributes are equal, False otherwise.
    """
    attributes = [
        "chargeowner_id",
        "charge_type",
        "charge_type_code",
        "note",
        "description",
        "price1",
        "price2",
        "price3",
        "price4",
        "price5",
        "price6",
        "price7",
        "price8",
        "price9",
        "price10",
        "price11",
        "price12",
        "price13",
        "price14",
        "price15",
        "price16",
        "price17",
        "price18",
        "price19",
        "price20",
        "price21",
        "price22",
        "price23",
        "price24",
    ]

    return all(getattr(charge1, attr) == getattr(charge2, attr) for attr in attributes)
