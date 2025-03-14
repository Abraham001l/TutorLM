import requests
import time
from dotenv import load_dotenv
import os
from filelock import FileLock
from bs4 import BeautifulSoup
import asyncio

# ---------- Scheduler Class ----------
class Scheduler:
    def __init__(self):
        load_dotenv()
        self.queue = []
        self.scraped_urls = []
        self.active_threads = 0
        self.scraper_api_key = os.getenv("SCRAPER_API_KEY")
    
    # ---------- Fetch HTML Function ----------
    def fetch_html(self, url):
        time.sleep(2)
        proxies = {"http": f"http://scraperapi:{self.scraper_api_key}@proxy-server.scraperapi.com:8001"}
        html = requests.get(url,proxies=proxies, verify=False)
        return html
    
    # ---------- Request URL Function ----------
    def request_url(self, url):
        # Add to scraped urls
        self.scraped_urls.append(url)

        # Add to queue
        self.add_to_queue(url)

        # Wait for free slot
        self.get_free_slot(url)

        # Update active threads & remove from queue
        self.active_threads += 1
        self.queue.pop(0)

        # Try to get html
        html = self.fetch_html(url)
        return html
 
    # ---------- Add To Queue Function ----------
    def add_to_queue(self, url):
        # Attempt to get lock
        lock = FileLock('queue_lock.txt.lock', timeout=5)
        try:
            with lock:
                self.queue.append(url)
        except Exception:
            self.add_to_queue(url)
    
    # ---------- Get Free Slot Function ----------
    def get_free_slot(self, url):
        # Wait until at the front of the queue
        while (self.queue.index(url)>0):
            time.sleep(1000)
        
        # Wait until thread opens
        while (self.active_threads>=5):
            time.sleep(1000)

# ---------- Crawler Class ----------
class Crawler:
    def __init__(self, url, keywords, schd, gen):
        self.url = url
        self.keywords = keywords
        self.schd = schd
        self.gen = gen
    
    # ---------- Crawl Function ----------
    async def crawl(self):
        # List to Store scraped content
        scraped_content = []

        # Attempt to get the html
        try:
            html = self.schd.request_url(self.url)
        except Exception:
            return scraped_content
        
        # Check if content is valuable
        if not self.is_valuable(html):
            return scraped_content
        
        # Scrape html
        # TODO
        dummy_scrape = self.url

        # Extract links to crawl & purge bad links
        branch_urls = self.extract_urls(html)
        self.purge_bad_urls(branch_urls)

        # Explore url branches
        crawler_objs = [Crawler(url,self.keywords,
                                self.schd,self.gen+1) for url in branch_urls]
        branch_content = await asyncio.gather(*[crawler.crawl() for crawler in crawler_objs])
        
        # Adding all content to scraped_content & returning it
        scraped_content.extend([dummy_scrape, branch_content])
        return scraped_content

    # ---------- HTML Value Check Function ----------
    def is_valuable(self, html):
        for word in self.keywords:
            if word in html:
                return True
        return False
    
    # ---------- Extract Links Function ----------
    def extract_urls(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        urls = [url.get('href') for url in soup.find_all('a')]
        return urls
    
    # ---------- Purge Bad Links Function ----------
    def purge_bad_urls(self, urls):
        # Purging already visited urls & urls with google.
        i = 0
        while i < len(urls):
            url = urls[i]
            if (url in self.schd.scraped_urls) or ('google.' in url):
                urls.pop(i)
                i -= 1
            i += 1

def create_google_query_url(query, n_results, n_start):
    return f'https://www.google.com/search?q={query}&start={n_start}&num={n_results}&tbm=nws&hl=en&lr=en'