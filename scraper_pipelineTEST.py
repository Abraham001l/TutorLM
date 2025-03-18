from scraper_pipeline import Scheduler, Crawler, create_google_query_url
import asyncio

schd = Scheduler()
url = create_google_query_url('new ikea chairs', 2, 0)
crawler = Crawler(url, ['ikea', 'chairs'], schd, 1)

content = asyncio.run(crawler.crawl())
print(content)