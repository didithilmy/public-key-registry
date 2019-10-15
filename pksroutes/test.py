import router
from router import Response

def testRoute(arg):
    return Response(responseBody="ID: " + arg['id'], headers={"Test": "Hello"})

router.get("/test/{id}", testRoute)