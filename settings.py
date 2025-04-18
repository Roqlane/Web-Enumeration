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
        except FileNotFoundError as e:
            print(e)
        except json.JSONDecodeError as e:
            print(e)
        except Exception as e:
            print("Error while opening the config file: " + self.configPath + "\n" + e)
            
        return data
    
    def getConfigWordlists(self, enumType):
        lst = [];
        if enumType == "all":
            for elt in self.config["wordlists"]:
                lst.append(self.config["wordlists"][elt])
        elif enumType in self.config["wordlists"]:
            lst.append(self.config["wordlists"][enumType])
        else:
            print(f"Wordlist \"{enumType}\" not in config file.")
            exit()
        
        return lst # contains the path of all wordlists

    def getFileData(self, path):
        if path == "":
            return []
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
        try:
            with open(path, 'r') as file:
                for line in file:
                    line = line.strip()
                    if not line or ':' not in line:
                        continue
                    key, value = line.split(':', 1)
                    headers[key.strip()] = value.strip()
        except FileNotFoundError:
            print(f"Error: Headers file not found: {path}")
        except Exception as e:
            print("Error while opening the file: " + path)
        
        return headers
    
    def getCookies(self, path):
        cookies = {}
        try:
            with open(path, 'r') as file:
                for line in file:
                    line = line.strip()
                    if not line or '=' not in line:
                        continue
                    key, value = line.split('=', 1)
                    cookies[key.strip()] = value.strip()
        except FileNotFoundError:
            print(f"Error: Cookies file not found: {path}")
        except Exception as e:
            print("Error while opening the file: " + path)
        return cookies