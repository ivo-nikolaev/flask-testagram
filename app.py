from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os.path
from werkzeug.utils import secure_filename

app =  Flask(__name__)
app.secret_key = 'the lazy dog was riding a bike when it met a german photo instructor'
cwd = os.getcwd()


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/photo_upload')
def photo_upload():
    return render_template('photo_upload.html')

# UPLOADING PHOTOS
@app.route('/uploader', methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        # save file to folder
        f = request.files['file']
        f.save(cwd + "/static/user_photos/" + secure_filename(f.filename))
        flash(f.filename + " was uploaded succesfully")

        # make a record in the photos.json
        photos = {}

        if os.path.exists('photos.json'):
            with open('photos.json') as photos_file:
                photos = json.load(photos_file)

        name = secure_filename(f.filename)
        photos[name] = {'photo': name} 

        with open('photos.json', 'w') as photos_file:
            json.dump(photos, photos_file)
        
        return redirect(url_for('photo_upload'))


# Get a photo
@app.route('/photo/<string:code>')
def photo(code):
    return redirect(url_for('static', filename='/user_photos/' + code))


# A hardcoded link for the album
@app.route('/album/test_user')
def album():
    photos = {}
    with open('photos.json') as photos_file:
        photos = json.load(photos_file)
    return render_template('album.html', photos=photos)

# A DYNAMIN LINK FOR ALBUMS

# @app.route('/album/<string:code>')
# def get_album(code):
#     return null
