import csv
import os

def save_lead(data, filename='leads.csv'):
    file_exists = os.path.isfile(filename)
    
    with open(filename, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['Company', 'URL', 'Email', 'Description', 'Source'])
        
        if not file_exists:
            writer.writeheader()
            
        writer.writerow(data)
    print(f"Saved lead to {filename}")

lead_data = {
    'Company': 'HelioAI',
    'URL': 'https://helioai.tech',
    'Email': 'priyansh@helioai.tech',
    'Description': 'eCommerce Shopping AI Agent For Shopify',
    'Source': 'Scraped'
}

if __name__ == "__main__":
    save_lead(lead_data)
