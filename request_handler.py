import http.server
import router
from router import Response


class RequestHandler(http.server.BaseHTTPRequestHandler):
    def send(self, status_code, message, headers = {}):
        self.protocol_version = "HTTP/1.1"
        self.send_response(status_code)
        self.send_header("Content-Length", len(message))

        for header in headers.keys():
            self.send_header(header, headers[header])

        self.end_headers()
        self.wfile.write(bytes(message, "utf8"))

    def do_GET(self):
        result = router.doGet(self.path)
        if(result == None):
            self.send(404, "Not found")
            return

        if (not isinstance(result, Response)):
            self.send(404, "Not found")
            return

        self.send(result.getStatusCode(), result.getResponseBody(), result.getHeaders())
        return