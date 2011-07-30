#!/usr/bin/env python
#coding=utf-8

import time
import BaseHTTPServer


PORT_NUMBER = 9000 # Maybe set this to 9000.


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    page = ""
    def do_GET(self):
        """Respond to a GET request."""
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(MyHandler.page)

class DataTableHandler(MyHandler):
    
    
    def do_GET(self):
        """Respond to a GET request."""
        path = self.path.lstrip('/')
        p_elements = path.split("?")
        cmd = p_elements[0]
        if cmd == '':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(self.page)
        elif cmd == 'search':
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            content = self.data_table.ToJSonResponse()
            self.wfile.write(content)
            
    
    

def serve_page(html_src):
    MyHandler.page = html_src
    httpd = BaseHTTPServer.HTTPServer(("", PORT_NUMBER), MyHandler)
    print "Visit address http://127.0.0.1:9000 in your browser."
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

if __name__ == "__main__":
    page = """
    <html><head><title>Title goes here.</title></head>
    <body><p>This is a test.</p>
    </body></html>
    """
    
    serve_page(page)
