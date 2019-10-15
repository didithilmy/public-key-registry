import http.server


class RequestHandler(http.server.BaseHTTPRequestHandler):
    def send(self, status_code, message):
        self.protocol_version = "HTTP/1.1"
        self.send_response(status_code)
        self.send_header("Content-Length", len(message))
        self.end_headers()
        self.wfile.write(bytes(message, "utf8"))

    def do_GET(self):
        message = "Hello!"
        print(self.path)
        self.send(200, "Hello!")
        return