"""
Scrape a single website and save the HTML content.
"""
import sys
import requests
from pathlib import Path
import json
from datetime import datetime
import hashlib

def scrape_single_site(url, output_dir=".tmp/scraped_html", timeout=30, user_agent=None):
    """
    Scrape a single website and save HTML content.
    
    Args:
        url: Target URL to scrape
        output_dir: Directory to save scraped HTML
        timeout: Request timeout in seconds
        user_agent: Custom user agent string
    
    Returns:
        dict: Result with status, file_path, and metadata
    """
    try:
        # Setup
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        headers = {
            'User-Agent': user_agent or 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Fetch page
        print(f"Fetching: {url}")
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        
        # Generate filename from URL hash
        url_hash = hashlib.md5(url.encode()).hexdigest()
        filename = f"{url_hash}.html"
        filepath = output_path / filename
        
        # Save HTML
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        # Save metadata
        metadata = {
            'url': url,
            'status_code': response.status_code,
            'timestamp': datetime.now().isoformat(),
            'content_length': len(response.text),
            'filename': filename
        }
        
        metadata_path = output_path / f"{url_hash}_meta.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"✓ Saved to: {filepath}")
        return {
            'success': True,
            'url': url,
            'file_path': str(filepath),
            'metadata': metadata
        }
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Error scraping {url}: {e}")
        return {
            'success': False,
            'url': url,
            'error': str(e)
        }
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return {
            'success': False,
            'url': url,
            'error': str(e)
        }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scrape_single_site.py <url> [output_dir]")
        sys.exit(1)
    
    url = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else ".tmp/scraped_html"
    
    result = scrape_single_site(url, output_dir)
    print(json.dumps(result, indent=2))
