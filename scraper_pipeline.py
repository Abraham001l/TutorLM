import crawl4ai.html2text
import requests
import time
from dotenv import load_dotenv
import os
from filelock import FileLock
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import ssl
from aiolimiter import AsyncLimiter
import crawl4ai
import itertools
from asyncio import Lock

# ---------- Scheduler Class ----------
class Scheduler:
    def __init__(self):
        load_dotenv()
        self.queue = []
        self.scraped_urls = []
        self.scraped_urls_lock = Lock()
        self.active_threads = 0
        self.semaphore = asyncio.Semaphore(5)
        self.scraper_api_key = os.getenv('SCRAPER_API_KEY')
        self.cert_path = 'proxyca.pem'
        self.ssl_context = ssl.create_default_context(cafile=self.cert_path)
        self.google_search_api_key = os.getenv('GOOGLE_SEARCH_API_KEY')
        self.google_search_cx_key = os.getenv('GOOGLE_SEARCH_CX_KEY')
    
    # ---------- AIOHTTP Client Session Initializer ----------
    async def initialize_aiohttp(self):
        self.session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=self.ssl_context))

    # ---------- AIOHTTP Client Session Closer ----------
    async def close_aiohttp(self):
        await self.session.close()

    # ---------- AIOHTTP Client Session Initializer For Google Search Engine ----------
    async def initialize_aiohttp_google(self):
        self.google_session = aiohttp.ClientSession()

    # ---------- AIOHTTP Client Session Closer For Google Search Engine ----------
    async def close_aiohttp_google(self):
        await self.google_session.close()

    # ---------- Google Search Engine Query Function ----------
    async def fetch_google_search_results(self, query, n_start):
        custom_search_url = f'https://www.googleapis.com/customsearch/v1?key={self.google_search_api_key}&cx={self.google_search_cx_key}&q={query}&start={n_start}&num=10'
        async with self.google_session.get(custom_search_url) as response:
            r_json = await response.json()
        return r_json
    
    # ---------- Fetch HTML Function ----------
    async def fetch_html(self, url):
        print(url)
        await asyncio.sleep(2)
        proxy_url = f'http://scraperapi:{self.scraper_api_key}@proxy-server.scraperapi.com:8001'
        async with self.session.get(url, proxy=proxy_url, ssl=self.ssl_context) as response:
            html = await response.text()
        print("ran")
        return html
    
    # ---------- Request URL Function ----------
    async def request_url(self, url):
        # Add to scraped urls
        async with self.scraped_urls_lock:
            self.scraped_urls.append(url)

        async with self.semaphore:
            return await self.fetch_html(url)

# ---------- Crawler Class ----------
class Crawler:
    def __init__(self, url, keywords, schd, gen, html2text):
        self.url = url
        self.keywords = keywords
        self.schd = schd
        self.gen = gen
        self.html2text = html2text
    
    # ---------- Crawl Function ----------
    async def crawl(self):
        # List to Store scraped content
        scraped_content = []

        # Attempt to get the html
        try:
            html = await self.schd.request_url(self.url)
        except Exception as e:
            print(e)
            return scraped_content
        
        # Check if content is valuable
        if not self.is_valuable(html):
            return scraped_content
        
        # Scrape html
        scrape = self.html2text.handle(html)

        # Limiting generations
        if self.gen+1 >= 2:
            scraped_content.extend([scrape])
            return scraped_content

        # Extract links to crawl & purge bad links
        branch_urls = self.extract_urls(html)
        await self.purge_bad_urls(branch_urls)
        print(branch_urls)

        # Explore url branches
        crawler_objs = [Crawler(url,self.keywords,
                                self.schd,self.gen+1, self.html2text) for url in branch_urls]
        branch_content = await asyncio.gather(*[crawler.crawl() for crawler in crawler_objs])
        
        # Adding all content to scraped_content & returning it
        scraped_content.extend([scrape, branch_content])
        return scraped_content

    # ---------- HTML Value Check Function ----------
    def is_valuable(self, html):
        for word in self.keywords:
            if word in html:
                return True
        return False
    
    # ---------- Extract URL's Function ----------
    def extract_urls(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        urls = []
        for url in soup.find_all('a'):
            url = url.get('href')
            # Avoiding nonetypes
            if url:
                # Extracting only the destination url
                http_loc = url.find('http')
                if http_loc != -1:
                    url = url[url.index('http'):]
                    urls.append(url)
        return urls
    
    # ---------- Purge Bad Links Function ----------
    async def purge_bad_urls(self, urls):
        # Purging already visited urls & urls with google.
        async with self.schd.scraped_urls_lock:
            filtered = [
                url for url in urls
                if url and url not in self.schd.scraped_urls and 'google.' not in url and 'youtube.' not in url
            ]
        urls[:] = filtered

async def web_query_to_data(query, keywords, n_results):
    # Initilizing the scheduler and html2text converter
    schd = Scheduler()
    await schd.initialize_aiohttp()
    await schd.initialize_aiohttp_google()
    html2text = crawl4ai.html2text.HTML2Text()
    html2text.ignore_links = True
    html2text.ignore_images = True
    print('finished initializers')

    # Getting url's
    urls = []
    for n in range(1, n_results+1):
        try:
            r_json = await schd.fetch_google_search_results(query, n)
        except Exception as e:
            print(e)
            # Closing aiohttp sessions
            await schd.close_aiohttp()
            await schd.close_aiohttp_google()
            return []

        for url in range(len(r_json['items'])):
            urls.append(r_json['items'][url]['link'])
    
    print(f'got urls: {urls}')

    # Launching crawlers
    crawler_objs = [Crawler(url,keywords,schd,1,html2text) for url in urls]
    content = await asyncio.gather(*[crawler.crawl() for crawler in crawler_objs])

    print('got crawlers content')

    # Flattening content list and returning it
    content = flatten_list(content)

    print(f'flat content: {content}')

    # Closing aiohttp session
    await schd.close_aiohttp()
    await schd.close_aiohttp_google()

    return content

def flatten_list(nested_list):
    flattened = []
    for item in nested_list:
        if isinstance(item, list):
            flattened.extend(flatten_list(item))
        else:
            flattened.append(item)
    return flattened

def create_google_query_url(query, n_results, n_start):
    return f'https://www.google.com/search?q={query}&tbm=nws&start={n_start}&num={n_results}&hl=en&lr=en'


def save_to_text(filename, content):
    f = open(filename, 'w', encoding='utf-8')
    f.write(content)
    f.close()