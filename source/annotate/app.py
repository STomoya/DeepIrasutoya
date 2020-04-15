import os
import shutil
from pathlib import Path

from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for

from images import Images

app = Flask(__name__)
images = Images()

@app.route('/')
def index():
    # erase temporal image for visualization in browser
    tmp_imgs = Path('/usr/src/source/annotate/static/').glob('*')
    tmp_imgs = [str(path) for path in tmp_imgs]
    for path in tmp_imgs:
        os.remove(path)
    
    # copy next image to static folder
    image = images.next()
    filename = image.split('/')[-1]
    shutil.copy(image, '/usr/src/source/annotate/static/'+filename)
    image_url = url_for('static', filename=filename)

    return render_template('index.html', image_src=image_url)

@app.route('/annotate', methods=['POST'])
def annotate():
    return redirect('/')

@app.route('/skip', methods=['POST'])
def skip():
    return redirect('/')

if __name__=='__main__':
    app.run(host='localhost', debug=True)
