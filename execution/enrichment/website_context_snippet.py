"""
Extract context snippet from website for personalization.
"""
import sys
import json
from bs4 import BeautifulSoup

def extract_context_snippet(html_content: str, max_length: int = 500) -> dict:
    """
    Extract relevant context from website.
    
    Args:
        html_content: HTML content
        max_length: Maximum snippet length
    
    Returns:
        Dict with context snippets
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract key sections
    context = {
        'title': '',
        'description': '',
        'about': '',
        'services': []
    }
    
    # Get title
    title_tag = soup.find('title')
    if title_tag:
        context['title'] = title_tag.get_text().strip()
    
    # Get meta description
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if meta_desc:
        context['description'] = meta_desc.get('content', '').strip()
    
    return context

if __name__ == "__main__":
    print("website_context_snippet.py - Context extraction tool")
