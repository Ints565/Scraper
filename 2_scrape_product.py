"""
Step 2: Scrape product data from hind.ee
Takes a URL and returns structured product data
"""
import asyncio
import re
from crawl4ai import AsyncWebCrawler
from bs4 import BeautifulSoup

async def scrape_product_data(url):
    """
    Scrape a single product from hind.ee
    Returns dictionary with product information
    """
    async with AsyncWebCrawler(
        verbose=False,
        headless=True
    ) as crawler:
        result = await crawler.arun(
            url=url,
            delay_before_return_html=3.0
        )
        
        soup = BeautifulSoup(result.html, 'html.parser')
        
        # Get product name
        product_name = soup.find('h1')
        product_name_text = product_name.text.strip() if product_name else 'Not found'
        
        print(f"\n📦 Scraping: {product_name_text}")
        
        # Find the sellers groups section
        sellers_groups = soup.find('div', class_='sellers-group')
        
        if not sellers_groups:
            print("⚠️ No sellers found")
            return {
                'product_name': product_name_text,
                'product_url': url,
                'offers': []
            }
        
        # Find all item-table-wrap divs with offers
        offers = sellers_groups.find_all('div', class_='item-table-wrap', itemprop='offers')
        print(f"   Found {len(offers)} offers")
        
        # Collect all offers for this product
        product_offers = []
        
        for i, offer in enumerate(offers[:3], 1):  # Top 3 cheapest
            # Find the specific td with class "col-7" that contains store info
            store_td = offer.find('td', class_='col-7')
            
            if store_td:
                # Find the tablet-show div inside the td
                tablet_show = store_td.find('div', class_='tablet-show')
                
                if tablet_show:
                    # Get the store link
                    store_data = tablet_show.find('a')
                    store_link = store_data.get('href', 'No link found') if store_data else 'Not found'
                    
                    # Extract store name from onclick attribute
                    onclick = store_data.get('onclick', '') if store_data else ''
                    match = re.search(r"'eventCategory':\s*'([^']+)'", onclick)
                    store_name = match.group(1) if match else "Unknown"
                    
                    # Get the price from inside the link
                    price_div = store_data.find('div', class_='price') if store_data else None
                    price_text = price_div.text.strip() if price_div else 'Not found'
                    
                    # Extract numeric price value
                    price_match = re.search(r'(\d+\.?\d*)', price_text.replace('€', '').replace(',', '.'))
                    price_value = float(price_match.group(1)) if price_match else 0.0
                    
                    offer_data = {
                        'position': i,
                        'store_name': store_name,
                        'store_link': store_link,
                        'price_text': price_text,
                        'price_value': price_value
                    }
                    
                    product_offers.append(offer_data)
                    print(f"   {i}. {store_name} - {price_text}")
        
        return {
            'product_name': product_name_text,
            'product_url': url,
            'offers': product_offers
        }

# Getting the URLS 

async def scrape_multiple_products(urls):
    """
    Scrape multiple product URLs
    Returns list of product data dictionaries
    """
    all_products = []

    # TEMP: collect failed URLs during this run
    failed_urls = []  # TEMP

    # TEMP: debug show what we received
    print(f"🔍 DEBUG: Received {len(urls)} URLs to scrape")  # TEMP
    for i, dbg_url in enumerate(urls[:10], 1):  # TEMP: preview first 10
        print(f"   {i}. {dbg_url}")  # TEMP
    
    for url in urls:
        try:
            print(f"\n🌐 Scraping: {url}")  # TEMP
            product_data = await scrape_product_data(url)
            all_products.append(product_data)

            # TEMP: consider it failed if no offers collected
            if not product_data.get('offers'):
                failed_urls.append(url)
        except Exception as e:
            failed_urls.append(url)
            print(f"❌ Error scraping {url}: {e}")  # TEMP
        
        print("\n" + "="*80 + "\n")
    
    # TEMP: dump failed URLs at the end for copy/paste
    if failed_urls:
        print("⛔ Failed URLs (TEMP):")
        for u in failed_urls:
            print(u)
        try:
            with open("failed_urls.txt", "w") as f:
                f.write("\n".join(failed_urls))
            print("💾 Wrote failed_urls.txt")
        except Exception:
            pass

    return all_products

async def main():
    # For testing - this will be replaced when we integrate with step 1
    test_urls = [
        "https://www.hind.ee/p/lenovo-thinkpad-t14-gen-4",
        "https://www.hind.ee/p/lenovo-thinkpad-l14-gen-5"
    ]
    
    products = await scrape_multiple_products(test_urls)
    print(f"\n✅ Scraped {len(products)} products")
    return products

if __name__ == "__main__":
    asyncio.run(main())

