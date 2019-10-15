import router


def testRoute(arg):
    return "ID: " + arg['id']

router.get("/test/{id}", testRoute)