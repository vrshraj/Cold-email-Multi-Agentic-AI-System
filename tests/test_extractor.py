"""
Test suite for email extraction functionality.
"""
import pytest
import sys
from pathlib import Path

# Add execution directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'execution' / 'scraping'))

from extract_emails import extract_emails, calculate_confidence

def test_extract_emails_basic():
    """Test basic email extraction."""
    html = """
    <html>
        <body>
            <p>Contact us at info@example.com</p>
            <p>Sales: sales@example.com</p>
        </body>
    </html>
    """
    
    results = extract_emails(html, min_confidence=0.5)
    emails = [r['email'] for r in results]
    
    assert 'info@example.com' in emails
    assert 'sales@example.com' in emails
    assert len(results) == 2

def test_extract_emails_filters_spam():
    """Test that spam emails are filtered out."""
    html = """
    <html>
        <body>
            <p>Contact: real@company.com</p>
            <p>Test: noreply@example.com</p>
        </body>
    </html>
    """
    
    results = extract_emails(html, min_confidence=0.7)
    emails = [r['email'] for r in results]
    
    assert 'real@company.com' in emails
    # noreply should be filtered due to low confidence
    assert 'noreply@example.com' not in emails

def test_calculate_confidence():
    """Test confidence scoring."""
    # Good email
    assert calculate_confidence('john.doe@company.com') > 0.7
    
    # Spam indicator
    assert calculate_confidence('noreply@example.com') < 0.5
    
    # Image file
    assert calculate_confidence('image.png@test.com') < 0.3

def test_extract_emails_deduplication():
    """Test that duplicate emails are removed."""
    html = """
    <html>
        <body>
            <p>Email: contact@example.com</p>
            <p>Also: contact@example.com</p>
            <p>Again: CONTACT@EXAMPLE.COM</p>
        </body>
    </html>
    """
    
    results = extract_emails(html, min_confidence=0.5)
    
    # Should only have one email (case-insensitive dedup)
    assert len(results) == 1
    assert results[0]['email'] == 'contact@example.com'

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
