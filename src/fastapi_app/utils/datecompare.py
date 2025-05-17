from datetime import date, datetime
from typing import Union


def same_day(a: Union[date, datetime], b: Union[date, datetime]) -> bool:
    """
    Returns True if both `a` and `b` represent the same calendar date.
    Accepts both datetime and date objects.
    """
    if isinstance(a, datetime):
        a = a.date()
    if isinstance(b, datetime):
        b = b.date()
    return a == b
