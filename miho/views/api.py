
from contextlib import closing
from functools import partial
import hashlib
import pathlib


from flask import Blueprint, jsonify, request
from werkzeug.datastructures import FileStorage
from PIL import Image
from PIL.ImageFile import ImageFile

from .. import utils

api = Blueprint('api', __name__)


@api.route('/')
def index():
    return jsonify()


@api.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return jsonify(error='nothing to upload'), 400

    images_dir = utils.get_images_dir()
    while True:
        tmp_file = '.' + utils.randstr(100)
        tmp_path = pathlib.Path(images_dir, tmp_file)
        if not tmp_path.exists():
            break

    image: FileStorage = request.files['image']
    digest = hashlib.sha256()
    with closing(image.stream) as fin, tmp_path.open('wb') as fout:
        for chunk in iter(partial(fin.read, 64 << 10), b''):
            digest.update(chunk)
            fout.write(chunk)

    file_hash = digest.hexdigest()

    img: ImageFile = Image.open(tmp_path)
    extension = {
        'jpeg': 'jpg',
        'jpg': 'jpg',
        'png': 'png',
        'gif': 'gif',
    }.get(img.format.lower(), None)

    if extension is None:
        tmp_path.unlink()
        return jsonify(error='unsupported format'), 400

    width, height = img.size
    sub_hash = file_hash[0:17]
    filename = f'{sub_hash}-{width}-{height}.{extension}'

    index = 0
    for im in utils.get_images():
        if im.filename == filename:
            tmp_path.unlink()
            img.close()
            return jsonify(error='file already exists', fn=im.fullname), 400
        index = max(index, im.index)

    index += 1

    new_filename = f'{index:06d}-{filename}'
    new_path = pathlib.Path(tmp_path.parent, new_filename)
    tmp_path.rename(new_path)

    thumb1_path = pathlib.Path(new_path.parent, 'thumbs', f'{index:06d}-1-{filename}.jpg')
    thumb2_path = pathlib.Path(new_path.parent, 'thumbs', f'{index:06d}-2-{filename}.jpg')

    t1 = img.convert('RGB')
    t1.thumbnail((512, 512), Image.BICUBIC)
    t1.save(str(thumb1_path), quality=85)
    t1.close()

    t2 = img.convert('RGB')
    t2.thumbnail((200, 200), Image.BICUBIC)
    t2.save(str(thumb2_path), quality=85)
    t2.close()

    return jsonify(success=f'images/{new_filename}')


@api.route('/delete/<fullname>', methods=['DELETE'])
def delete(fullname):
    images_dir = utils.get_images_dir()

    m = utils.match_image(fullname)
    img = utils.match_to_tuple(m)

    image_path = pathlib.Path(images_dir, img.fullname)
    preview_path = pathlib.Path(images_dir, 'thumbs', img.preview)
    thumbnail_path = pathlib.Path(images_dir, 'thumbs', img.thumbnail)

    if image_path.exists():
        image_path.unlink()
    if preview_path.exists():
        preview_path.unlink()
    if thumbnail_path.exists():
        thumbnail_path.unlink()

    return jsonify(success='file deleted')
