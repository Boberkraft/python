from flask import Flask, request, render_template, send_file
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from PIL import Image, ImageOps
from io import BytesIO
import os
import uuid

from database import Database
from user import User

app = Flask(__name__, static_folder='files', static_url_path='')
CORS(app)
ALLOWED_EXTENSION = set('text pdf png jpg jpeg gif'.split())
ALLOWED_MODE = ('selected', 'database')
ALLOWED_ACTION = ('add', 'select', 'delete', 'unselect')
UPLOAD_FOLDER = 'uploads/'
IMAGE_SIZE_QUALITY = 2
###
qlty = IMAGE_SIZE_QUALITY

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION

@app.route('/upload_files/', methods=['GET', 'POST'])
def upload_files():
    files_added = []
    images = []
    added = []
    if request.method == 'POST':
        if 'file' not in request.files:
            pass
        files = request.files.getlist('files[]')
        for file in files:
            if file.filename == '':
                pass
            if file and allowed_file(file.filename):
                original_filename = secure_filename(file.filename)
                random_filename = str(uuid.uuid4()) + '.' + original_filename.split('.')[1]
                file.save(os.path.join('uploads', random_filename))
                files_added.append(random_filename)

                # prepere to select
                images.append(dict(name=random_filename, original_name=original_filename, file=random_filename))
    ids = User.upload(images)
    for i in range(len(files_added)):
        added.append([ids[i], files_added[i], []])
    return {'how_many': len(added), 'data': render_template('card.html', files=added, static='/uploads/')}


def generate_thumb(path):
    image = Image.open(path)
    image.thumbnail((400*qlty, 300*qlty))
    return image

@app.route('/change_state/', methods=['GET', 'POST'])
def change():
    # msg = { 'mode': 'xx',
    #         'status': 'xx',
    #         xx}
    msg = request.json
    print('New Change state:', msg)
    if msg:
        mode, action = msg['mode'], msg['action']
        if mode not in ALLOWED_MODE or action not in ALLOWED_ACTION:
            raise ValueError('Not allowed mode or action!')
        if mode == 'selected':
            if action == 'select':
                User.select(msg['id'])
            elif action == 'unselect':
                User.unselect(msg['id'])
            elif action == 'add':
                User.add_uploaded(msg['id'], msg['tags'])
            elif action == 'delete':
                id = msg.get('id', None)
                User.delete(id)

        elif mode == 'database':
            if action == 'add':
                User.add_selected()
            if action == 'delete':
                User.delete_selected()
        else:
            print('Undefinied mode!')
        return str({'status': 'ok'})
    return str({'status': 'failed'})
@app.route('/view/')
def view_images():
    return 'wyswietlasz'

@app.route('/uploads/<path>')
def get_files(path):
    folder = os.path.dirname(os.path.abspath(__file__))
    up_folder = os.path.join(folder, 'uploads/')
    file_path = os.path.join(up_folder, secure_filename(path))
    image = generate_thumb(file_path)
    img_w, img_h = image.size
    background = Image.new('RGBA', (400*qlty, 300*qlty), (255,255,255,255))
    bg_w, bg_h = background.size
    offset = (bg_w - img_w)//2, (bg_h - img_h)//2
    background.paste(image, offset)
    fake_file = BytesIO()
    background.save(fake_file, 'PNG')
    fake_file.seek(0)
    return send_file(fake_file, mimetype='image/png')

@app.route('/add/')
def dodaj():

    images = User.get_uploaded()
    print('*'*10)
    [print(img.tags) for img in images]
    print('*' * 10)
    out = [[img.id, img.file, [tag.name for tag in img.tags]] for img in images]
    return render_template('add.html', files=out, static='/uploads/')

@app.route('/')
def main():

    images = User.get_images()
    print('*'*10)
    [print(img.name) for img in images]
    print('*' * 10)
    out = [[img.id, img.file,  [tag.name for tag in img.tags]] for img in images]
    return render_template('index.html', files=out, static='/uploads/')
app.run()



