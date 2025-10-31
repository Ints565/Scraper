import asyncio
from crawl4ai import AsyncWebCrawler

async def test_scrape():
    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(url="https://hind.ee")
        print("Success! Here's a sample of the content:")
        print(result.markdown[:500])  # First 500 characters

asyncio.run(test_scrape())
