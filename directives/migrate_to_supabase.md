# Migrate to Supabase Directive

## Objective
Transfer lead data from Google Sheets to Supabase database for better scalability and querying.

## Input
- Google Sheet ID and range
- Supabase connection details
- Migration mapping rules

## Process
1. Read data from Google Sheets
2. Transform data to match Supabase schema
3. Validate data integrity
4. Create/update Supabase tables
5. Batch insert records
6. Handle conflicts (upsert strategy)
7. Verify migration completeness
8. Update migration log

## Output
- Migration summary (records processed, inserted, updated)
- Error log for failed records
- Data validation report
- Rollback snapshot (if needed)

## Error Handling
- Connection failures → Retry with backoff
- Schema mismatches → Log and skip record
- Constraint violations → Apply conflict resolution
- Partial failures → Continue and log errors
- Transaction failures → Rollback and retry

## Success Criteria
- 100% of valid records migrated
- Data integrity maintained
- No duplicate records created
- Foreign key relationships preserved
- Migration is idempotent (can be re-run safely)
