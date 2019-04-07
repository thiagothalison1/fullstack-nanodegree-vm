from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import database
import urlparse

class webServerHandler(BaseHTTPRequestHandler):
    HTML_TEMPLATE = "<html><head></head><body>%s</body></html>"
    RESTAURANT_LIST_ITEM_TEMPLATE = "<li>%s<p><a href='/restaurants/edit/%d'>Edit<a/></p><p><a href='/restaurants/delete/%d'>Delete<a/></p></li><br>"
    CREATE_RESTAURANT_TEMPLATE = "<form method='POST' enctype='multipart/form-data'>\
        <h2>Make a new Restaurant</h2>\
        <input name='newRestaurant' type='text'>\
        <input type='submit' value='Create'>\
        </form>"
    EDIT_RESTAURANT_TEMPLATE = "<form method='POST' enctype='multipart/form-data'>\
        <h2>Edit an existing Restaurant</h2>\
        <input name='newRestaurantName' type='text'>\
        <input name='restaurantId' type='hidden' value='%s'>\
        <input type='submit' value='Edit'>\
        </form>"
    REMOVE_RESTAURANT_TEMPLATE = "<form method='POST' enctype='multipart/form-data'>\
        <h2>Are you sure you want to delete a restaurant:</h2>\
        <input name='restaurantId' type='hidden' value='%s'>\
        <input name='delete' type='submit' value='Delete'>\
        <input name='cancel' type='submit' value='Cancel'>\
        </form>"

    def send_success_message(self, message):
        self.send_response(200)         # Sends an HTTP OK status
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        response = self.HTML_TEMPLATE % message
        self.wfile.write(response)

    def handle_restaurants(self):
        restaurants = database.get_restaurants()
        restaurantsHtml = lambda restaurant : self.RESTAURANT_LIST_ITEM_TEMPLATE % (restaurant.name, restaurant.id, restaurant.id)
        restaurantsList = "<h1><a href='/restaurants/new'>Make a new restaurant here!</a></h1><ul>%s</ul>" % "".join(map(restaurantsHtml, restaurants))
        self.send_success_message(restaurantsList)

    def handle_restaurants_new_get(self):
        self.send_success_message(self.CREATE_RESTAURANT_TEMPLATE)

    def handle_restaurants_new_post(self):
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        if ctype == 'multipart/form-data':
            fields = cgi.parse_multipart(self.rfile, pdict)
            new_restaurant_name = fields.get('newRestaurant')
            database.create_restaurant(new_restaurant_name[0])

        self.send_response(302)
        self.send_header('Location', "/restaurants")
        self.end_headers()

    def handle_restaurants_edit_get(self):
        restaurant_id = self.path.split('/')[-1]
        edit_restaurant_page = self.EDIT_RESTAURANT_TEMPLATE % restaurant_id
        self.send_success_message(edit_restaurant_page)

    def handle_restaurants_edit_post(self):
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        if ctype == 'multipart/form-data':
            fields = cgi.parse_multipart(self.rfile, pdict)
            new_restaurant_name = fields.get('newRestaurantName')
            restaurant_id = fields.get('restaurantId')
            database.edit_restaurant(restaurant_id[0], new_restaurant_name[0])

        self.send_response(302)
        self.send_header('Location', "/restaurants")
        self.end_headers()

    def handle_restaurants_delete_get(self):
        restaurant_id = self.path.split('/')[-1]
        remove_restaurant_page = self.REMOVE_RESTAURANT_TEMPLATE % restaurant_id
        self.send_success_message(remove_restaurant_page)

    def handle_restaurants_delete_post(self):
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        if ctype == 'multipart/form-data':
            fields = cgi.parse_multipart(self.rfile, pdict)
            if 'delete' in fields:
                restaurant_id = fields.get('restaurantId')
                database.delete_restaurant(restaurant_id[0])

        self.send_response(302)
        self.send_header('Location', "/restaurants")
        self.end_headers()

    def do_GET(self):
        api = {
            '/restaurants': self.handle_restaurants,
            '/restaurants/new': self.handle_restaurants_new_get,
            '/restaurants/edit': self.handle_restaurants_edit_get,
            '/restaurants/delete': self.handle_restaurants_delete_get
        }

        apiMatch = [value for key, value in api.iteritems() if key in self.path]

        print apiMatch

        if len(apiMatch) > 0:
            apiMatch[len(apiMatch) - 1]()
        else:
            self.send_error(404, 'File Not Found: %s' % self.path)
        return

    def do_POST(self):
        api = {
            '/restaurants/new': self.handle_restaurants_new_post,
            '/restaurants/edit': self.handle_restaurants_edit_post,
            '/restaurants/delete': self.handle_restaurants_delete_post
        }

        apiMatch = [value for key, value in api.iteritems() if key in self.path]

        if len(apiMatch) > 0:
            apiMatch[len(apiMatch) - 1]()
        else:
            self.send_error(404, 'File Not Found: %s' % self.path)
        return

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