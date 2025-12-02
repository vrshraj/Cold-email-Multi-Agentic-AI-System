# Orchestrator Pipeline Directive

## Objective
Coordinate the execution of all pipeline stages in the correct order with proper error handling.

## Input
- Pipeline configuration (workflow plan)
- Initial parameters (URLs, targets, limits)
- Execution context (scheduled/manual, priority)

## Process
1. Load workflow plan and validate
2. Initialize pipeline state
3. Execute stages in sequence:
   - Scrape websites
   - Extract contacts
   - Validate leads
   - Enrich lead data
   - Generate emails
   - Store to Sheets/Supabase
4. Monitor execution progress
5. Handle stage failures and retries
6. Collect metrics and logs
7. Trigger learner for feedback analysis
8. Generate execution report

## Output
- Pipeline execution status
- Stage-by-stage results
- Error summary
- Performance metrics
- Processed lead count
- Execution timeline

## Error Handling
- Stage failure → Retry with backoff or skip
- Timeout → Cancel and log partial results
- Resource exhaustion → Pause and resume
- Critical errors → Halt pipeline and alert
- Partial failures → Continue with successful records

## Success Criteria
- All stages complete successfully or fail gracefully
- No data loss between stages
- Execution time within acceptable limits
- All errors logged and categorized
- State is recoverable for resume/retry
