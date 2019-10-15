from routes import Mapper
getMap = Mapper()
postMap = Mapper()
putMap = Mapper()
deleteMap = Mapper()

def get(routePath, function):
    getMap.connect(routePath, controller=function)

def doGet(route):
    result = getMap.match(route)
    if (result == None):
        return None

    function = result['controller']

    return function(result)

class Response:
    def __init__(self, statusCode = 200, responseBody = None, headers = {}):
        self.statusCode = statusCode
        self.responseBody = responseBody
        self.headers = headers

    def getStatusCode(self):
        return self.statusCode

    def getResponseBody(self):
        return self.responseBody

    def getHeaders(self):
        return self.headers