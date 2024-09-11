import json
import argparse
import time
import aiohttp
import asyncio
import math

RED = "\33[91m"
BLUE = "\33[94m"
GREEN = "\033[32m"
YELLOW = "\033[93m"
PURPLE = '\033[0;35m' 
CYAN = "\033[36m"
END = "\033[0m"

CONFIG_PATH = "config.json"

def banner():
    font = f"""{BLUE}
---------
WebEnum 
---------{END}"""
    print(font)

def getWordlistsJson(path):
    data = ""
    try:
        with open(path, "r") as configFile:
            data = json.loads(configFile.read())
    except :
        print("Error while opening the config file: " + path)
        
    return data

def getWordlist(path):
    data = []
    try:
        with open(path, "r") as f:
            data = f.readlines()
    except:
        print("Error while opening the file: " + path)
        
    return data

def getConfigWordlists(data):
    lst = [];
    for elt in data["files"]:
        lst.append(data["files"][elt])
        
    return lst

def getUrl(url):
    finalUrl = ""
    if "http" not in url and "https" not in url:
        finalUrl = "http://" + url
    else:
        finalUrl = url
        
    if finalUrl[-1] != '/':        
        finalUrl += '/'
        
    return finalUrl
    
def displayState(current, length):
    #print the progress of the enumeration
    state = math.ceil((current*100) / length)
    if (state != 0 and state % 10 == 0):
        if (state == 100):
            print(f"Launching search...", end="\r", flush=True)
        else:
            print(f"{state}%", end="\r", flush=True)
        

async def requestUrl(session, url, current, length):
    global results, statusCode
    url = url.replace('\n', '')
    try:
        displayState(current, length)
        async with session.get(url) as resp:
            if str(resp.status) in statusCode:
                print(f"{GREEN}[+] Found : {url.ljust(50)}Code : {resp.status}{END}")
                results.append((url,resp.status))
    except aiohttp.ClientError:
        print(f"{RED}[-] Failed : {url}{END}")

async def search(url, path):
    global headers, cookies, extensions, statusCode
    data = getWordlist(path)
    url = getUrl(url)
    urls = [url + endpoint + ext for endpoint in data for ext in extensions]
    urlsLength = len(urls)
    
    async with aiohttp.ClientSession(headers=headers, cookies=cookies) as session:
        tasks = [requestUrl(session, u, i, urlsLength) for (i,u) in enumerate(urls)]
        await asyncio.gather(*tasks)
        
def run_search(url, path):
    asyncio.run(search(url, path))
    
def main(args):
    global headers, cookies, extensions, statusCode
    wordlists = args.wordlists
    enumType = None
    extensions = args.extensions
    statusCode = args.status_codes
    cookies = args.cookies
    headers = args.headers
    if args.wordlists == None:
        enumType = args.type
        if enumType == "all":
            wordlists = getConfigWordlists(getWordlistsJson(CONFIG_PATH))
        else:
            wordlists = [getWordlistsJson(CONFIG_PATH)["files"][enumType]]
            
    
    for w in wordlists:
        print("Enumerating " + w)
        run_search(args.url, w)
    
            
if __name__ == "__main__":
    banner()
    start = time.time()    
    config = getWordlistsJson("config.json")
    
    parser = argparse.ArgumentParser(description="Enum a webpage asynchronously with the different wordlists either entered or using the premade config files")
    parser.add_argument("url", help="Url to scan")
    parser.add_argument("-w", "--wordlists", nargs='+', help="You can enter one or several wordlists that will be used for the enumeration")
    parser.add_argument("-type", choices=["backup", "config", "hidden", "common", "all"], help="If no wordlists were entered, you could chose which type of file to search (backup, config, hidden, common, all) (default: all)", default="all")
    parser.add_argument("-x", "--extensions", help="The extensions that will be added to each endpoint of wordlist", nargs='+', default=[""])
    parser.add_argument("-sc", "--status-codes", help="The status codes that will be returned (default: 200)", default=['200'], nargs='+')
    parser.add_argument("-H", "--headers", help="Headers you would like to add to the requests", type=json.loads)
    parser.add_argument("-c", "--cookies", help="Cookies you would like to add to the requests. You must set them a dictionary ({\"key\":\"value\"})", type=json.loads)
    #parser.add_argument("-R", "--recursive", help="Search the page recursively", default=False, action='store_true')

    args = parser.parse_args()
    
    main(args)


    #backup extension
    
    #config extension
    
    #type of search (backend, config, hidden, common, all) 
    
    #add extensions for common search
    
    #status code
    


    print("\nFinished in %ss" % (time.time() - start))


            