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
    n = len(endpoints * (len(extensions) + 1))
    print(f"\nLoading {n} requests... This process can take time.\n")
    
def getEndpoints(wordlists, loader: LoadSettings):
    data = []
    for w in wordlists:
        for e in loader.getFileData(w):
            data.append(e)
            
    return data

def fuzzWordExists(url, cookies, headers, params):
    if "FUZZ" in url:
        return True
    print(params)
    if params != None:
        if "FUZZ" in params.keys() or "FUZZ" in params.values():
            return True
    if cookies != None:
        if "FUZZ" in cookies.keys() or "FUZZ" in cookies.values():
            return True
    if headers != None:
        if "FUZZ" in headers.keys() or "FUZZ" in headers.values():
            return True
        
    return False
            
    
    
def main(args):    
    urls_found = []
    settingsLoader = LoadSettings(CONFIG_PATH)
    
    target_url = args.url
    wordlists = args.wordlists
    enumType = args.type
    extensions = args.extensions
    mode = args.mode
    
    hidden_status_codes = args.hidden_codes
    status_codes = args.status_codes
    hidden_filesizes = args.hidden_sizes
    cookies = args.cookies
    headers = args.headers
    method = args.method
    params = args.params
    error_response = args.error
    
    if args.params:
        try:
            json.loads(args.params)
        except ValueError:
            extracted = args.params.split("&")
            extracted = [e.split("=") for e in extracted]
            params = dict()
            for e in extracted:
                try:
                    params[e[0]] = e[1]
                except Exception as e:
                    print("Bad parameters format:" + str(e))
                    
            
    
    timeout = args.timeout
    time_interval = args.time_interval
    max_concurrency = args.max_concurrency
    
    if (mode == "fuzz" or mode == "force") and not fuzzWordExists(target_url, cookies, headers, params):
        exit("Error: FUZZ is missing.")
        
    if mode == "force" and (params == None or args.error == None):
        exit("Force mode used but it is missing: --params or --error") 
    
    if wordlists == None:
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

    searcher = Search(target_url, method,  cookies, headers, extensions, status_codes, timeout, 
            time_interval, max_concurrency, mode, params, error_response, hidden_status_codes, hidden_filesizes)
        
    endpoints = getEndpoints(wordlists, settingsLoader)
    
    print(f"Wordlists:  {', '.join(wordlists)}")
    print(searcher)
    displayNumberOfRequests(endpoints, extensions)

    searcher.run_search(endpoints, urls_found)
    
            
if __name__ == "__main__":
    banner()
    start = time.time()    
    
    parser = argparse.ArgumentParser(description="Perform a website enumeration asynchronously \
                        with different wordlists", usage="python3 WebEnum.py url [options]")
    parser.add_argument("url", help="Url to scan")
    parser.add_argument("-w", "--wordlists", nargs='+', help="You can enter a single or several \
                        wordlists that will be used for the enumeration")
    parser.add_argument("-x", "--extensions", help="The extensions that will be added to each \
                        endpoint of wordlist", nargs='+')
    parser.add_argument("-xf", "--extensions-file", help="File containing extensions")
    parser.add_argument("-sc", "--status-codes", help="The status codes that will be returned \
                        (default: 200,204,301,302,307,401,403)", nargs='+')
    parser.add_argument("-hc", "--hidden-codes", help="Hide requests with these status codes", nargs='+', default=[])
    parser.add_argument("-hs", "--hidden-sizes", help="Hide requests with these sizes", nargs='+', default=[])
    parser.add_argument("-H", "--headers", help="Headers you would like to add to the requests. \
                        Example: {\"key1\":\"value1\", \"key2\":\"value2\"}", type=json.loads)
    parser.add_argument("-Hf", "--headers-file", help="File containing headers (json format)")
    parser.add_argument("-c", "--cookies", help="Cookies you would like to add to the requests. \
                        Example: {\"key1\":\"value1\", \"key2\":\"value2\"}", type=json.loads)
    parser.add_argument("-cf", "--cookies-file", help="File containing cookies (json format)")
    parser.add_argument("-m", "--method", help="You can chose which request mode you want to use", 
                        choices=["GET","POST","PUT","DELETE"],default="GET")
    parser.add_argument("--type", help="If no wordlists were to be entered, you could chose which \
                        type of file (backup, common...) to search with the provided wordlists \
                        (default: all)", default="all")
    parser.add_argument("--timeout", help="Stop sending requests after this long (s)", type=int)
    parser.add_argument("--time-interval", help="Time to wait between each request (s)", type=float)
    parser.add_argument("--max-concurrency", help="Number of simultaneous requests", type=int)
    parser.add_argument("--mode", choices=["dir", "vhost", "fuzz", "force"], default="dir", help="""
                        Dir mode: perform directory enumeration (Default)
                        Vhost mode: perform vhost enumeration by setting the Host header with the wordlist content
                        Fuzzing mode: perform fuzzing on headers value, cookies value, [GET|POST|PUT|DELETE] parameters
                        Force mode: same as fuzz mode except it requires the --error field to confirm the success of the attack
                        \n The word FUZZ needs to be included. You can include FUZZ inside multiple fields.
                        You can choose to put the FUZZ keyword inside the url.
                        Example:
                            python3 WebEnum.py http://localhost/login --mode fuzz --method POST --params \"login=admin&password=FUZZ\"
                            or '{\"login\":\"admin\",\"password\":\"FUZZ\"}'
                            python3 WebEnum.py http://localhost/import?file=FUZZ --mode fuzz
                            python3 WebEnum.py http://localhost/login --mode force -H {\"session\":\"FUZZ\"} --error "Incorrect session"
                            python3 WebEnum.py http://localhost/ --mode vhost -w SecLists-master/Discovery/DNS/subdomains-top1million-110000.txt
                        """)
    parser.add_argument("--params", help="Json or POST data format")
    parser.add_argument("--error", help="Works with force mode. It must contains the response in case of incorrect indredentials")
    #parser.add_argument("-R", "--recursive", help="Search the page recursively", default=False, action='store_true')

    args = parser.parse_args()
    
    main(args)
    
    print("\nFinished in %ss" % (time.time() - start))


            