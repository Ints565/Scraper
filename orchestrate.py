"""
Main orchestrator: Combines all three steps into one workflow
"""
import asyncio
from datetime import datetime

# Import our three steps
import importlib.util

# Load module from filename with numbers
def load_module(filepath):
    spec = importlib.util.spec_from_file_location("module", filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

step1 = load_module('1_fetch_product_urls.py')
step2 = load_module('2_scrape_product.py')
step3 = load_module('3_save_to_sheets.py')

async def main():
    print("🚀 Starting laptop price monitoring pipeline\n")
    print("="*80 + "\n")
    
    # Step 1: Fetch product URLs from Supabase
    print("📊 STEP 1: Fetching product URLs from Supabase")
    print("-" * 80)
    urls = step1.fetch_all_product_urls()
    print(f"✅ Got {len(urls)} URLs\n")
    
    # Step 2: Scrape all products
    print("🔍 STEP 2: Scraping product data")
    print("-" * 80)
    products_data = await step2.scrape_multiple_products(urls)
    print(f"✅ Scraped {len(products_data)} products\n")
    
    # Step 3: Save to storage
    print("💾 STEP 3: Saving data")
    print("-" * 80)
    
    # Choose your storage method:
    # step3.save_to_csv(products_data)
    # save_to_supabase(products_data)
    step3.save_to_google_sheets(products_data)  # Requires credentials setup
    
    print("\n" + "="*80)
    print("✅ Pipeline complete!")
    print("="*80)

if __name__ == "__main__":
    asyncio.run(main())

