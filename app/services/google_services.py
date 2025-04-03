from copy import deepcopy
from datetime import datetime
from typing import List

from aiogoogle import Aiogoogle

from app.models import CharityProject
from app.core.config import (
    settings, FORMAT, SPREADSHEET_BODY, HEADER,
    SPREADSHEET_ROWS, SPREADSHEET_COLS
)


async def spreadsheets_create(wrapper_services: Aiogoogle) -> tuple[str, str]:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = deepcopy(SPREADSHEET_BODY)
    spreadsheet_body['properties']['title'] = f'Отчёт от {now_date_time}'
    spreadsheet_id = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body))

    return (spreadsheet_id['spreadsheetId'],
            spreadsheet_id['spreadsheetUrl'])


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
):
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields='id'
        ))


async def spreadsheets_update_value(
        spreadsheet_id: str,
        projects: List[CharityProject],
        wrapper_services: Aiogoogle
):
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = deepcopy(HEADER)
    table_values[0][1] = now_date_time
    data = [
        [str(project.name),
         str(project.close_date - project.create_date),
         str(project.description)]
        for project in projects
    ]
    table_values.extend(data)
    rows = len(table_values)
    cols = max(map(len, table_values))
    if rows > SPREADSHEET_ROWS or cols > SPREADSHEET_COLS:
        raise ValueError(
            f'Нет места. Необходимо: {rows} строк, {cols} колонок. '
            f'Имеется: {SPREADSHEET_ROWS} строк, {SPREADSHEET_COLS} колонок.'
        )
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'R1C1:R{rows}C{cols}',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
