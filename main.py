import sys
import os
import glob
import shutil
import PIL
from PIL import Image
import time
from flask import Flask, render_template, request, redirect, url_for
from flask import *
from flask import send_file, send_from_directory, safe_join, abort
from copy import copy
from main import app as Application
from werkzeug.utils import secure_filename
# from pytransform import pyarmor_runtime

app = Flask(__name__, template_folder='templates') 
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.jpeg']

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/', methods=['POST','GET'])
def root():
    return render_template('index.html')

@app.route('/upload', methods=['POST','GET'])
def upload():
    # if request.method == 'POST':
    # print('inside upload')
    uploaded_file = request.files['image']
    uploaded = uploaded_file.filename
    outputpath = os.path.join(app.root_path, 'output', 'image.png')
    inputpath = os.path.join(app.root_path, 'input', 'image.png')
    delete_path1 = os.path.join(app.root_path, "output")
    delete_path2 = os.path.join(app.root_path, "input")
    filename = "image"
    #start deletion
    if os.listdir(delete_path1) != 0:
        # print(os.listdir(delete_path1))
        for image in os.listdir(delete_path1):
            # if i.startswith('image'):  # not to remove other images
            if os.path.exists(image):
                os.remove(image)
    if os.listdir(delete_path2) != 0:
        # print(os.listdir(delete_path2))
        for image in os.listdir(delete_path2):
            # if i.startswith('image'):  # not to remove other images
            if os.path.exists(image):
                os.remove(image)
    #end deletion
    print('files deleted')
    if uploaded != '':
        file_ext = os.path.splitext(uploaded)[1]
        if file_ext not in current_app.config['UPLOAD_EXTENSIONS']:
            error = 'Invalid file extension, please upload again.'
            return render_template("index.html", error=error)
        else:
            os.chdir(delete_path2)
            filename = filename + file_ext
            uploaded_file.save(filename)
            #resize the image to pixel 375x812
            return redirect(url_for('frame'))
    else:
        error = 'No image uploaded, please try again.'
        return render_template("index.html", error=error)

@app.route('/frame', methods=['POST','GET'])
def frame():
    # os.system('python iPhoneFrame.py')
    os.chdir(app.root_path)
    import iPhoneFrame
    outputpath = os.path.join(app.root_path, 'output', 'image.png') 
    if os.path.exists(outputpath):
        print('exists')
        return render_template('frame.html')
    else:
        return redirect(url_for('upload'))


if __name__ == '__main__':
    app.run(debug=False, use_reloader=True)