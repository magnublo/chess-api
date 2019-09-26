from app.handlers import BaseHandler


class IndexHandler(BaseHandler):

    def get(self, key):
        self.render('index.html')