import os
import shutil
import datetime

from flask import Flask, render_template, redirect, request
from scraper import Scraper

app = Flask(__name__)
scraper = Scraper('https://www.irasutoya.com/search?updated-max=2020-03-12T13:00:00%2B09:00&max-results=10000')

@app.route('/')
def index():
    filename = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + '.png'
    url = scraper.save_image('/usr/src/source/scrape/static/images/'+filename)
    return render_template('index.html', filename=filename)

@app.route('/save', methods=['POST'])
def save():
    filename = scraper.current_filename
    shutil.move(filename, '/usr/src/data/images')
    scraper.next()
    return redirect('/')

@app.route('/skip', methods=['POST'])
def skip():
    os.remove(scraper.current_filename)
    scraper.next()
    return redirect('/')


if __name__=='__main__':
    app.run(host='localhost')