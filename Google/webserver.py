#!/usr/bin/env python
#coding=utf-8

import time
import BaseHTTPServer


PORT_NUMBER = 9000 # Maybe set this to 9000.


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    page = ""
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write(MyHandler.page)


def serve_page(html_src):
    MyHandler.page = html_src
    httpd = BaseHTTPServer.HTTPServer(("", PORT_NUMBER), MyHandler)
    print "Visit address http://127.0.0.1:9000 in your browser."
    try:
        httpd.serve_forever()
    except KeyboardInterupt:
        pass
    http.server_close()

if __name__ == "__main__":
    page = """
    <html><head><title>Title goes here.</title></head>
    <body><p>This is a test.</p>
    </body></html>
    """
    
    serve_page(page)
