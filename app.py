import brickschema
import os
import subprocess
import tempfile
from flask import Flask, request, flash, redirect, send_file
from io import BytesIO
import make223p
import makeBrick


app = Flask(__name__)
ALLOWED_EXTENSIONS = {'ttl'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return '''
    <!doctype html>
    <title>RDF-ELK Model Renderer</title>
    <h1>RDF-elK Model Renderer</h1>
    <p>
    This site generates SVG diagrams for 223P and Brick ontology models.
    </p>
    <p>
      <ul>
      <li><a href="/render/brick">Brick</a></li>
      <li><a href="/render/223p">223P</a></li>
      </ul>
    </p>
    <p>
    Steps:
    <ol>
        <li>Navigate to the <a href="/render/brick">Brick</a> or <a href="/render/223p">223P</a> page.</li>
        <li>Upload a model file</li>
        <li>Wait 1-2 minutes for the diagram to be generated</li>
        <li>Save the diagram to yoru computer</li>
    </ol>
    </p>
    '''


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
            else:
                return "Unknown metadata standard"
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
