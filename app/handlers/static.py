import mimetypes
import os

from tornado.web import HTTPError

from app.handlers import BaseHandler
from definitions import ROOT_DIR

def guess_type(file_location):
    if file_location[-3:] == ".js":
        return "text/javascript", None
    else:
        return mimetypes.guess_type(file_location)

class StaticFileHandler(BaseHandler):

    def get(self, *args, **kwargs):
        file_location = ROOT_DIR+str(self.request.path)
        if not os.path.isfile(file_location):
            raise HTTPError(status_code=404)
        content_type, _ = guess_type(file_location)
        self.add_header('Content-Type', content_type)
        with open(file_location, 'rb') as source_file:
            self.write(source_file.read())