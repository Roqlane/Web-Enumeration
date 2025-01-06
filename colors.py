RED = "\33[91m"
BLUE = "\33[94m"
GREEN = "\033[32m"
YELLOW = "\033[93m"
PURPLE = '\033[0;35m' 
CYAN = "\033[36m"
END = "\033[0m"

def getColor(code):
    color = CYAN
    if code < 500:
        color = RED
    if code < 400:
        color = BLUE
    if code < 300:
        color = GREEN
    if code < 200:
        color = PURPLE
        
    return color