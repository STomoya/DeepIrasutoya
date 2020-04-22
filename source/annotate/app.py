import os
import shutil
from pathlib import Path

from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
from flask import url_for

from images import Images

app = Flask(__name__)
images = Images()
total = str(len(images))

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

    current = str(images.index)

    return render_template('index.html', image_src=image_url, filename=filename, total=total, current=current)

@app.route('/annotate/<filename>', methods=['POST'])
def annotate(filename=None):
    cleaness = request.form['cleaness']
    gender = request.form['gender']
    what = request.form['what']
    negaposi = request.form['negaposi']
    
    with open('/usr/src/data/annotation.csv', 'a', encoding='utf-8') as fout:
        fout.write(','.join([filename, cleaness, gender, what, negaposi]) + '\n')

    return redirect('/')

@app.route('/skip/<filename>', methods=['POST'])
def skip(filename=None):
    with open('/usr/src/data/annotation.csv', 'a', encoding='utf-8') as fout:
        fout.write(','.join([filename, 'skipped']) + '\n')
    return redirect('/')

if __name__=='__main__':
    app.run(host='localhost', debug=True)
