from datetime import datetime

from app.models import DonationsBase


def invest_mode(
    target: DonationsBase,
    sources: list[DonationsBase]
) -> list[DonationsBase]:
    """Распределяет средства из источников в целевой объект."""
    changed = []
    for source in sources:
        changed.append(source)
        invest_amount = min(
            source.full_amount - source.invested_amount,
            target.full_amount - target.invested_amount
        )
        for obj in (source, target):
            obj.invested_amount += invest_amount
            if obj.invested_amount == obj.full_amount:
                obj.fully_invested = True
                obj.close_date = datetime.now()
        if target.fully_invested:
            break
    return changed
