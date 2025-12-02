"""
Scrape multiple websites concurrently.
"""
import sys
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from scrape_single_site import scrape_single_site

def scrape_multiple_sites(urls, output_dir=".tmp/scraped_html", max_workers=3, timeout=30):
    """
    Scrape multiple websites concurrently.
    
    Args:
        urls: List of URLs to scrape
        output_dir: Directory to save scraped HTML
        max_workers: Number of concurrent workers
        timeout: Request timeout in seconds
    
    Returns:
        dict: Results summary with successes and failures
    """
    results = {
        'total': len(urls),
        'successful': 0,
        'failed': 0,
        'details': []
    }
    
    print(f"Scraping {len(urls)} URLs with {max_workers} workers...")
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_url = {
            executor.submit(scrape_single_site, url, output_dir, timeout): url 
            for url in urls
        }
        
        # Process completed tasks
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                result = future.result()
                results['details'].append(result)
                
                if result['success']:
                    results['successful'] += 1
                else:
                    results['failed'] += 1
                    
            except Exception as e:
                print(f"✗ Exception for {url}: {e}")
                results['failed'] += 1
                results['details'].append({
                    'success': False,
                    'url': url,
                    'error': str(e)
                })
    
    print(f"\n✓ Completed: {results['successful']}/{results['total']} successful")
    return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scrape_multiple_sites.py <urls_file> [output_dir] [max_workers]")
        print("  urls_file: Text file with one URL per line")
        sys.exit(1)
    
    urls_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else ".tmp/scraped_html"
    max_workers = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    
    # Read URLs from file
    with open(urls_file, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]
    
    results = scrape_multiple_sites(urls, output_dir, max_workers)
    
    # Save results
    output_path = Path(output_dir)
    results_file = output_path / "scraping_results.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: {results_file}")
