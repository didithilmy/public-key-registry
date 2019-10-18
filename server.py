import os, sys
import socketserver
import ssl

from request_handler import RequestHandler
from pksroutes import *

def main():
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

        try:
            httpd.serve_forever()
        except BaseException as e:
            print("Stop server. Error: ", e)
            httpd.server_close()
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)


if __name__ == '__main__':
    main()
