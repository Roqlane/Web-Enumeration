import json
import argparse
import time
from colors import *
from search import Search
from settings import LoadSettings


CONFIG_PATH = "config.json"

def banner():
    font = f"""{BLUE}
-----------
| WebEnum |
-----------{END}"""
    print(font)
    
def displayNumberOfRequests(endpoints, extensions):
    n = 0
    for _ in endpoints:
        for _ in extensions:
            n += 1
        
    print(f"\nLoading {n} requests... This process can take time.\n")
    
def getEndpoints(wordlists, loader: LoadSettings):
    data = []
    for w in wordlists:
        for e in loader.getFileData(w):
            data.append(e)
            
    return data
    
def main(args):    
    urls_found = []
    settingsLoader = LoadSettings(CONFIG_PATH)
    
    target_url = args.url
    wordlists = args.wordlists
    enumType = None
    extensions = args.extensions
    status_codes = args.status_codes
    cookies = args.cookies
    headers = args.headers
    method = args.method
    timeout = args.timeout
    time_interval = args.time_interval
    max_concurrency = args.max_concurrency
    fuzz_mode = args.fuzz
    
    if wordlists == None:
        enumType = args.type
        wordlists = settingsLoader.getConfigWordlists(enumType)
    if status_codes == None:
            status_codes = settingsLoader.getSettings("status_codes")
    if extensions == None:        
        if args.extensions_file != None:
            extensions = settingsLoader.getFileData(args.extensions_file)
        else:
            extensions = settingsLoader.getSettings("extensions")
    if cookies == None:
        if args.cookies_file != None:
            cookies = settingsLoader.getCookies(args.cookies_file)
        else:
            cookies = settingsLoader.getSettings("cookies")
    if headers == None:
        if args.headers_file != None:
            headers = settingsLoader.getHeaders(args.headers_file)
        else:
            headers = settingsLoader.getSettings("headers")
    if timeout == None:
        timeout = settingsLoader.getSettings("timeout")
    if time_interval == None:
        time_interval = settingsLoader.getSettings("time_interval")
    if max_concurrency == None:
        max_concurrency = settingsLoader.getSettings("max_concurrency")

    searcher = Search(target_url, method,  cookies, headers, extensions, status_codes,
                    timeout, time_interval, max_concurrency)
        
    endpoints = getEndpoints(wordlists, settingsLoader)
    
    print(f"Wordlists:  {', '.join(wordlists)}")
    print(f"Extension: {', '.join(extensions)}")
    print(f"Status Codes: {', '.join(status_codes)}")
            
    displayNumberOfRequests(endpoints, extensions)

    searcher.run_search(endpoints, urls_found)
    
            
if __name__ == "__main__":
    banner()
    start = time.time()    
    
    parser = argparse.ArgumentParser(description="Enum a webpage asynchronously \
                        with different wordlists")
    parser.add_argument("-u", "--url", help="Url to scan")
    parser.add_argument("-w", "--wordlists", nargs='+', help="You can enter a single or several \
                        wordlists that will be used for the enumeration")
    parser.add_argument("-x", "--extensions", help="The extensions that will be added to each \
                        endpoint of wordlist", nargs='+')
    parser.add_argument("-xf", "--extensions-file", help="File containing extensions")
    parser.add_argument("-sc", "--status-codes", help="The status codes that will be returned \
                        (default: 200, 302)", nargs='+')
    parser.add_argument("-H", "--headers", help="Headers you would like to add to the requests. \
                        Example: {\"key1\":\"value1\", \"key2\":\"value2\"}", type=json.loads)
    parser.add_argument("-Hf", "--headers-file", help="File containing headers (json format)")
    parser.add_argument("-c", "--cookies", help="Cookies you would like to add to the requests. \
                        Example: {\"key1\":\"value1\", \"key2\":\"value2\"}", type=json.loads)
    parser.add_argument("-cf", "--cookies-file", help="File containing cookies (json format)")
    parser.add_argument("-m", "--method", help="You can chose which request mode you want to use", 
                        default="GET")
    parser.add_argument("--type", help="If no wordlists were to be entered, you could chose which \
                        type of file (backup, common...) to search with the provided wordlists \
                        (default: all)", default="all")
    parser.add_argument("--timeout", help="Stop sending requests after this long (s)", type=int)
    parser.add_argument("--time-interval", help="Time to wait between each request (s)", type=float)
    parser.add_argument("--max-concurrency", help="Number of simultaneous requests", type=int)
    parser.add_argument("--fuzz", help="Fuzzing mode: This works the same than in normal mode except \
                        you have to write \"FUZZ\" inside the url", action='store_true', default=False)
    #parser.add_argument("-R", "--recursive", help="Search the page recursively", default=False, action='store_true')

    args = parser.parse_args()
    
    main(args)
    
    print("\nFinished in %ss" % (time.time() - start))


            