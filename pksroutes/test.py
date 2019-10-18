import router
from router import Response


@router.get("/test/{id}")
def testRoute(request):
    return Response(responseBody="ID: " + request.args['id'], headers={"Test": "Hello"})

@router.post("/test/{id}")
def testPost(request):
    return Response(responseBody="ID: " + str(request.body), headers={"Test": "Hello"})
