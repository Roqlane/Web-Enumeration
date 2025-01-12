import aiohttp
import asyncio
import signal
import ssl
from colors import *
from urllib.parse import urlparse


class Search:
    def __init__(self, url, method, cookies, headers, extensions, status_code,
                 timeout, time_interval, max_concurrency, fuzz_mode):
        self.fuzz_mode = fuzz_mode
        self.url = self.get_url(url)
        self.host = urlparse(self.url).netloc
        self.method = method
        self.cookies = cookies
        self.headers = headers
        self.status_code = status_code
        self.extensions = extensions
        self.timeout = timeout
        self.time_interval = time_interval
        self.max_concurrency = max_concurrency
        self.ssl_context = self.create_ssl_context()
        
    def create_ssl_context(self):
            # For ctf, the certificate may not be valid. This ignore this case.
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            
            return ssl_context
        
    async def is_server_up(self, session):
        """Send a request with a premade session to check if the target server is up"""
        try:            
            url = self.remove_fuzz_from_host()
            async with session.head(url, timeout=self.timeout, ssl=self.ssl_context) as response:
                return response.status < 500
        except Exception as e:
            print(f"{RED}[-] Server check failed : {e}{END}")
            return False
    
    def get_url(self, url):
        """Make sure the given url is in a valid format."""
        if not url.startswith(("http://", "https://")):
            url = f"http://{url}"
        if not url.endswith('/'):
            url += '/'
        
        return url
            
    async def request_url(self, session, semaphore, timeout, endpoint, currentIndex, endpoints_found):
        """Send the request"""
        #fuzz mode activated
        if self.fuzz_mode:
            #vhost enumeration
            if self.fuzz_in_host():
                self.set_host_header(endpoint)
                complete_url = self.remove_fuzz_from_host()
            else:
                complete_url = self.url.replace("FUZZ", endpoint)
        else:
            complete_url = self.url + endpoint
        async with semaphore:
            await asyncio.sleep(self.time_interval)
            try:
                async with session.request(self.method, complete_url, timeout=timeout,
                                           allow_redirects=False, ssl=self.ssl_context) as resp:
                    #content = await resp.read()
                    if self.fuzz_mode and self.fuzz_in_host():
                       print(f"{getColor(resp.status)}[+] {currentIndex} Found : {endpoint} (Code : {resp.status}){END}")   
                                     
                    elif str(resp.status) in self.status_code and endpoint not in endpoints_found:
                        print(f"{getColor(resp.status)}[+] {currentIndex} Found : {complete_url} (Code : {resp.status}){END}")
                        endpoints_found.append(endpoint)
            except aiohttp.ClientError as e:
                raise RuntimeError(e)
            except asyncio.TimeoutError as e:
                print(f"{RED}[-] Timeout : {complete_url}{END}")
            except Exception as e:
                print(e)
                print(f"{RED}[-] Failed : {complete_url}{END}")
            

    async def search_urls(self, wordlist, endpoints_found):
        """Add all requests in a pool"""
        async with aiohttp.ClientSession(headers=self.headers, cookies=self.cookies) as session:
            if await self.is_server_up(session):
                semaphore = asyncio.Semaphore(self.max_concurrency)
                timeout = aiohttp.ClientTimeout(total=self.timeout)
                endpoints = [endpoint + ext for endpoint in wordlist for ext in self.extensions]
                tasks = [self.request_url(session, semaphore, timeout, e, i, endpoints_found) for (i,e) in enumerate(endpoints)]
                try:
                    await asyncio.gather(*tasks)
                except RuntimeError as e:
                    print(f"{RED}[-] Error occurred : {e}{END}")
                    # Cancel all pending tasks
                    for task in asyncio.all_tasks():
                        if not task.done():
                            task.cancel()
                    print("Pending tasks cancelled.")    
                except asyncio.CancelledError:
                    raise
            
    def run_search(self, wordlist, endpoints_found):
        """Handle the enumeration. Stops if any errors"""
        loop = asyncio.get_event_loop()
        # Register the signal handler for Ctrl+C
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, lambda: self.shutdown(loop))
        
        try:
            loop.run_until_complete(self.search_urls(wordlist, endpoints_found))
        except asyncio.CancelledError:
            print("\nProcess terminated.")
        finally:
            loop.close()
                
    def shutdown(self, loop):
        """Signal handler to cancel tasks on Ctrl+C."""
        for task in asyncio.all_tasks(loop=loop):
            task.cancel()
            
    def fuzz_in_host(self):
        """Check if 'FUZZ' is in the host"""
        return 'FUZZ' in self.host

    def set_host_header(self, endpoint):
        self.headers["Host"] = self.host.replace("FUZZ", endpoint)
        
    def remove_fuzz_from_host(self):
        url = self.url
        if self.fuzz_mode and self.fuzz_in_host():
            url = url.replace("FUZZ.", "")
        return url