import os
from mimetypes import guess_type

from tornado.web import HTTPError

from app.handlers import BaseHandler
from definitions import ROOT_DIR


class ImageHandler(BaseHandler):

    def get(self):
        file_location = ROOT_DIR+str(self.request.path)
        if not os.path.isfile(file_location):
            raise HTTPError(status_code=404)
        content_type, _ = guess_type(file_location)
        self.add_header('Content-Type', content_type)
        with open(file_location, 'rb') as source_file:
            self.write(source_file.read())