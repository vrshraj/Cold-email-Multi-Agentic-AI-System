# Enrich Lead Directive

## Objective
Enhance lead data with additional context and metadata for personalized outreach.

## Input
- Validated lead data
- Enrichment sources and APIs
- Enrichment budget/limits

## Process
1. Detect technology stack from website
2. Extract company metadata (size, industry, location)
3. Gather LinkedIn profile information
4. Identify decision makers and roles
5. Extract recent news/updates about company
6. Analyze website content for pain points
7. Calculate engagement potential score

## Output
- Enriched lead profile
- Technology stack list
- Company metadata
- Key decision makers
- Personalization data points
- Engagement score

## Error Handling
- API rate limits → Queue and retry
- Missing data → Mark as incomplete
- Conflicting data → Use most recent/reliable source
- Enrichment failures → Continue with partial data

## Success Criteria
- At least 70% of leads enriched successfully
- Key data points populated (tech stack, industry)
- Enrichment data is current (< 30 days old)
- Personalization opportunities identified
