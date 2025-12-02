"""
Deduplicate and clean lead data.
"""
import sys
import json
from typing import List

def dedupe_and_clean(leads: List[dict]) -> dict:
    """
    Remove duplicates and clean lead data.
    
    Args:
        leads: List of lead dictionaries
    
    Returns:
        Dict with cleaned leads
    """
    # Use email as unique key
    unique_leads = {}
    
    for lead in leads:
        email = lead.get('email', '').lower().strip()
        
        if email and email not in unique_leads:
            # Clean the lead data
            cleaned_lead = {
                'email': email,
                'company': lead.get('company', '').strip(),
                'website': lead.get('website', '').strip(),
                'source': lead.get('source', 'unknown')
            }
            unique_leads[email] = cleaned_lead
    
    return {
        'original_count': len(leads),
        'unique_count': len(unique_leads),
        'duplicates_removed': len(leads) - len(unique_leads),
        'leads': list(unique_leads.values())
    }

if __name__ == "__main__":
    print("dedupe_and_clean.py - Deduplication and cleaning tool")
