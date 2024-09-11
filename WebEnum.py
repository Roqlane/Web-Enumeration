import json
import argparse
import time
import aiohttp
import asyncio

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
---------{END}                                                                                                                                                                             
    """
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
        finalUrl = "https://" + url
    else:
        finalUrl = url
        
    if finalUrl[-1] != '/':        
        finalUrl += '/'
        
    return finalUrl
    
def displayState(current, length):
    #print the progress of the enumeration
    state = (current * 100) // length
    if (state != 0 and state % 10 == 0):
        print(f"{state}%", end="\r", flush=True)
        
async def is_host_online(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.head(url) as resp:
                if 200 <= resp.status < 400:
                    return True
                else:
                    print(f"{RED}[-] Host {url} is offline. Status: {resp.status}{END}")
                    return False
                
    except aiohttp.ClientError as e:
        print(f"{RED}[-] Host {url} is unreachable. Error: {e}{END}")
        return False

async def requestUrl(session, url, statusCode, current, length):
    url = url.replace('\n', '')
    try:
        async with session.get(url) as resp:
            displayState(current, length)
                
            if str(resp.status) in statusCode:
                print(f"{GREEN}[+] Found : {url}\tCode : {resp.status}{END}")
    except aiohttp.ClientError:
        print(f"{RED}[-] Failed : {url}{END}")

async def search(url, path, extensions, statusCode):
    data = getWordlist(path)
    url = getUrl(url)
    urls = [url + endpoint + ext for endpoint in data for ext in extensions]
    urlsLength = len(urls)
    
    async with aiohttp.ClientSession() as session:
        tasks = [requestUrl(session, u, statusCode,i, urlsLength) for (i,u) in enumerate(urls)]
        await asyncio.gather(*tasks)
        
def run_search(url, path, extensions, statusCode):
    asyncio.run(search(url, path, extensions, statusCode))
    
def main(args):
    wordlists = args.wordlists
    enumType = None
    if args.wordlists == None:
        enumType = args.type
        if enumType == "all":
            wordlists = getConfigWordlists(getWordlistsJson(CONFIG_PATH))
        else:
            wordlists = [getWordlistsJson(CONFIG_PATH)["files"][enumType]]
            
    
    for w in wordlists:
        print("Enumerating " + w)
        run_search(args.url, w, args.extensions, args.status_codes)
    
            
if __name__ == "__main__":
    banner()
    config = getWordlistsJson("config.json")
    
    parser = argparse.ArgumentParser(description="Enum a webpage asynchronously with the different wordlists either entered or using the premade config files")
    parser.add_argument("url", help="Url to scan")
    parser.add_argument("-w", "--wordlists", nargs='+', help="You can enter one or several wordlists that will be used for the enumeration")
    parser.add_argument("-type", choices=["backup", "config", "hidden", "common", "all"], help="If no wordlists were entered, you could chose which type of file to search (backup, config, hidden, common, all) (default: all)", default="all")
    parser.add_argument("-x", "--extensions", help="The extensions that will be added to each endpoint of wordlist", nargs='+', default=[""])
    parser.add_argument("-sc", "--status-codes", help="The status codes that will be returned (default: 200)", default=[200], nargs='+')
    #parser.add_argument("-R", "--recursive", help="Search the page recursively", default=False, action='store_true')

    args = parser.parse_args()
    
    start = time.time()    
    
    main(args)



    #backup extension
    
    #config extension
    
    #type of search (backend, config, hidden, common, all) 
    
    #add extensions for common search
    
    #status code
    


    print("\nFinished in %ss" % (time.time() - start))


            