import requests
import time
from dotenv import load_dotenv
import os
from filelock import FileLock

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


