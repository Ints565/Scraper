"""
Step 3: Save scraped product data to Google Sheets
"""
import os
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
import json
import csv

def save_to_google_sheets(products_data):
    """
    Save product data to Google Sheets
    products_data should be a list of product dictionaries from scraper
    """
    
    # Google Sheets setup (configurable via env)
    credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', '/Users/indrekvaher/Downloads/lenovoarvutid-36b91c2f7a61.json')
    spreadsheet_name = os.getenv('SHEETS_SPREADSHEET', 'Lenovo')
    worksheet_name = os.getenv('SHEETS_WORKSHEET', 'Prices')
    
    try:
        # Authenticate with Google Sheets
        scope = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
        creds = Credentials.from_service_account_file(credentials_path, scopes=scope)
        client = gspread.authorize(creds)
        
        # Open the spreadsheet
        spreadsheet = client.open(spreadsheet_name)
        try:
            worksheet = spreadsheet.worksheet(worksheet_name)
        except gspread.WorksheetNotFound:
            worksheet = spreadsheet.add_worksheet(title=worksheet_name, rows=1000, cols=10)
        
        # Columns to export (in order)
        headers = ['product_name', 'product_url', 'store_name', 'price_value', 'timestamp']
        
        # Ensure header row exists (append if empty)
        existing = worksheet.get_all_values()
        if not existing:
            worksheet.append_row(headers)
        
        # Prepare data for insertion
        rows_to_insert = []
        for product in products_data:
            for offer in product['offers']:
                row = [
                    product['product_name'],
                    product['product_url'],
                    offer['store_name'],
                    offer['price_value'],
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                ]
                rows_to_insert.append(row)
        
        if rows_to_insert:
            result = worksheet.append_rows(rows_to_insert)
            print(f"✅ Saved {len(rows_to_insert)} rows to Google Sheets")
            print(f"   Sheet URL: https://docs.google.com/spreadsheets/d/{spreadsheet.id}")
        else:
            print("⚠️ No data to save (empty offers)")
        
    except FileNotFoundError:
        print("❌ Credentials file not found. Please set GOOGLE_APPLICATION_CREDENTIALS")
    except gspread.exceptions.SpreadsheetNotFound:
        print(f"❌ Spreadsheet '{spreadsheet_name}' not found. Please create & share with:")
        print("   lenovarvutid@lenovoarvutid.iam.gserviceaccount.com")
    except gspread.exceptions.APIError as e:
        print(f"❌ Google Sheets API Error: {e}")
    except Exception as e:
        print(f"❌ Error saving to Google Sheets: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

def save_to_supabase(products_data):
    """
    Alternative: Save to Supabase instead
    """
    from supabase import create_client
    
    url = "https://muegxjihaepqayvwuyjz.supabase.co"
    key = "your-service-role-key-here"
    supabase = create_client(url, key)
    
    all_offers = []
    
    for product in products_data:
        for offer in product['offers']:
            all_offers.append({
                'product_name': product['product_name'],
                'product_url': product['product_url'],
                'store_name': offer['store_name'],
                'store_link': offer['store_link'],
                'price_text': offer['price_text'],
                'price_value': offer['price_value'],
                'position': offer['position'],
                'scraped_at': datetime.now().isoformat()
            })
    
    try:
        result = supabase.table('laptop_prices').insert(all_offers).execute()
        print(f"✅ Saved {len(all_offers)} offers to Supabase")
    except Exception as e:
        print(f"❌ Error saving to Supabase: {e}")

def save_to_csv(products_data, filename='laptop_prices.csv'):
    """
    Alternative: Save to CSV file
    """
    import csv
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['timestamp', 'product_name', 'product_url', 'position', 
                     'store_name', 'store_link', 'price_text', 'price_value']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for product in products_data:
            for offer in product['offers']:
                writer.writerow({
                    'timestamp': datetime.now().isoformat(),
                    'product_name': product['product_name'],
                    'product_url': product['product_url'],
                    'position': offer['position'],
                    'store_name': offer['store_name'],
                    'store_link': offer['store_link'],
                    'price_text': offer['price_text'],
                    'price_value': offer['price_value']
                })
    
    print(f"✅ Saved to {filename}")

if __name__ == "__main__":
    # For testing - this data would come from the scraper
    test_data = [
        {
            'product_name': 'Lenovo ThinkPad T14 Gen 4',
            'product_url': 'https://www.hind.ee/p/lenovo-thinkpad-t14-gen-4',
            'offers': [
                {
                    'position': 1,
                    'store_name': 'Itsupply.ee',
                    'store_link': 'https://...',
                    'price_text': '725.00 €',
                    'price_value': 725.0
                }
            ]
        }
    ]
    
    # Choose one of these:
    save_to_csv(test_data)
    # save_to_supabase(test_data)
    # save_to_google_sheets(test_data)

