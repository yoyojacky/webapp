from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory
import os
from werkzeug.utils import secure_filename



UPLOAD_FOLDER = '/home/pi/webapp/uploads'
ALLOWED_EXTENSIONS = {'txt','pdf', 'jpg','md','png', 'jpeg', 'gif', 'zip', '7z','avi', 'mov', 'mv', 'wm', 'ogg', 'mp4', 'mp3'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.urandom(24)


def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')

def index():
    return render_template('index.html')

@app.route('/cakes')

def cakes():
    return render_template('cakes.html')

@app.route('/hello/<name>')

def hello(name):
    return render_template('page.html', name=name)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
    return render_template('upload.html')


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config['UPLOAD_FOLDER'], name)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
