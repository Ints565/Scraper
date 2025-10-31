"""
Step 1: Fetch product names from Supabase and convert to hind.ee URLs
"""
import os
import re
from supabase import create_client, Client

# Initialize Supabase client from environment
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Missing SUPABASE_URL or SUPABASE_KEY environment variables")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_products_from_supabase():
    """
    Fetch product names from Supabase (Model column)
    Returns a list of product names
    """
    try:
        # Query the Model column from your table
        # Update 'your_table_name' with your actual table name
        response = supabase.table('Lenovoarvutid').select('model').execute()
        
        if response.data:
            products = [item['model'] for item in response.data if item.get('model')]
            print(f"✅ Found {len(products)} products from Supabase")
            return products
        else:
            print("⚠️ No products found in database")
            return []
    
    except Exception as e:
        print(f"❌ Error fetching from Supabase: {e}")
        return []

def product_name_to_hindee_url(product_name):
    """
    Convert a product name to hind.ee URL format
    Example: "Lenovo ThinkPad T14 Gen 4" -> "lenovo-thinkpad-t14-gen-4"
    """
    # Convert to lowercase
    url_slug = product_name.lower()
    
    # Replace spaces with hyphens
    url_slug = url_slug.replace(' ', '-')
    
    # Remove special characters, keep only alphanumeric and hyphens
    url_slug = re.sub(r'[^a-z0-9\-]', '', url_slug)
    
    # Remove multiple consecutive hyphens
    url_slug = re.sub(r'--+', '-', url_slug)
    
    # Construct the full URL
    full_url = f"https://www.hind.ee/p/{url_slug}"
    
    return full_url

def fetch_all_product_urls():
    """
    Main function: Get products from Supabase and convert to URLs
    Returns list of URLs ready to scrape
    """
    product_names = get_products_from_supabase()
    
    if not product_names:
        # Fallback: return hardcoded products for testing
        print("📝 Using fallback products for testing")
        # product_names = [
        #     "Lenovo ThinkPad T14 Gen 4",
        #     "Lenovo ThinkPad L14 Gen 5",
        #     "Lenovo ThinkPad Z13"
        # ]
    
    urls = []
    for product_name in product_names:
        url = product_name_to_hindee_url(product_name)
        urls.append(url)
        print(f"🔗 {product_name} -> {url}")
    
    return urls

if __name__ == "__main__":
    urls = fetch_all_product_urls()
    print(f"\n✅ Generated {len(urls)} URLs ready to scrape")

