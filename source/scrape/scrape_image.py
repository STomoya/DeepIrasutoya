import time
from io import BytesIO
from pathlib import Path

import requests
from bs4 import BeautifulSoup
import lxml
from PIL import Image
from tqdm import tqdm

# creat dir for images
base = Path('/usr/src/data/images')
if not base.exists():
    base.mkdir()

# load dataset urls
'''
file format
    "id_0","url_0"
    "id_1","url_1"
    ...
'''
with open('/usr/src/data/urls_man.csv', 'r') as fin:
    data = fin.read()
lines = data.split('\n')
lines = [line.split(',') for line in lines]

# scrape images and save
for line in tqdm(lines):
    start = time.time()

    id = line[0]
    src = line[1]
    
    # scrape
    response = requests.get(src)
    image = Image.open(BytesIO(response.content))
    # crop image to square
    width, height = image.size
    if width <= height:
        cropped_image = image.crop((0, 0, width, width))
    else:
        cropped_image = image.crop((0, 0, height, height))
    # resize
    resized_image = cropped_image.resize((224, 224))
    # convert to RGB (JPEG)
    converted_image = resized_image.convert('RGB')
    
    converted_image.save('/usr/src/data/images/{}.jpg'.format(id))

    time.sleep(max(0, 1-(time.time()-start)))