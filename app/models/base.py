from datetime import datetime

from sqlalchemy import Column, Integer, Boolean, DateTime, CheckConstraint

from app.core.db import Base


class DonationsBase(Base):
    __abstract__ = True
    __table_args__ = (
        CheckConstraint('full_amount > 0', name='check_full_amount_positive'),
        CheckConstraint(
            '0 <= invested_amount <= full_amount', name='check_invested_range'
        )
    )
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(
        Integer, default=0, nullable=False, server_default='0'
    )
    fully_invested = Column(
        Boolean, default=False, nullable=False, server_default='false'
    )
    create_date = Column(DateTime, default=datetime.now, nullable=False)
    close_date = Column(DateTime)

    def __init__(self, **kwargs):
        kwargs.setdefault('invested_amount', 0)
        kwargs.setdefault('fully_invested', False)
        kwargs.setdefault('create_date', datetime.now())
        super().__init__(**kwargs)

    def __repr__(self):
        return (
            f'{type(self).__name__}'
            f'{self.id=}, '
            f'{self.full_amount=}, '
            f'{self.invested_amount=},'
            f'{self.create_date=}, '
            f'{self.close_date=}'
        )
