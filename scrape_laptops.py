import asyncio
import re
from crawl4ai import AsyncWebCrawler
from bs4 import BeautifulSoup

# Initialize Supabase client
# url = "https://muegxjihaepqayvwuyjz.supabase.co"  # Your Project URL
# key = "your-service-role-key-here"  # Your service role key
# supabase: Client = create_client(url, key)

async def scrape_laptop(url):
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
        print(f"\nProduct: {product_name_text}")
        
        # Find the sellers groups section
        sellers_groups = soup.find('div', class_='sellers-group')
        if sellers_groups:
            # Find all item-table-wrap divs with offers
            offers = sellers_groups.find_all('div', class_='item-table-wrap', itemprop='offers')
            print(f"\nFound {len(offers)} offers:")
            
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
                        price = price_div.text.strip() if price_div else 'Not found'
                        
                        print(f"{i}. Store Name: {store_name}")
                        print(f"   Store Link: {store_link}")
                        print(f"   Price: {price}")

                    else:
                        print(f"{i}. No tablet-show div found")
                else:
                    print(f"{i}. No col-7 td found")
        else:
            print("No sellers-groups found")

async def main():
    urls = [
        "https://www.hind.ee/p/lenovo-thinkpad-t14-gen-4",
        "https://www.hind.ee/p/lenovo-thinkpad-l14-gen-5",
        "https://www.hind.ee/p/lenovo-thinkpad-thinkpad-z13"
    ]
    
    for url in urls:
        await scrape_laptop(url)
        print("\n" + "="*80 + "\n")  # Separator between laptops

asyncio.run(main())