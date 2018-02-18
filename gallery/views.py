import os

from flask import Blueprint, render_template, request, current_app
import simplejson
import json

from segmentation.dummy_segmentation import DummySegmentation
from .models import ImageObject


gallery = Blueprint('gallery', __name__, template_folder='templates', static_folder='static')


@gallery.route('/', methods=['GET', 'POST',])
def show_gallery():
    images = ImageObject.all(current_app.config['GALLERY_ROOT_DIR'])
    image_types = ["Image", "Segmented image", "Classified image"]
    return render_template('gallery.tmpl', images=images, image_types=image_types)


def get_new_name(filename, add):
    # todo change name to png
    name = filename.split(".")[:-1]
    name = ".".join(name)
    return "{}_{}.{}".format(name, add, filename.split(".")[-1])


@gallery.route('/upload', methods=['POST',])
def upload():
    if request.method == 'POST' and 'image' in request.files:
        image = request.files['image']
        root = current_app.config['GALLERY_ROOT_DIR']
        original_obj = ImageObject('', post=image, root=root)

        masks, segmented_image, segments_info = DummySegmentation().create_segmetns(image)
        # todo get augmentation of segmented_image

        seg_name = get_new_name(original_obj.filename, "seg")
        ImageObject.save_foto(original_obj.abspath, seg_name, original_obj)

        print("local", os.path.join(original_obj.localpath, seg_name), os.path.join(original_obj.localpath, original_obj.filename))

        result = {#'segmented': os.path.join(original_obj.localpath, seg_name),
                  'segmented': "/static/gallery/milashka_enot_1280x1024.jpg",
                  'original': os.path.join(original_obj.localpath, original_obj.filename),
                  'cell_n': segments_info['cell_n']}
        return json.dumps(result)
    return (simplejson.dumps({'error': 'you need to pass an image'}), 400)


@gallery.route('/image_<filename>', methods=['GET', 'POST',])
def show_image(filename):
    # image_ = request.args['image']  # counterpart for url_for()
    img = ImageObject(filename, root=current_app.config['GALLERY_ROOT_DIR']+"/"+".".join(filename.split(".")[:-1]))
    # messages = session['messages']       # counterpart for session
    # return ("ok, "'Hello {}, how are you?'.format(filename))
    return render_template("fotopage.tmpl", image=[img])
