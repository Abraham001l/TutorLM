import crawl4ai.html2text
from scraper_pipeline import Scheduler, Crawler, create_google_query_url, save_to_text, web_query_to_data
import asyncio
import crawl4ai
import json

content = asyncio.run(web_query_to_data('how to do matrix multiplication', [], 1))

for i in range(len(content)):
    save_to_text(f'{i}.txt', content[i])



