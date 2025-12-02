"""
Convert HTML to plain text.
"""
from bs4 import BeautifulSoup
import sys

def html_to_text(html_content: str) -> str:
    """
    Convert HTML to plain text.
    
    Args:
        html_content: HTML string
    
    Returns:
        Plain text content
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()
    
    # Get text
    text = soup.get_text()
    
    # Clean up whitespace
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = ' '.join(chunk for chunk in chunks if chunk)
    
    return text

if __name__ == "__main__":
    print("html_to_text.py - HTML to text converter")
