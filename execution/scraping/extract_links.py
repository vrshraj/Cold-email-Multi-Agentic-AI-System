"""
Extract links from HTML content.
"""
import re
import sys
import json
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def extract_links(html_content: str, base_url: str = None) -> dict:
    """
    Extract all links from HTML content.
    
    Args:
        html_content: HTML string to parse
        base_url: Base URL for resolving relative links
    
    Returns:
        Dict with categorized links
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    links = {
        'internal': [],
        'external': [],
        'social': [],
        'contact_forms': []
    }
    
    # Extract all <a> tags
    for link in soup.find_all('a', href=True):
        href = link['href']
        
        # Resolve relative URLs
        if base_url:
            href = urljoin(base_url, href)
        
        # Categorize link
        if 'contact' in href.lower() or 'get-in-touch' in href.lower():
            links['contact_forms'].append(href)
        elif any(social in href.lower() for social in ['linkedin', 'twitter', 'facebook', 'instagram']):
            links['social'].append(href)
        elif base_url and urlparse(href).netloc == urlparse(base_url).netloc:
            links['internal'].append(href)
        else:
            links['external'].append(href)
    
    # Deduplicate
    for category in links:
        links[category] = list(set(links[category]))
    
    return links

if __name__ == "__main__":
    # Placeholder implementation
    print("extract_links.py - Link extraction tool")
