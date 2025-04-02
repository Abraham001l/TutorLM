import crawl4ai.html2text
from scraper_pipeline import Scheduler, Crawler, create_google_query_url, save_to_text, web_query_to_data
import asyncio
import crawl4ai
import json

content = asyncio.run(web_query_to_data('Fuego Tortilla Grill Reviews', [], 1))
json_data = {}
for i in range(len(content)):
    json_data[f'data{i}'] = content[i]
json_string = json.dumps(json_data)
print(json_string)



