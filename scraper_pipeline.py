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



# ---------- Scheduler Class ----------
class Scheduler:
    def __init__(self):
        load_dotenv()
        self.queue = []
        self.scraped_urls = []
        self.active_threads = 0
        self.semaphore = asyncio.Semaphore(5)
        self.scraper_api_key = os.getenv("SCRAPER_API_KEY")
        self.cert_path = 'proxyca.pem'
        self.ssl_context = ssl.create_default_context(cafile=self.cert_path)
    
    # ---------- Fetch HTML Function ----------
    async def fetch_html(self, url):
        print(url)
        await asyncio.sleep(2)
        proxy_url = f"http://scraperapi:{self.scraper_api_key}@proxy-server.scraperapi.com:8001"
        print('about to run')
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=self.ssl_context)) as session:
            async with session.get(url, proxy=proxy_url, ssl=self.ssl_context) as response:
                html = await response.text()
        print("ran")
        return html
    
    # ---------- Request URL Function ----------
    async def request_url(self, url):
        # Add to scraped urls
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
        except Exception:
            print('couldnt get html')
            return scraped_content
        
        # Check if content is valuable
        if not self.is_valuable(html):
            return scraped_content
        
        # Scrape html
        scrape = self.html2text.handle(html)

        # Limiting generations
        if self.gen == 3:
            scraped_content.extend([scrape, []])
            return scraped_content

        # Extract links to crawl & purge bad links
        branch_urls = self.extract_urls(html)
        self.purge_bad_urls(branch_urls)

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
    def purge_bad_urls(self, urls):
        # Purging already visited urls & urls with google.
        i = 0
        while i < len(urls):
            url = urls[i]
            if not url:
                urls.pop(i)
                i -= 1
            elif (url in self.schd.scraped_urls) or ('google.' in url):
                urls.pop(i)
                i -= 1
            i += 1
        print(len(urls))

def create_google_query_url(query, n_results, n_start):
    return f'https://www.google.com/search?q={query}&start={n_start}&num={n_results}&tbm=nws&hl=en&lr=en'