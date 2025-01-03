import json
class LoadWordlists:
    def __init__(self, configPath):
        self.configPath = configPath
        
    def getWordlistsJson(self):
        data = ""
        try:
            with open(self.configPath, "r") as configFile:
                data = json.loads(configFile.read())
        except :
            print("Error while opening the config file: " + self.configPath)
            
        return data
    
    def getConfigWordlists(self, enumType):
        data = self.getWordlistsJson()
        lst = [];
        if enumType == "all":
            for elt in data["files"]:
                if elt == "custom" and data["files"]["custom"] != []:
                    for customElt in data["files"][elt]:
                        lst.append(customElt)
                else:
                    lst.append(data["files"][elt])
        elif enumType == "custom":
            for elt in data["files"]["custom"]:
                lst.append(elt)
        else:
            lst.append(data["files"][enumType])
        
        return lst # contains the path of all wordlists

    def getWordlist(self, path):
        data = []
        try:
            with open(path, "r") as f:
                data = f.readlines()
        except:
            print("Error while opening the file: " + path)
            
        return data
