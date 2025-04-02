from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import DonationsBase


class Donation(DonationsBase):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

    def __repr__(self):
        base_repr = super().__repr__()
        return (
            f'{base_repr}, '
            f'{self.used_id=}, '
            f'{self.comment=}'
        )
