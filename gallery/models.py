"""
This module aims to create a model having the filesystem as backend, since
if someone don't want to add extra metadata more than the metadata given
by the file informations is useless to use a database.

TODO: traverse directory.
"""
import subprocess

from werkzeug import secure_filename
from werkzeug.datastructures import FileStorage

import os
import time
import fnmatch
import flask

from PIL import Image


class FilesystemObjectDoesNotExist(Exception):
    pass


class FilesystemObject(object):
    def __init__(self, filename, post=None, root=""):
        """Create an object from the information of the given filename or from a
        uploaded file.

        Example of usage:

            if request.method == 'POST' and 'photo' in request.POST:
                f = FilesystemObject('cats.png', request.POST['photo'])

        """
        self.root_dir = root
        self.filename = filename if filename else secure_filename(post.filename)
        self.abspath = ""
        # self.local_path = ""
        self.subdir = self.root_dir.split('/')[-1]
        if post:
            self.upload(post)

    def upload(self, post):
        """Get a POST file and save it to the settings.GALLERY_ROOT_DIR"""
        # TODO: handle filename conflicts
        directory = ".".join(self.filename.split(".")[:-1])

        self.abspath = os.path.join(self.root_dir, directory)
        self.localpath = os.path.join("/static/gallery", directory)
        if not os.path.exists(self.abspath):
            os.makedirs(self.abspath)
        print("save picture", os.path.join(self.abspath, self.filename))
        post.save(os.path.join(self.abspath, self.filename))

    @staticmethod
    def save_foto(directory, filename, image):

        # image.save(os.path.join(directory, filename))

        # resp = flask.make_response(open(os.path.join(image.abspath, image.filename)).read())
        # resp.content_type = "image/jpeg"
        # resp.save(os.path.join(directory, filename))
        #

        # new_image = FileStorage(stream=image.read(), filename=filename, #name=image.name,
        #                         content_type=image.content_type, content_length=image.content_length,
        #                         headers=image.headers)
        # new_image.save(os.path.join(directory, filename))
        # print("save_image", image, resp)

        # new_image = flask.make_response(image.read())
        # resp.content_type = "image/jpeg"

        im = Image.open((os.path.join(image.abspath, image.filename)))
        im.save(os.path.join(directory, ''.join(filename.split('.')[:-1])+'.png'))

    @staticmethod
    def get_information(root):
        for dirpath, dirnames, filenames in os.walk(root):
            # name = os.path.split(dirpath)[1]
            if dirpath == root:
                continue
            stat = os.stat(os.path.normpath(dirpath))
            yield stat.st_ctime, dirpath  # Yield directory

            # subprocess.check_output(['ls', '-l', '../static/gallery'])
            # b'total 0\n-rw-r--r--  1 memyself  staff  0 Mar 14 11:04 files\n'

    @classmethod
    def all(cls, root):
        """Return a list of files contained in the directory pointed by settings.GALLERY_ROOT_DIR.
        """

        directories = sorted(FilesystemObject.get_information(root), key=lambda x: x[0], reverse=True)
        directories = [d[1] for d in directories]
        files = [[(f, d) for f in os.listdir(d)] for d in directories]
        return [[cls(f, root=d) for f, d in file_list] for file_list in files]



class ImageObject(FilesystemObject):
    pass

