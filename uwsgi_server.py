from wsgi.page_builder import Pagebuilder


class Application:
    def __init__(self):
        self.routes = {}
        self.page_builder = Pagebuilder()

    def __call__(self, environ, start_response, *args, **kwargs):
        print(environ)
        print(dir(environ))
        request = environ['PATH_INFO']
        data_type = self.routes.get(request, None)
        if data_type:
            start_response('200 OK', [('Content-Type', 'text/html')])
            return self.build_page(data_type)
        else:
            start_response('404 NOT FOUND', [('Content-Type', 'text/html')])
            return self.build_page(data_type)

    def add_route(self, route, name):
        self.routes[route] = name

    def build_page(self, data_type):
        str_data = self.page_builder.build(data_type)
        byte_data = list()
        print(str_data)
        for line in str_data:
            byte_data.append(line.encode('utf8') + b'\n')
        return byte_data


application = Application()

application.add_route('/movies', 'movies')
application.add_route('/users', 'users')
