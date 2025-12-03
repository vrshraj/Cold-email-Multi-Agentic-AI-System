# Scrape Website Directive

## Objective
Extract structured data from target websites for lead generation purposes.

## Input
- Target URL(s)
- Scraping configuration (selectors, depth, rate limits)

## Process
1. Validate URL format and accessibility
2. Fetch page content using appropriate method (static/dynamic)
3. Parse HTML and extract relevant data
4. Handle pagination and multi-page scraping
5. Respect robots.txt and rate limits

## Output
- Scraped HTML content
- Extracted structured data (JSON)
- Metadata (timestamp, source URL, status)

## Error Handling
- Invalid URLs → Log and skip
- Rate limiting → Implement exponential backoff
- Blocked requests → Rotate user agents/proxies
- Parsing errors → Save raw HTML for manual review

## Success Criteria
- All accessible pages scraped successfully
- Data extracted matches expected schema
- No violations of website terms of service
- **CRITICAL: Only real, verified data extracted (no dummy/fake leads)**
- Data sources validated: real companies, real emails, real profiles
- Lead authenticity verified before export

## Self-Anneal Feedback (Updated 2025-12-03)
Previous execution generated 450 dummy leads instead of real leads.
**Lesson Learned**: Lead generation must use authenticated APIs or verified data sources only.
**Correction Action**: Use LinkedIn Sales Navigator API, Upwork API, Fiverr API, or third-party services (Hunter.io, Apollo.io, RocketReach) for real lead extraction.

