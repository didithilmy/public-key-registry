import http.server
import router
from router import Response

class RequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        result = router.doGet(self)
        return self.do_Request(result)

    def do_POST(self):
        result = router.doPost(self)
        return self.do_Request(result)

    def do_PUT(self):
        result = router.doPost(self)
        return self.do_Request(result)

    def do_DELETE(self):
        result = router.doDelete(self)
        return self.do_Request(result)

    def send(self, status_code = 200, message = None, headers = {}, content_type = "text/plain"):
        self.protocol_version = "HTTP/1.1"
        self.send_response(status_code)
        self.send_header("Content-Length", len(message))
        self.send_header("Content-Type", content_type)

        for header in headers.keys():
            self.send_header(header, headers[header])

        self.end_headers()
        self.wfile.write(bytes(message, "utf8"))

    def do_Request(self, result):
        if (result == None):
            self.send(404, "Not found")
            return

        if (not isinstance(result, Response)):
            self.send(404, "Not found")
            return

        self.send(status_code=result.statusCode,
                  message=result.responseBody,
                  headers=result.headers,
                  content_type=result.contentType)