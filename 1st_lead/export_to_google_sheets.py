#!/usr/bin/env python3
"""
Export leads to Google Sheets
"""

import json
from pathlib import Path
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SHEET_ID = "1XN4wIbZijwpAdI2I3SaBLkuCWWdbQFX9yqwocWfslHQ"
CREDENTIALS_PATH = "credentials.json"
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_sheets_service():
    """Authenticate and return Google Sheets service."""
    credentials = Credentials.from_service_account_file(
        CREDENTIALS_PATH, 
        scopes=SCOPES
    )
    return build('sheets', 'v4', credentials=credentials)

def load_leads():
    """Load leads from the search agent output."""
    json_path = Path(".tmp/discovery/discovered_leads_20251202_113000.json")
    if not json_path.exists():
        # If file doesn't exist, generate it
        from execution.scraping.search_agent import SearchAgent
        agent = SearchAgent()
        leads = agent.find_leads("Businesses needing agentic AI workflow automation solutions", 51)
        output_path = agent.save_results(leads)
        json_path = Path(output_path)
    
    with open(json_path) as f:
        return json.load(f)

def prepare_data(leads):
    """Prepare leads data for Google Sheets."""
    rows = []
    
    # Header row
    headers = [
        'Lead #',
        'First Name',
        'Last Name',
        'Company Name',
        'Title',
        'Industry',
        'LinkedIn URL',
        'Company Website',
        'Email Domain',
        'Likely Email',
        'Status',
        'Date Contacted',
        'Notes'
    ]
    rows.append(headers)
    
    # Data rows
    for idx, lead in enumerate(leads, 1):
        name_parts = lead['person_name'].split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''
        
        website = lead['website_url']
        email_domain = website.replace('https://', '').replace('http://', '').replace('www.', '')
        likely_email = f"{first_name.lower()}@{email_domain}"
        
        row = [
            str(idx),
            first_name,
            last_name,
            lead['company_name'],
            lead['title'],
            lead['industry'],
            lead['linkedin_url'],
            lead['website_url'],
            email_domain,
            likely_email,
            '',
            '',
            ''
        ]
        rows.append(row)
    
    return rows

def export_to_sheets(service, sheet_id, data):
    """Export data to Google Sheets."""
    body = {
        'values': data
    }
    
    result = service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range='Sheet1!A1',
        valueInputOption='RAW',
        body=body
    ).execute()
    
    return result

def format_sheet(service, sheet_id):
    """Format the Google Sheet with styling."""
    requests = [
        {
            "updateSheetProperties": {
                "fields": "gridProperties.frozenRowCount",
                "properties": {
                    "sheetId": 0,
                    "gridProperties": {
                        "frozenRowCount": 1
                    }
                }
            }
        },
        {
            "repeatCell": {
                "range": {
                    "sheetId": 0,
                    "startRowIndex": 0,
                    "endRowIndex": 1
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": {
                            "red": 0.2,
                            "green": 0.2,
                            "blue": 0.2
                        },
                        "textFormat": {
                            "foregroundColor": {
                                "red": 1,
                                "green": 1,
                                "blue": 1
                            },
                            "bold": True
                        },
                        "horizontalAlignment": "CENTER"
                    }
                },
                "fields": "userEnteredFormat"
            }
        },
        {
            "autoResizeDimensions": {
                "dimensions": {
                    "sheetId": 0,
                    "dimension": "COLUMNS"
                }
            }
        }
    ]
    
    body = {'requests': requests}
    service.spreadsheets().batchUpdate(
        spreadsheetId=sheet_id,
        body=body
    ).execute()

def main():
    print("Loading leads...")
    leads = load_leads()
    print(f"Loaded {len(leads)} leads")
    
    print("Preparing data...")
    data = prepare_data(leads)
    
    print("Authenticating with Google Sheets...")
    service = get_sheets_service()
    
    print("Exporting to Google Sheets...")
    result = export_to_sheets(service, SHEET_ID, data)
    print(f"Successfully updated {result['updatedCells']} cells")
    
    print("Formatting sheet...")
    format_sheet(service, SHEET_ID)
    
    print("\nSUCCESS! Your leads have been exported to Google Sheets:")
    print(f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit")

if __name__ == '__main__':
    main()
