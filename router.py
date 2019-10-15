from routes import Mapper
from urllib.parse import urlparse, parse_qs

getMap = Mapper()
postMap = Mapper()
putMap = Mapper()
deleteMap = Mapper()

def executeController(map, path):
    parsedPath = urlparse(path)

    result = map.match(parsedPath.path)
    if (result == None):
        return None

    function = result['controller']

    request = Request(
        args = result,
        query = parse_qs(parsedPath.query),
        data = {},
        rawData = None
    )

    return function(request)

def doGet(route):
    return executeController(getMap, route)

def doPost(route):
    return executeController(postMap, route)

def doPut(route):
    return executeController(putMap, route)

def doDelete(route):
    return executeController(deleteMap, route)

def get(routePath):
    def wrap(f):
        getMap.connect(routePath, controller=f)
        def wrapped_f(*args):
            f(*args)
        return wrapped_f
    return wrap

class Request:
    def __init__(self, args = {}, query = {}, data = {}, rawData = None):
        self.args = args
        self.query= query
        self.data = data
        self.rawData = rawData

class Response:
    def __init__(self, statusCode = 200, responseBody = None, contentType = "text/plain", headers = {}):
        self.statusCode = statusCode
        self.responseBody = responseBody
        self.contentType = contentType
        self.headers = headers