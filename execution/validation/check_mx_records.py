"""
Check MX records for email domains.
"""
import dns.resolver
import sys
import json

def check_mx_records(domain: str) -> dict:
    """
    Check if domain has valid MX records.
    
    Args:
        domain: Email domain to check
    
    Returns:
        Dict with MX record status
    """
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        return {
            'domain': domain,
            'has_mx': True,
            'mx_count': len(mx_records),
            'mx_records': [str(mx.exchange) for mx in mx_records]
        }
    except Exception as e:
        return {
            'domain': domain,
            'has_mx': False,
            'error': str(e)
        }

if __name__ == "__main__":
    print("check_mx_records.py - MX record validation tool")
