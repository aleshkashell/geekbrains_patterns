import asyncio
import jinja2
from store import Store


class Pagebuilder:
    html_path = 'wsgi/head.html'

    def __init__(self):
        self.template = self._load_template()
        self.types = {
            'users': self._body_users,
            'movies': self._body_movies
        }
        self.loop = asyncio.get_event_loop()
        self.store = Store()

    def _body_users(self):
        users = self.loop.run_until_complete(self.store.get_users())
        result = list()
        for user in users:
            result.append((user['username'], user['createdAt']))
        return result

    def _body_movies(self):
        movies = self.loop.run_until_complete(self.store.get_movies())
        result = list()
        for movie in movies:
            result.append((movie["title"], movie["createdAt"]))
        return result

    def _build_body(self, data_type):
        try:
            method = self.types[data_type]
        except KeyError:
            method = self._body_raw
        return method()

    def build(self, data_type):
        data = {
            "body": self._build_body(data_type),
            "Title": data_type
        }
        return self.template.render(**data)

    def _body_raw(self):
        return f'Incorrect type'

    def _load_template(self):
        template_loader = jinja2.FileSystemLoader(searchpath="./wsgi")
        template_env = jinja2.Environment(loader=template_loader)
        TEMPLATE_FILE = "head.html"
        return template_env.get_template(TEMPLATE_FILE)
