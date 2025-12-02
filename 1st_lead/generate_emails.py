#!/usr/bin/env python3
"""
Generate personalized cold emails for all leads
"""

import json
from pathlib import Path
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SHEET_ID = "1XN4wIbZijwpAdI2I3SaBLkuCWWdbQFX9yqwocWfslHQ"
CREDENTIALS_PATH = "credentials.json"
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

EMAIL_TEMPLATES = {
    "E-commerce": {
        "subject": "{first_name}, 80% faster order processing?",
        "body": """Hi {first_name},

I noticed {company_name} is scaling fast in e-commerce.

Most teams struggle with manual order processing - it's costing them 30+ hours per week and slowing down customer fulfillment.

We help e-commerce companies like {company_name} automate this with AI agents that handle order-to-fulfillment in minutes, not hours.

Would it make sense to chat for 15 minutes next week?

Best regards,
[Your Name]"""
    },
    
    "Digital Marketing": {
        "subject": "{first_name}, qualified leads 24/7?",
        "body": """Hi {first_name},

{company_name} is doing great work in {industry}.

The challenge most marketing teams face: only 10-15% of leads get qualified because manual screening takes too long.

We built AI agents that qualify leads 24/7, so your team never misses a potential customer. Most clients see 5x more conversions.

Quick question - how much time does your team spend on lead qualification weekly?

Best regards,
[Your Name]"""
    },
    
    "Customer Support": {
        "subject": "{first_name}, support response time?",
        "body": """Hi {first_name},

{company_name} is growing fast. I know support tickets are piling up.

Most teams waste 40+ hours/week on repetitive support tasks that could be automated. This kills customer satisfaction and costs a fortune.

We use AI agents to handle 80% of support requests automatically, freeing your team for complex issues.

Worth a 15-min chat?

Best regards,
[Your Name]"""
    },
    
    "HR & Recruitment": {
        "subject": "{first_name}, cutting hiring time in half?",
        "body": """Hi {first_name},

{company_name} is clearly growing - that means hiring pressure.

Hiring teams typically spend 40+ hours/month just screening resumes and scheduling interviews. It's a bottleneck that slows everything down.

We've built AI agents that screen resumes, schedule interviews, and send candidate updates - cutting hiring time from months to weeks.

Your industry is seeing 60% faster hiring with this approach.

Quick question - what's your biggest bottleneck in recruiting right now?

Best regards,
[Your Name]"""
    },
    
    "Finance & Accounting": {
        "subject": "{first_name}, invoice processing at scale?",
        "body": """Hi {first_name},

{company_name} handles invoices daily. Most finance teams spend 30+ minutes per invoice manually processing them.

With AI agents, that time drops to under 5 minutes per invoice. Plus no data entry errors.

This usually saves companies $10K-$50K/month in labor costs alone.

Would it be worth 15 minutes to explore this?

Best regards,
[Your Name]"""
    },
    
    "Real Estate": {
        "subject": "{first_name}, automating lead follow-up?",
        "body": """Hi {first_name},

{company_name} generates good leads - the challenge is following up with all of them.

Most real estate teams lose 30-40% of potential deals because they can't keep up with follow-ups and scheduling.

AI agents handle all the follow-ups, qualify leads, and schedule tours automatically. Our clients see 70% more conversions.

What percentage of your leads do you currently follow up with?

Best regards,
[Your Name]"""
    },
    
    "Healthcare": {
        "subject": "{first_name}, appointment no-shows?",
        "body": """Hi {first_name},

{company_name} knows how costly appointment no-shows are.

Most healthcare practices lose 20-25% of revenue to no-shows and missed follow-ups.

AI agents handle appointment reminders, patient communication, and follow-ups automatically - reducing no-shows by 25%.

Worth exploring?

Best regards,
[Your Name]"""
    },
    
    "Education": {
        "subject": "{first_name}, student engagement at scale?",
        "body": """Hi {first_name},

{company_name} is growing in the education space. Managing student communication at scale is tough.

Most programs spend 20+ hours/week on administrative communications that could be automated.

AI agents handle course updates, student questions, and engagement automatically - improving retention by 15-20%.

Quick 15-min chat?

Best regards,
[Your Name]"""
    },
    
    "Default": {
        "subject": "{first_name}, automating your operations?",
        "body": """Hi {first_name},

I came across {company_name} and was impressed by what you're building in {industry}.

Most companies in your space struggle with manual processes that consume 30+ hours per week and limit scaling.

We help teams like {company_name} automate these workflows with AI agents, cutting operational costs by 40-60%.

Would you be open to a quick 15-minute conversation?

Best regards,
[Your Name]"""
    }
}

