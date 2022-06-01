import brickschema
import os
import subprocess
import tempfile
from flask import Flask, request, flash, redirect, send_file
from io import BytesIO
import make223p
import makeBrick
from werkzeug.utils import secure_filename


app = Flask(__name__)
ALLOWED_EXTENSIONS = {'ttl'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/render/<std>', methods=["GET", "POST"])
def render_model(std):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            print("reading file")
            g = brickschema.Graph()
            g.parse(data=file.read(), format='turtle')
            print("rendering model...")
            if std == '223p':
                jscode = make223p.render_model(g)
            elif std == 'brick':
                jscode = makeBrick.render_model(g)
            with tempfile.NamedTemporaryFile(suffix='.js', dir=os.getcwd()) as f:
                f.write(jscode.encode('utf-8'))
                f.seek(0)
                res = subprocess.run(f"node {f.name}", shell=True, cwd=os.getcwd(), capture_output=True)
                svg_io = BytesIO()
                svg_io.write(res.stdout)
                svg_io.seek(0)
                return send_file(svg_io, mimetype='image/svg+xml')
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

if __name__ == "__main__":
    app.run("0.0.0.0")
