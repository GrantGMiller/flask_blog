from flask import Markup
from flask_dictabase import BaseTable


class Post(BaseTable):
    @property
    def url(self):
        return f'/post/{self["uuid"]}'

    @property
    def author(self):
        return 'Anonymous'

    @property
    def author_url(self):
        return '#'

    @property
    def body_markup(self):
        return Markup(self['body'])

    def ui_safe(self):
        ret = {}
        for key in ['uuid', 'public']:
            ret[key] = self.get(key, None)
        return ret
