from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

class webServerHandler(BaseHTTPRequestHandler):

    def hello_message(self, greeting):
        form = "<form method='POST' enctype='multipart/form-data' action='/hello'>\
                <h2>What would you like me to say?</h2>\
                <input name='message' type='text'>\
                <input type='submit' value='Submit'>\
                </form>"
        message = ""
        message += "<html><body style='color: red; font-size: 30px'>%s <a href='/hello'>Back To Hello!</a> %s </body></html>" % (greeting, form)
        return message
    
    def do_GET(self):
        self.send_response(200)         # Sends an HTTP OK status
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        if self.path.endswith("/hello"):    # Checks whether the request url pattern ends with /hello 
            # Starts sending the Http message body
            message = self.hello_message("Hello")
            self.wfile.write(message)
            print message
            return
        elif self.path.endswith("/ola"):
            message = self.hello_message("Ola")

            self.wfile.write(message)
            print message
            return
        else:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            self.send_response(301)
            self.end_headers()

            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')

            output = ""
            output += "<html><body>"
            output += " <h2> Okay, how about this: </h2>"
            output += "<h1> %s </h1>" % messagecontent[0]

            output += "<form method='POST' enctype='multipart/form-data' action='/hello'>\
                <h2>What would you like me to say?</h2>\
                <input name='message' type='text'\
                <input type='submit' value='Submit'>\
                </form>"
            output += "</body></html>"

            self.wfile.write(output)
            print output
        except:
            pass

def main():
    try:
        address = ("", 3004)
        server = HTTPServer(address, webServerHandler)
        print "Web server running on port %s" % address[1]
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()