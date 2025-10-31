# Laptop Price Monitor

A modular price monitoring system that scrapes laptop prices from hind.ee and stores them in various backends.

## 📁 Project Structure

```
Scraper/
├── 1_fetch_product_urls.py    # Step 1: Get products from Supabase → URLs
├── 2_scrape_product.py         # Step 2: Scrape product data from hind.ee
├── 3_save_to_sheets.py         # Step 3: Save data to storage (CSV/Supabase/Sheets)
├── orchestrate.py              # Main script that runs all steps
├── scrape_laptops.py           # Clean version (no database)
├── scrape_laptops_supabase.py  # Full version with Supabase
└── requirements_full.txt       # All dependencies

```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements_full.txt
```

### 2. Configure Your Storage

**For Supabase:**
- Update credentials in `1_fetch_product_urls.py` and `3_save_to_sheets.py`
- Create `laptop_prices` table in Supabase

**For Google Sheets:**
- Download service account credentials
- Share your sheet with the service account email

### 3. Run the Pipeline
```bash
python orchestrate.py
```

Or run individual steps:
```bash
python 1_fetch_product_urls.py  # Step 1 only
python 2_scrape_product.py      # Step 2 only
python 3_save_to_sheets.py      # Step 3 only
```

## 📊 Data Flow

```
Supabase (Products)
    ↓
1_fetch_product_urls.py → Convert to hind.ee URLs
    ↓
2_scrape_product.py → Scrape price data
    ↓
3_save_to_sheets.py → Save to CSV/Supabase/Sheets
```

## 🔧 Configuration

### Supabase Setup
1. Create a Supabase account
2. Get your project URL and service key
3. Create tables:
   - `products` (for product names)
   - `laptop_prices` (for scraped data)

### Google Sheets Setup
1. Create a Google Cloud project
2. Enable Sheets API
3. Create service account and download JSON
4. Share your sheet with the service account email

## 📝 Features

- ✅ Modular design - each step is independent
- ✅ Multiple storage options (CSV, Supabase, Google Sheets)
- ✅ Scrapes top 3 cheapest prices per product
- ✅ Handles errors gracefully
- ✅ Clean separation of concerns

## 🎯 Usage Examples

**Basic scraping (no database):**
```bash
python scrape_laptops.py
```

**Full pipeline with Supabase:**
```bash
python orchestrate.py
```

**Custom:**
```python
from 1_fetch_product_urls import fetch_all_product_urls
from 2_scrape_product import scrape_multiple_products

urls = fetch_all_product_urls()
products = await scrape_multiple_products(urls)
```

## 📄 License

MIT

