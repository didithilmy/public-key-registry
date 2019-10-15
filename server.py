import os
import socketserver
import ssl

from request_handler import RequestHandler
import pksroutes.test

bindPort = int(os.getenv("PORT", 8080))
tlsEnabled = bool(os.getenv("TLS_ENABLED", False) == "true")
tlsCertPath = str(os.getenv("TLS_CERT_PATH"))
tlsKeyPath = str(os.getenv("TLS_KEY_PATH"))
Handler = RequestHandler

with socketserver.TCPServer(("", bindPort), Handler) as httpd:
    print("Serving at port", bindPort)
    if (tlsEnabled):
        httpd.socket = ssl.wrap_socket(httpd.socket,
            keyfile=tlsKeyPath,
            certfile=tlsCertPath, server_side=True)
    httpd.serve_forever()