def get_sheets_service():
    """Authenticate and return Google Sheets service."""
    credentials = Credentials.from_service_account_file(
        CREDENTIALS_PATH, 
        scopes=SCOPES
    )
    return build('sheets', 'v4', credentials=credentials)

def load_leads():
    """Load leads from JSON file."""
    json_path = Path(".tmp/discovery/discovered_leads_20251202_113000.json")
    with open(json_path) as f:
        return json.load(f)

def get_email_template(industry):
    """Get the best email template for the industry."""
    for key in EMAIL_TEMPLATES.keys():
        if key.lower() in industry.lower() or industry.lower() in key.lower():
            return EMAIL_TEMPLATES[key]
    return EMAIL_TEMPLATES["Default"]

def generate_email(lead):
    """Generate a personalized email for a lead."""
    name_parts = lead['person_name'].split(' ', 1)
    first_name = name_parts[0]
    
    template = get_email_template(lead['industry'])
    
    subject = template["subject"].format(
        first_name=first_name,
        company_name=lead['company_name'],
        industry=lead['industry']
    )
    
    body = template["body"].format(
        first_name=first_name,
        company_name=lead['company_name'],
        industry=lead['industry']
    )
    
    return {
        "subject": subject,
        "body": body
    }

def export_emails_to_sheets(service, sheet_id, leads):
    """Add emails to the Google Sheet in a new sheet."""
    requests = [{
        "addSheet": {
            "properties": {
                "title": "Email Drafts",
                "gridProperties": {
                    "rowCount": len(leads) + 1,
                    "columnCount": 4
                }
            }
        }
    }]
    
    response = service.spreadsheets().batchUpdate(
        spreadsheetId=sheet_id,
        body={"requests": requests}
    ).execute()
    
    sheet_id_new = response['replies'][0]['addSheet']['properties']['sheetId']
    
    rows = [['Lead #', 'Company', 'Email Subject', 'Email Body']]
    
    for idx, lead in enumerate(leads, 1):
        email = generate_email(lead)
        rows.append([
            str(idx),
            lead['company_name'],
            email['subject'],
            email['body']
        ])
    
    body = {'values': rows}
    service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range='Email Drafts!A1',
        valueInputOption='RAW',
        body=body
    ).execute()
    
    format_requests = [
        {
            "repeatCell": {
                "range": {
                    "sheetId": sheet_id_new,
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
            "updateSheetProperties": {
                "fields": "gridProperties.frozenRowCount",
                "properties": {
                    "sheetId": sheet_id_new,
                    "gridProperties": {
                        "frozenRowCount": 1
                    }
                }
            }
        },
        {
            "autoResizeDimensions": {
                "dimensions": {
                    "sheetId": sheet_id_new,
                    "dimension": "COLUMNS"
                }
            }
        }
    ]
    
    service.spreadsheets().batchUpdate(
        spreadsheetId=sheet_id,
        body={"requests": format_requests}
    ).execute()
    
    return len(leads)

def main():
    print("Loading leads...")
    leads = load_leads()
    print(f"Loaded {len(leads)} leads")
    
    print("Generating personalized emails...")
    for idx, lead in enumerate(leads, 1):
        email = generate_email(lead)
        print(f"  {idx}. {lead['company_name']}: {email['subject']}")
    
    print("\nAuthenticating with Google Sheets...")
    service = get_sheets_service()
    
    print("Exporting emails to Google Sheets...")
    count = export_emails_to_sheets(service, SHEET_ID, leads)
    
    print(f"\nSUCCESS! {count} personalized emails have been generated!")

if __name__ == '__main__':
    main()
