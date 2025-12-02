"""
Normalize and clean URLs.
"""
from urllib.parse import urlparse, urlunparse
import sys

def normalize_url(url: str) -> str:
    """
    Normalize URL to standard format.
    
    Args:
        url: URL to normalize
    
    Returns:
        Normalized URL
    """
    # Parse URL
    parsed = urlparse(url)
    
    # Ensure scheme
    if not parsed.scheme:
        url = 'https://' + url
        parsed = urlparse(url)
    
    # Remove trailing slash
    path = parsed.path.rstrip('/')
    
    # Rebuild URL
    normalized = urlunparse((
        parsed.scheme,
        parsed.netloc.lower(),
        path,
        parsed.params,
        parsed.query,
        ''  # Remove fragment
    ))
    
    return normalized

if __name__ == "__main__":
    print("url_normalizer.py - URL normalization utility")
