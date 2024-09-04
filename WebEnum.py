import requests
import json
import argparse

RED = "\33[91m"
BLUE = "\33[94m"
GREEN = "\033[32m"
YELLOW = "\033[93m"
PURPLE = '\033[0;35m' 
CYAN = "\033[36m"
END = "\033[0m"

def banner():
    font = f"""
    {BLUE}
-------------------------------------------------------------------------------------------------------

oooooo   oooooo     oooo            .o8       oooooooooooo                                           
 `888.    `888.     .8'            "888       `888'     `8                                           
  `888.   .8888.   .8'    .ooooo.   888oooo.   888         ooo. .oo.   oooo  oooo  ooo. .oo.  .oo.   
   `888  .8'`888. .8'    d88' `88b  d88' `88b  888oooo8    `888P"Y88b  `888  `888  `888P"Y88bP"Y88b  
    `888.8'  `888.8'     888ooo888  888   888  888    "     888   888   888   888   888   888   888  
     `888'    `888'      888    .o  888   888  888       o  888   888   888   888   888   888   888  
      `8'      `8'       `Y8bod8P'  `Y8bod8P' o888ooooood8 o888o o888o  `V88V"V8P' o888o o888o o888o 
      
-------------------------------------------------------------------------------------------------------
                                                                                                                                                                                                                               
    {END}                                                                                                                                                                             
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
    try:
        with open(path, "r") as f:
            data = f.readlines()
    except:
        print("Error while opening the file: " + path)
        
    return data


def search(url, path):
    #perform url searching on backend files
    data = getWordlist(path)
    for endpoint in data:
        req = requests.get(url + endpoint)
        
        #check if request is valid
        if req.status_code == 200:
            print("[+] Found :" + url + endpoint)
            
if __name__ == "__main__":
    banner()
    config = getWordlistsJson("config.json")
    
    parser = argparse.ArgumentParser(description="Enum a webpage according to a config file")
    parser.add_argument("url", help="url to scan")
    parser.add_argument("type", help="which type of file to search (backup, config, hidden, common, all)")
    parser.add_argument("-x")
    parser.add_argument("-sc")

    #backup extension
    #config extension
    
    #type of search (backend, config, hidden, common, all) 
    
    #add extensions for common search
    
    #status code
    
    #perform the searching
    for key, path in config["files"].items():
        print(key, path)
        search("url", path)
            