# Errors and Edge Cases Directive

## Objective
Document common errors, edge cases, and their handling strategies across the pipeline.

## Common Errors

### Scraping Errors
- **403 Forbidden**: Rotate user agents, use proxies
- **429 Rate Limited**: Implement exponential backoff
- **Timeout**: Increase timeout, retry with smaller chunks
- **JavaScript Required**: Use Playwright instead of requests
- **CAPTCHA**: Log for manual review, skip temporarily

### Extraction Errors
- **No Contacts Found**: Expand search patterns, check alternate pages
- **Obfuscated Emails**: Apply deobfuscation rules
- **Invalid Format**: Log and skip, improve regex patterns
- **Too Many Contacts**: Apply filtering rules, prioritize by relevance

### Validation Errors
- **No MX Records**: Flag as invalid, retry after 24h
- **Temporary Failure**: Queue for retry
- **Spam Trap Detected**: Blacklist and remove
- **Duplicate Lead**: Merge data, update existing record

### Enrichment Errors
- **API Quota Exceeded**: Queue for next cycle
- **No Data Available**: Mark as incomplete, continue
- **Stale Data**: Refresh if older than threshold
- **Conflicting Sources**: Use priority ranking

### Email Generation Errors
- **Missing Required Data**: Use fallback template
- **High Spam Score**: Regenerate with adjustments
- **Template Not Found**: Use default template
- **Personalization Failure**: Fall back to generic version

### Storage Errors
- **Authentication Failure**: Refresh tokens, retry
- **Schema Mismatch**: Log and notify, skip record
- **Duplicate Key**: Update existing or skip
- **Connection Lost**: Retry with exponential backoff

## Edge Cases

### Data Quality
- Empty or null values in critical fields
- Unicode and special characters in names
- Multiple email formats on same page
- Inconsistent company name variations

### Business Logic
- Lead already contacted recently
- Company on do-not-contact list
- Multiple contacts from same company
- Competitor domains detected

### System Resources
- Disk space exhaustion
- Memory limits reached
- API rate limits across multiple services
- Concurrent execution conflicts

## Handling Strategy
1. **Detect**: Identify error/edge case early
2. **Log**: Record details for analysis
3. **Recover**: Apply appropriate recovery strategy
4. **Learn**: Feed back to learner system
5. **Alert**: Notify if manual intervention needed

## Success Criteria
- All errors handled gracefully
- No unhandled exceptions
- Edge cases documented and tested
- Recovery strategies proven effective
- Minimal manual intervention required
