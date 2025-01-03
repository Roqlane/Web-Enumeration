import json
import argparse
import time
from colors import *
from search import Search
from wordlist import LoadWordlists


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
    
def getEndpoints(wordlists, loader: LoadWordlists):
    data = []
    for w in wordlists:
        for e in loader.getWordlist(w):
            data.append(e)
            
    return data
    
def main(args):    
    urls_found = []

    wordlistLoader = LoadWordlists(CONFIG_PATH)
    searcher = Search()
    
    targetUrl = searcher.get_url(args.url)
    wordlists = args.wordlists
    enumType = None
    extensions = args.extensions
    statusCode = args.status_codes
    cookies = args.cookies
    headers = args.headers
    
    # if no wordlists were given, take from the default ones
    if args.wordlists == None:
        enumType = args.type
        wordlists = wordlistLoader.getConfigWordlists(enumType)
        
    endpoints = getEndpoints(wordlists, wordlistLoader)
    
    print(f"Wordlists:  {', '.join(wordlists)}")
    print(f"Extension: {', '.join(extensions)}")
    print(f"Status Codes: {', '.join(statusCode)}")
            
    displayNumberOfRequests(endpoints, extensions)
    

    searcher.run_search(targetUrl, endpoints,
        headers, cookies, extensions, statusCode, urls_found)
    
            
if __name__ == "__main__":
    banner()
    start = time.time()    
    
    parser = argparse.ArgumentParser(description="Enum a webpage asynchronously \
                        with different wordlists")
    parser.add_argument("url", help="Url to scan")
    parser.add_argument("-w", "--wordlists", nargs='+', help="You can enter a single or several \
                        wordlists that will be used for the enumeration")
    parser.add_argument("-type", choices=["backup", "config", "hidden", "common", "custom", "all"], \
                        help="If no wordlists were to be entered, you could chose which type of file \
                        to search with the provided wordlists (default: all)", default="all")
    parser.add_argument("-x", "--extensions", help="The extensions that will be added to each \
                        endpoint of wordlist", nargs='+', default=[""])
    parser.add_argument("-sc", "--status-codes", help="The status codes that will be returned \
                        (default: 200)", default=['200'], nargs='+')
    parser.add_argument("-H", "--headers", help="Headers you would like to add to the requests. \
                        Example: {\"key1\":\"value1\", \"key2\":\"value2\"}", type=json.loads)
    parser.add_argument("-c", "--cookies", help="Cookies you would like to add to the requests. \
                        Example: {\"key1\":\"value1\", \"key2\":\"value2\"}", type=json.loads)
    #parser.add_argument("-R", "--recursive", help="Search the page recursively", default=False, action='store_true')

    args = parser.parse_args()
    
    main(args)
    
    print("\nFinished in %ss" % (time.time() - start))


            