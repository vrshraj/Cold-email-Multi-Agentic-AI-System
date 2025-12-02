"""
Extract email addresses from HTML content.
"""
import re
import sys
import json
from pathlib import Path
from typing import List, Set

def extract_emails(html_content: str, min_confidence: float = 0.7) -> List[dict]:
    """
    Extract email addresses from HTML content.
    
    Args:
        html_content: HTML string to parse
        min_confidence: Minimum confidence score (0-1)
    
    Returns:
        List of dicts with email and confidence score
    """
    # Email regex pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    
    # Find all potential emails
    potential_emails = re.findall(email_pattern, html_content)
    
    # Deduplicate
    unique_emails: Set[str] = set(potential_emails)
    
    # Filter and score emails
    results = []
    for email in unique_emails:
        confidence = calculate_confidence(email)
        
        if confidence >= min_confidence:
            results.append({
                'email': email.lower(),
                'confidence': confidence,
                'valid': True
            })
    
    return results

def calculate_confidence(email: str) -> float:
    """
    Calculate confidence score for an email address.
    
    Args:
        email: Email address to score
    
    Returns:
        Confidence score between 0 and 1
    """
    score = 0.5  # Base score
    
    # Penalize common false positives
    spam_indicators = ['example.com', 'test.com', 'noreply', 'no-reply', 'donotreply']
    if any(indicator in email.lower() for indicator in spam_indicators):
        score -= 0.3
    
    # Penalize image/asset emails
    if any(ext in email.lower() for ext in ['.png', '.jpg', '.gif', '.css', '.js']):
        score -= 0.5
    
    # Boost for common business domains
    business_domains = ['.com', '.io', '.co', '.net', '.org']
    if any(email.endswith(domain) for domain in business_domains):
        score += 0.2
    
    # Boost for professional patterns
    if re.match(r'^[a-z]+\.[a-z]+@', email):  # firstname.lastname@
        score += 0.2
    
    # Ensure score is between 0 and 1
    return max(0.0, min(1.0, score))

def process_html_file(filepath: str, min_confidence: float = 0.7) -> dict:
    """
    Process a single HTML file and extract emails.
    
    Args:
        filepath: Path to HTML file
        min_confidence: Minimum confidence threshold
    
    Returns:
        Dict with extraction results
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        emails = extract_emails(html_content, min_confidence)
        
        return {
            'success': True,
            'file': filepath,
            'emails_found': len(emails),
            'emails': emails
        }
    except Exception as e:
        return {
            'success': False,
            'file': filepath,
            'error': str(e)
        }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_emails.py <html_dir> [output_file] [min_confidence]")
        sys.exit(1)
    
    html_dir = Path(sys.argv[1])
    output_file = sys.argv[2] if len(sys.argv) > 2 else ".tmp/parsed_json/contacts.json"
    min_confidence = float(sys.argv[3]) if len(sys.argv) > 3 else 0.7
    
    # Process all HTML files
    results = []
    all_emails = []
    
    for html_file in html_dir.glob("*.html"):
        print(f"Processing: {html_file.name}")
        result = process_html_file(str(html_file), min_confidence)
        results.append(result)
        
        if result['success']:
            all_emails.extend(result['emails'])
    
    # Deduplicate across all files
    unique_emails = {email['email']: email for email in all_emails}
    
    output_data = {
        'total_files': len(results),
        'total_emails': len(unique_emails),
        'emails': list(unique_emails.values()),
        'file_results': results
    }
    
    # Save results
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"\n✓ Extracted {len(unique_emails)} unique emails")
    print(f"✓ Saved to: {output_file}")
