import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

def upload_excel_to_google_sheet(excel_path, sheet_title, creds_path, spreadsheet_id=None):
    # Load Excel file
    df = pd.read_excel(excel_path)
    # Authenticate
    creds = service_account.Credentials.from_service_account_file(
        creds_path,
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    # Use provided spreadsheet_id, do not create new
    if not spreadsheet_id:
        raise ValueError("spreadsheet_id must be provided for upload.")
    # Prepare data
    values = [df.columns.tolist()] + df.values.tolist()
    body = {'values': values}
    # Check if sheet/tab exists, create if not
    sheets_metadata = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    sheet_titles = [s['properties']['title'] for s in sheets_metadata['sheets']]
    if sheet_title not in sheet_titles:
        add_sheet_request = {
            'requests': [{
                'addSheet': {
                    'properties': {'title': sheet_title}
                }
            }]
        }
        service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=add_sheet_request
        ).execute()
    # Write data to the correct tab
    sheet.values().update(
        spreadsheetId=spreadsheet_id,
        range=f'{sheet_title}!A1',
        valueInputOption='RAW',
        body=body
    ).execute()
    print(f"Uploaded {excel_path} to tab '{sheet_title}' in Google Sheet: https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit")
    return spreadsheet_id

if __name__ == "__main__":
    creds_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'credentials.json'))
    linkedin_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '1st_lead', 'linkedin_leads.xlsx'))
    fiverr_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '1st_lead', 'fiverr_leads.xlsx'))
    upwork_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '1st_lead', 'upwork_leads.xlsx'))
    spreadsheet_id = "1XN4wIbZijwpAdI2I3SaBLkuCWWdbQFX9yqwocWfslHQ"
    upload_excel_to_google_sheet(linkedin_path, 'LinkedIn Leads', creds_path, spreadsheet_id)
    upload_excel_to_google_sheet(upwork_path, 'Upwork Leads', creds_path, spreadsheet_id)
    upload_excel_to_google_sheet(fiverr_path, 'Fiverr Leads', creds_path, spreadsheet_id)
