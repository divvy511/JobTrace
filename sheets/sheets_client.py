import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from utils.logger import setup_logger

logger = setup_logger("sheets_client")

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


class SheetsClient:
    def __init__(self):
        sheet_id = os.getenv("GOOGLE_SHEETS_ID")
        cred_file = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE")

        if not sheet_id or not cred_file:
            raise ValueError("Google Sheets env variables not set")

        self.sheet_id = sheet_id

        creds = Credentials.from_service_account_file(cred_file, scopes=SCOPES)

        self.service = build("sheets", "v4", credentials=creds)
        self.ensure_headers()

        logger.info("Google Sheets client initialized")

    def append_job_actions(self, actions: list):
        rows = []

        for a in actions:
            rows.append(
                [
                    a.timestamp.isoformat(),
                    a.company_name,
                    a.role,
                    a.recruiter_name,
                    a.action_type,
                    a.channel,
                    a.confidence or "",
                    a.notes,
                ]
            )

        if not rows:
            logger.info("No valid job actions to write")
            return

        self.service.spreadsheets().values().append(
            spreadsheetId=self.sheet_id,
            range="A:H",
            valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS",
            body={"values": rows},
        ).execute()

        logger.info(f"Wrote {len(rows)} job actions to Google Sheets")

    def ensure_headers(self):
        headers = [
            [
                "Timestamp",
                "Company Name",
                "Role",
                "Recruiter Name",
                "Action Type",
                "Channel",
                "Source Confidence",
                "Notes",
            ]
        ]

        result = (
            self.service.spreadsheets()
            .values()
            .get(spreadsheetId=self.sheet_id, range="A1:I1")
            .execute()
        )

        if "values" not in result:
            logger.info("Headers not found. Creating header row.")
            self.service.spreadsheets().values().update(
                spreadsheetId=self.sheet_id,
                range="A1:I1",
                valueInputOption="RAW",
                body={"values": headers},
            ).execute()
        else:
            logger.info("Headers already exist.")
