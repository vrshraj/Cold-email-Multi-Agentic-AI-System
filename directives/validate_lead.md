# Validate Lead Directive

## Objective
Verify the quality and validity of extracted leads before enrichment.

## Input
- Lead data (email, company, website)
- Validation rules and criteria

## Process
1. Validate email format (RFC 5322)
2. Check MX records for email domain
3. Verify email deliverability (optional SMTP check)
4. Validate company website accessibility
5. Check against spam trap databases
6. Deduplicate against existing leads
7. Score lead quality (0-100)

## Output
- Validation status (valid/invalid/uncertain)
- Quality score
- Validation details (which checks passed/failed)
- Cleaned and normalized data

## Error Handling
- Invalid email format → Reject and log
- No MX records → Flag as suspicious
- Duplicate leads → Merge or skip based on policy
- Timeout on checks → Retry with backoff

## Success Criteria
- All leads validated against defined criteria
- Invalid leads filtered out
- Quality scores assigned accurately
- No false negatives (valid leads rejected)
