import logging
import sys

from pydantic import BaseSettings, EmailStr
from typing import Optional


MIN_PASSWORD_LENGTH = 3
MIN_LENGTH = 1
MAX_LENGTH = 100
FORMAT = '%Y/%m/%d %H:%M:%S'
SPREADSHEET_ROWS = 100
SPREADSHEET_COLS = 10

SPREADSHEET_BODY = dict(
    properties=dict(
        title=None,
        locale='ru_RU'
    ),
    sheets=[dict(properties=dict(
        sheetType='GRID',
        sheetId=0,
        title='Лист1',
        gridProperties=dict(
            rowCount=SPREADSHEET_ROWS,
            columnCount=SPREADSHEET_COLS
        )
    ))]
)
HEADER = [
    ['Отчёт от', None],
    ['Топ проектов по скорости закрытия.'],
    ['Название проекта', 'Время сбора', 'Описание']
]

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(stream=sys.stdout)
formatter = logging.Formatter(
    '%(asctime)s, %(levelname)s, %(message)s, %(name)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)


class Settings(BaseSettings):
    app_title: str = 'Благотворительный фонд'
    app_description: str = 'Cобираем пожертвования'
    database_url: str = 'sqlite+aiosqlite:///./cat_charity_fund.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    email: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()
