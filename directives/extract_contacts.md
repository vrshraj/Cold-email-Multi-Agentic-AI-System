# Extract Contacts Directive

## Objective
Identify and extract contact information (emails, phone numbers, social links) from scraped content.

## Input
- Scraped HTML/text content
- Extraction patterns and rules

## Process
1. Parse HTML/text for contact patterns
2. Extract email addresses using regex
3. Extract phone numbers with format validation
4. Identify social media links (LinkedIn, Twitter, etc.)
5. Extract contact form URLs
6. Deduplicate extracted contacts

## Output
- List of email addresses
- Phone numbers with country codes
- Social media profile URLs
- Contact metadata (source page, confidence score)

## Error Handling
- Malformed emails → Validate and flag
- Duplicate contacts → Merge and track sources
- No contacts found → Log for manual review
- Obfuscated emails → Apply deobfuscation techniques

## Success Criteria
- All valid contacts extracted
- No false positives (spam traps, generic emails)
- Proper attribution to source pages
