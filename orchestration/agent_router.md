# Agent Router

## Purpose
Determine which execution tool/agent to call based on the current directive and context.

## Routing Rules

### Scraping Stage (scrape_website.md)
**Condition**: Need to fetch website content
- **Static sites** → `execution/scraping/scrape_single_site.py`
- **JavaScript-heavy sites** → `execution/utils/fetch_page_playwright.py`
- **Multiple URLs** → `execution/scraping/scrape_multiple_sites.py`
- **Batch processing** → `execution/scraping/scrape_multiple_sites.py` with concurrency

### Extraction Stage (extract_contacts.md)
**Condition**: Have scraped HTML, need to extract contacts
- **Email extraction** → `execution/scraping/extract_emails.py`
- **Link extraction** → `execution/scraping/extract_links.py`
- **Combined extraction** → Call both in sequence

### Validation Stage (validate_lead.md)
**Condition**: Have extracted contacts, need validation
- **Email format check** → `execution/validation/validate_email_format.py`
- **MX record check** → `execution/validation/check_mx_records.py`
- **Deduplication** → `execution/validation/dedupe_and_clean.py`
- **Full validation** → Call all three in sequence

### Enrichment Stage (enrich_lead.md)
**Condition**: Have validated leads, need enrichment
- **Tech stack detection** → `execution/enrichment/tech_stack_detector.py`
- **LinkedIn data** → `execution/enrichment/linkedin_metadata.py`
- **Website context** → `execution/enrichment/website_context_snippet.py`
- **Full enrichment** → Call all in parallel, merge results

### Email Generation Stage (generate_email.md)
**Condition**: Have enriched leads, need email drafts
- **Template selection** → `execution/email_generation/choose_template.py`
- **Email generation** → `execution/email_generation/generate_draft_email.py`
- **Sequence**: Choose template first, then generate

### Storage Stage (store_to_sheets.md or migrate_to_supabase.md)
**Condition**: Have processed data, need to store
- **Google Sheets write** → `execution/storage/google_sheets_write.py`
- **Google Sheets read** → `execution/storage/google_sheets_read.py`
- **Supabase write** → `execution/storage/supabase_write.py`
- **Supabase read** → `execution/storage/supabase_read.py`
- **Migration** → `execution/storage/migrate_sheet_to_supabase.py`

### Learning Stage (learner_self_anneal.md)
**Condition**: Have feedback or corrections, need to learn
- **Collect feedback** → `execution/learner/collect_feedback.py`
- **Analyze patterns** → `execution/learner/analyze_corrections.py`
- **Update prompts** → `execution/learner/update_prompts.py`
- **Sequence**: Collect → Analyze → Update

## Utility Tools (Always Available)

- **HTML to text** → `execution/utils/html_to_text.py`
- **URL normalization** → `execution/utils/url_normalizer.py`
- **Logging** → `execution/utils/logger.py`
- **Config loading** → `execution/utils/config_loader.py`

## Decision Logic

```python
def route_agent(directive, context):
    if directive == "scrape_website":
        if context.get("requires_js"):
            return "fetch_page_playwright"
        elif len(context.get("urls", [])) > 1:
            return "scrape_multiple_sites"
        else:
            return "scrape_single_site"
    
    elif directive == "extract_contacts":
        return ["extract_emails", "extract_links"]
    
    elif directive == "validate_lead":
        return ["validate_email_format", "check_mx_records", "dedupe_and_clean"]
    
    elif directive == "enrich_lead":
        return ["tech_stack_detector", "linkedin_metadata", "website_context_snippet"]
    
    elif directive == "generate_email":
        return ["choose_template", "generate_draft_email"]
    
    elif directive == "store_to_sheets":
        return "google_sheets_write"
    
    elif directive == "migrate_to_supabase":
        return "migrate_sheet_to_supabase"
    
    elif directive == "learner_self_anneal":
        return ["collect_feedback", "analyze_corrections", "update_prompts"]
```

## Error Routing

If a tool fails:
1. Check directive error handling section
2. Apply retry logic if specified
3. Route to fallback tool if available
4. Log error and continue or halt based on severity

## Parallel vs Sequential

- **Parallel**: Enrichment tools (independent data sources)
- **Sequential**: Validation tools (each depends on previous)
- **Conditional**: Scraping tools (based on site type)
