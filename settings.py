import json
class LoadSettings:
    def __init__(self, configPath):
        self.configPath = configPath
        self.config = self.getConfigJson()
        
    def getConfigJson(self):
        data = ""
        try:
            with open(self.configPath, "r") as configFile:
                data = json.loads(configFile.read())
        except :
            print("Error while opening the config file: " + self.configPath)
            
        return data
    
    def getConfigWordlists(self, enumType):
        lst = [];
        if enumType == "all":
            for elt in self.config["wordlists"]:
                lst.append(self.config["wordlists"][elt])
        elif enumType in self.config["wordlists"]:
            for elt in self.config["wordlists"][enumType]:
                lst.append(elt)
        else:
            print(f"Settings \"{enumType}\" not in config file.")
        
        return lst # contains the path of all wordlists

    def getFileData(self, path):
        data = []
        try:
            with open(path, "r") as f:
                data = [line.strip() for line in f.readlines()]
        except:
            print("Error while opening the file: " + path)
            
        return data
    
    def getSettings(self, name):
        return self.config["settings"][name]
    
    def getHeaders(self, path):
        headers = {}
        with open(path, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                if ':' in line:
                    key, value = line.split(':', 1)
                    headers[key.strip()] = value.strip()
        return headers
    
    def getCookies(self, path):
        cookies = {}
        with open(path, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                if '=' in line:
                    key, value = line.split('=', 1)
                    cookies[key.strip()] = value.strip()
        return cookies