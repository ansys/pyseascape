from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib import parse
hostName = "localhost"
serverPort = 0

class RHSC_MockServer(BaseHTTPRequestHandler):  
    def do_GET(self): 
        if self.path=="/kill":
            self.send_response(200)    
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html><head><title>https://testserver.com</title></head>", "utf-8"))
            self.wfile.write(bytes("<body><p>Server Closed successfully.</p></body>", "utf-8"))
            self.wfile.write(bytes("</html>", "utf-8"))
            self.server._BaseServer__shutdown_request = True
        elif self.path.startswith("None"):
            self.send_response(200)    
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(bytes('"null"', "utf-8"))
        else:
            self.send_response(200)    
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html><head><title>https://testserver.com</title></head>", "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8"))
            self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
            self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        pargs = parse.parse_qs(post_data)
        # post_args = dict([tuple(item.split('=')) for item in post_data.split('&')])
        cmd = pargs.get('command')[0] if pargs.get("command") else None
        # cmd = post_data
        if cmd.startswith("None"):
            self.send_response(200)    
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(bytes('"null"', "utf-8"))
        elif cmd.startswith('open_db'):
            db_path = cmd.split('(')[2].split(',')[0]
            self.send_response(200)    
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(f'"SeaScapeDB({db_path})"', "utf-8"))
        else:
            self.send_response(200)    
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(bytes("Please enter a valid command", "utf-8"))
            # self.wfile.write(bytes("<body>", "utf-8"))
            # self.wfile.write(bytes(f"<p>Request: {pargs=} \n {type(pargs)=}</p>", "utf-8"))
            # self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
            # self.wfile.write(bytes("</body></html>", "utf-8"))



if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), RHSC_MockServer)
    with open("port.out",'w') as f:
        f.write("Server started: http://%s:%s" % (hostName, webServer.server_port))
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        webServer.server_close()
        print("Server stopped.")