from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt, Field


class DonationBase(BaseModel):
    comment: Optional[str] = Field(None, min_length=1)
    full_amount: PositiveInt = Field(...)

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    pass


class UserDonationDB(DonationCreate):
    id: int = Field(...)
    create_date: datetime = datetime.now()

    class Config:
        orm_mode = True


class DonationDB(UserDonationDB):
    fully_invested: bool = Field(False)
    close_date: Optional[datetime] = Field(None)
    user_id: Optional[int] = Field(None)
    invested_amount: int = Field(0)

    class Config:
        orm_mode = True
