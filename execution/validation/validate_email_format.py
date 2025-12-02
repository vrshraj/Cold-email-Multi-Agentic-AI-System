"""
Validate email format using RFC 5322 standards.
"""
import re
import sys
import json
from typing import List

def validate_email_format(email: str) -> dict:
    """
    Validate email format.
    
    Args:
        email: Email address to validate
    
    Returns:
        Dict with validation result
    """
    # RFC 5322 simplified regex
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    is_valid = bool(re.match(pattern, email))
    
    return {
        'email': email,
        'valid': is_valid,
        'reason': 'Valid format' if is_valid else 'Invalid format'
    }

def validate_emails_batch(emails: List[str]) -> dict:
    """
    Validate multiple emails.
    
    Args:
        emails: List of email addresses
    
    Returns:
        Dict with validation results
    """
    results = {
        'total': len(emails),
        'valid': 0,
        'invalid': 0,
        'details': []
    }
    
    for email in emails:
        result = validate_email_format(email)
        results['details'].append(result)
        
        if result['valid']:
            results['valid'] += 1
        else:
            results['invalid'] += 1
    
    return results

if __name__ == "__main__":
    print("validate_email_format.py - Email format validation tool")
