import aiohttp
import asyncio
import signal
from colors import *

class Search:
    def __init__(self):
        pass
    
    def get_url(self, url):
        finalUrl = ""
        if "http" not in url and "https" not in url:
            finalUrl = "http://" + url
        else:
            finalUrl = url
            
        if finalUrl[-1] != '/':        
            finalUrl += '/'
            
        return finalUrl
            
    async def request_url(self, session, url, currentIndex, statusCode, urls_found):
        url = url.replace('\n', '')
        try:
            async with session.get(url) as resp:                
                if str(resp.status) in statusCode and url not in urls_found:
                    print(f"{GREEN}[+] {currentIndex} Found : {url.ljust(50)}Code : {resp.status}{END}")
                    urls_found.append(url)
        except aiohttp.ClientError:
            print(f"{RED}[-] Failed : {url}{END}")

    async def search_urls(self, url, wordlist, headers, cookies, extensions, statusCode, urls_found):
        """Adds all requests in a pool"""
        urls = [url + endpoint + ext for endpoint in wordlist for ext in extensions]
        
        async with aiohttp.ClientSession(headers=headers, cookies=cookies) as session:
            tasks = [self.request_url(session, u, i, statusCode, urls_found) for (i,u) in enumerate(urls)]
            try:
                await asyncio.gather(*tasks)
            except asyncio.CancelledError:
                print("Tasks were cancelled!")
                raise
            
    def run_search(self, url, wordlist, headers, cookies, extensions, statusCode, urls_found):
        loop = asyncio.get_event_loop()
        # Register the signal handler for Ctrl+C
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, lambda: self.shutdown(loop))
        
        try:
            loop.run_until_complete(self.search_urls(url, wordlist, headers, cookies, extensions, statusCode, urls_found))
        except asyncio.CancelledError:
            print("Process terminated")
        finally:
            loop.close()
                
    def shutdown(self, loop):
        """Signal handler to cancel tasks on Ctrl+C."""
        for task in asyncio.all_tasks(loop=loop):
            task.cancel()