from datetime import datetime

from src.fastapi_app.models.charge import Charge  # Replace with actual import
from src.fastapi_app.utils.chargecompare import compare_charges  # Replace with actual import


# Helper to create a charge object
def create_charge(
    chargeowner_id=1,
    charge_type="D03",
    charge_type_code="DT_C_01",
    note="Nettarif C",
    description="Standard tarif",
    prices=None,
    valid_from="2025-04-01T00:00:00",
    valid_to="2025-10-01T00:00:00",
):
    prices = prices or [0.1] * 24
    return Charge(
        chargeowner_id=chargeowner_id,
        charge_type=charge_type,
        charge_type_code=charge_type_code,
        note=note,
        description=description,
        price24=prices[0],
        price1=prices[1],
        price2=prices[2],
        price3=prices[3],
        price4=prices[4],
        price5=prices[5],
        price6=prices[6],
        price7=prices[7],
        price8=prices[8],
        price9=prices[9],
        price10=prices[10],
        price11=prices[11],
        price12=prices[12],
        price13=prices[13],
        price14=prices[14],
        price15=prices[15],
        price16=prices[16],
        price17=prices[17],
        price18=prices[18],
        price19=prices[19],
        price20=prices[20],
        price21=prices[21],
        price22=prices[22],
        price23=prices[23],
        valid_from=datetime.fromisoformat(valid_from),
        valid_to=datetime.fromisoformat(valid_to),
    )


def test_compare_identical_charges():
    c1 = create_charge()
    c2 = create_charge()
    assert compare_charges(c1, c2) is True


def test_compare_with_different_prices():
    c1 = create_charge()
    prices = [0.1] * 23 + [0.2]  # last price is different
    c2 = create_charge(prices=prices)
    assert compare_charges(c1, c2) is False


def test_compare_with_different_metadata():
    c1 = create_charge()
    c2 = create_charge(note="Something else")
    assert compare_charges(c1, c2) is False


def test_compare_with_different_dates_only():
    c1 = create_charge()
    c2 = create_charge(valid_to="2025-12-01T00:00:00")
    assert compare_charges(c1, c2) is True


def test_compare_with_different_chargeowner():
    c1 = create_charge(chargeowner_id=1)
    c2 = create_charge(chargeowner_id=2)
    assert compare_charges(c1, c2) is False
