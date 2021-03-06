import gspread
import numpy as np
import pandas as pd
import os
import logging

# there is an alternative gspread_pandas but there it wraps arround gspread so credentials go trough it...
# for security reasons I chose this simpler wrapper
from gspread_dataframe import set_with_dataframe, get_as_dataframe

from backend.repository import Repository

log = logging.getLogger(__name__)


class GSheetRepository(Repository):

    def __init__(self, base_url: str):
        self.base_url = base_url
        self._gspread_client = None
        self._spreadsheet = None

    def _get_gspread_client(self):

        if self._gspread_client is None:
            try:
                self._gspread_client = gspread.service_account(
                    filename=os.getenv(
                        "GOOGLE_APPLICATION_CREDENTIALS", "~/.config/gspread/service_account.json"
                    )
                )
            except FileNotFoundError as e:
                log.error(f"Unable to create gspread client #{e}")

        return self._gspread_client

    def _get_spreadsheet(self):
        if self._spreadsheet is None:
            self._spreadsheet = self._get_gspread_client().open_by_url(self.base_url)
        return self._spreadsheet

    def _get_worksheet(self, worksheet_name: str) -> gspread.Worksheet:
        sheet = self._get_spreadsheet()
        worksheet = sheet.worksheet(worksheet_name)
        return worksheet

    def store_dataframe(self, df: pd.DataFrame, storage_location: str, allow_create: bool,
                        store_index: bool = False) -> None:
        if not self.exists(storage_location):
            if allow_create:
                log.info(f'Created storage location {storage_location}')
                self.create_storage_location(storage_location)
            else:
                raise ValueError('Storage location does not exists, create it or call this with allow_create=True')

        worksheet = self._get_worksheet(storage_location)

        df = df.replace([np.inf, -np.inf], np.nan)

        set_with_dataframe(worksheet, df, include_index=store_index, resize=True)

    def get_dataframe(self, storage_location: str) -> pd.DataFrame:
        worksheet = self._get_worksheet(storage_location)

        headers = worksheet.row_values(1)  # 1 indexed

        if 'date' in headers:
            return get_as_dataframe(worksheet, parse_dates=['date'], header=0)

        return get_as_dataframe(worksheet, header=0)

    def exists(self, storage_location: str) -> bool:
        spreadsheet = self._get_spreadsheet()
        sheet_names = [sheet.title for sheet in spreadsheet]
        return storage_location in sheet_names

    def create_storage_location(self, storage_location: str) -> None:
        if self.exists(storage_location):
            log.warning(f'Storage location {storage_location} already exists')
            return

        _ = self._get_spreadsheet().add_worksheet(title=storage_location, rows=2, cols=2)

    def delete_storage_location(self, storage_location: str) -> None:
        if not self.exists(storage_location):
            log.warning(f'storage location {storage_location} requested for deletion did not exist:')
            return

        worksheet = self._get_worksheet(storage_location)
        self._get_spreadsheet().del_worksheet(worksheet)

    def create_repository(self, repository_name: str, admin_email: str) -> str:
        log.info(f'Creating a new Google Sheet "{repository_name}" as a repository')
        client = self._get_gspread_client()

        spreadsheet = client.create(repository_name)
        log.info(f'Created sheet with id: {spreadsheet.id}')

        self.base_url = spreadsheet.url
        log.info(f'URL: {spreadsheet.url}')

        spreadsheet.share(admin_email, perm_type='user', role='owner')
        log.info(f'Assigned {admin_email} as owner')

        return spreadsheet.id
