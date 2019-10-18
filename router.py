import traceback
from routes import Mapper
from urllib.parse import urlparse, parse_qs

getMap = Mapper()
postMap = Mapper()
putMap = Mapper()
deleteMap = Mapper()

def executeController(map, requestHandler):
    try:
        parsedPath = urlparse(requestHandler.path)
        contentLength = int(requestHandler.headers.get('content-length', 0))

        body = requestHandler.rfile.read(contentLength).decode('utf-8')

        result = map.match(parsedPath.path)
        if (result == None):
            return None

        function = result['controller']

        request = Request(
            args = result,
            query = parse_qs(parsedPath.query),
            headers = requestHandler.headers,
            body = body
        )

        return function(request)
    except BaseException:
        print(traceback.format_exc())
        return Response(statusCode = 500, responseBody = "Internal Server Error")

def doGet(requestHandler):
    return executeController(getMap, requestHandler)

def doPost(requestHandler):
    return executeController(postMap, requestHandler)

def doPut(requestHandler):
    return executeController(putMap, requestHandler)

def doDelete(requestHandler):
    return executeController(deleteMap, requestHandler)

def registerRoute(map, routePath):
    def wrap(f):
        map.connect(routePath, controller=f)
        def wrapped_f(*args):
            f(*args)
        return wrapped_f
    return wrap

def get(routePath):
    return registerRoute(getMap, routePath)

def post(routePath):
    return registerRoute(postMap, routePath)

def put(routePath):
    return registerRoute(putMap, routePath)

def delete(routePath):
    return registerRoute(deleteMap, routePath)


class Request:
    def __init__(self, args = {}, query = {}, headers = None, body = None):
        self.args = args
        self.query= query
        self.headers = headers
        self.body = body

class Response:
    def __init__(self, statusCode = 200, responseBody = None, contentType = "text/plain", headers = {}):
        self.statusCode = statusCode
        self.responseBody = responseBody
        self.contentType = contentType
        self.headers = headers