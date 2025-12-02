# Store to Sheets Directive

## Objective
Save processed lead data and generated emails to Google Sheets for review and tracking.

## Input
- Processed lead data
- Generated email drafts
- Sheet configuration (ID, range, format)

## Process
1. Authenticate with Google Sheets API
2. Format data according to sheet schema
3. Check for existing records (avoid duplicates)
4. Append new rows or update existing
5. Apply conditional formatting rules
6. Update summary/statistics sheet
7. Set data validation rules
8. Create backup snapshot

## Output
- Updated Google Sheet with new leads
- Row IDs for tracking
- Update timestamp
- Success/failure count

## Error Handling
- Authentication failures → Retry with token refresh
- Rate limits → Batch and queue writes
- Duplicate entries → Skip or merge based on policy
- Schema mismatches → Log and notify
- Network errors → Retry with exponential backoff

## Success Criteria
- All valid leads written to sheet
- No data loss or corruption
- Proper formatting maintained
- Audit trail preserved
