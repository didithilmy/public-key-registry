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