import crawl4ai.html2text
from scraper_pipeline import Scheduler, Crawler, create_google_query_url
import asyncio
import crawl4ai

schd = Scheduler()
# url = create_google_query_url('new ikea chairs', 2, 0)
# crawler = Crawler(url, ['ikea', 'chairs'], schd, 1)
# content = asyncio.run(crawler.crawl())
# print(content)

# testing crawl4ai html2text
converter = crawl4ai.html2text.HTML2Text()
converter.ignore_links = True
converter.ignore_images = True
html = asyncio.run(schd.request_url('https://www.housedigest.com/1639830/ikea-gray-toilet-paper-cons/'))
markdown = converter.handle(html)
print(markdown)

