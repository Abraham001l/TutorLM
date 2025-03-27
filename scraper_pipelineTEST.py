import crawl4ai.html2text
from scraper_pipeline import Scheduler, Crawler, create_google_query_url, save_to_text, web_query_to_data
import asyncio
import crawl4ai

content = asyncio.run(web_query_to_data('how to solve friction on a ramp problems', ['friction', 'ramp'], 1))

    
for i in range(len(content)):
    save_to_text(f'{i}.txt', content[i])

# testing crawl4ai html2text
# converter = crawl4ai.html2text.HTML2Text()
# converter.ignore_links = True
# converter.ignore_images = True
# html = asyncio.run(schd.request_url('https://www.housedigest.com/1639830/ikea-gray-toilet-paper-cons/'))
# markdown = converter.handle(html)
# print(markdown)

