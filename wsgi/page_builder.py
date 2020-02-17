import asyncio
from store import Store


class Pagebuilder:
    html_path = 'wsgi/head.html'

    def __init__(self):
        self.types = {
            'users': self._body_users,
            'movies': self._body_movies
        }
        self.loop = asyncio.get_event_loop()
        self.store = Store()

    def _body_users(self):
        users = self.loop.run_until_complete(self.store.get_users())
        result = list()
        for i in users:
            pass

    def _body_movies(self):
        movies = self.loop.run_until_complete(self.store.get_movies())
        result = list()
        for movie in movies:
            result.append(f'<b>{movie["title"]:100}\t{movie["createdAt"]}</b>')
        return '\n'.join(result)

    def _build_header(self):
        with open(self.html_path) as f:
            return ''.join(f.readlines())

    def _build_body(self, data_type):
        try:
            method = self.types[data_type]
        except KeyError:
            method = self._body_raw
        return method()

    def build(self, data_type):
        data = list()
        data.append(self._build_header())
        data.append(self._build_body(data_type=data_type))
        data.append('</body>')
        data.append('</html>')
        return data

    def _body_raw(self):
        return f'Incorrect type'
