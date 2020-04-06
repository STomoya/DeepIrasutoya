
import time
from io import BytesIO

import requests
from bs4 import BeautifulSoup
import lxml
from PIL import Image

class Scraper():
    def __init__(self, first_url, min_interval=1.):
        self.next_page = None         # next page
        self.entry_urls = []          # list of urls of entries in each page
        self.entry_index = 0          # index of current entry
        self.image_urls = []          # list of urls of images in each entry
        self.image_index = 0          # index of current image

        self.current_filename = None  # most recent save image filename

        self.interval = min_interval  # minimun interval for waiting
        self.last_get = time.time()   # latest get called time

        # initual run
        page_soup = self.get(first_url)
        self.find_next(page_soup)
        self.find_entries(page_soup)
        entry_soup = self.get(self.entry_urls[self.entry_index])
        self.find_images(entry_soup)

    def wait(needs_wait):
        def inner(self, *args, **kwargs):
            wait_time = self.interval - (time.time() - self.last_get)
            time.sleep(max(0., wait_time))
            ret = needs_wait(self, *args, **kwargs)
            self.last_get = time.time()
            # print(wait_time)
            return ret
        return inner
    
    @wait
    def get(self, url):
        '''
        request url and convert to soup
        '''
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        return soup

    def find_entries(self, page_soup):
        '''
        find entries for page
        '''
        entries = page_soup.find_all(name='div', class_='boxim')
        self.entry_urls = [entry.find('a')['href'] for entry in entries]

    def find_images(self, entry_soup):
        '''
        find images from entry
        '''
        images = entry_soup.find(name='div', class_='entry').find_all('img', class_=None)
        temp_urls = [image['src'] for image in images]
        self.image_urls = [url if 'https:' in url else 'https:' + url for url in temp_urls]

    def find_next(self, page_soup):
        '''
        find next url from page
        '''
        self.next_page = page_soup.find('a', class_='blog-pager-older-link')
        if self.next_page:
            self.next_page = self.next_page['href']

    @wait
    def save_image(self, filename, image_url=None):
        '''
        save image
        '''
        if image_url == None:
            url = self.image_urls[self.image_index]
        else:
            url = image_url
        response = requests.get(url)
        image = Image.open(BytesIO(response.content))
        image.save(filename)
        self.current_filename = filename

        return url

    def next(self):
        '''
        scrape images one by one
        '''
        self.image_index += 1
        if self.image_index >= len(self.image_urls):    # when we reach the final image
            self.image_index = 0                        # init image index
            self.entry_index += 1                       # look at next entry
            if self.entry_index >= len(self.entry_urls):    # when we reach the final entry
                self.entry_index = 0                        # init entry index
                if self.next_page == None:                      # when we reach the end
                    print('we have reached the end')
                    return False
                page_soup = self.get(self.next_page)
                self.find_entries(page_soup)                # update entry list
                print('looking at ', self.next_page)
                print(self.current_filename)
                self.find_next(page_soup)
            entry_soup = self.get(self.entry_urls[self.entry_index])
            self.find_images(entry_soup)                # update image list
        
        return True
        
if __name__=='__main__':
    
    scraper = Scraper('https://www.irasutoya.com/search?updated-max=2015-04-15T15:00:00%2B09:00&max-results=10000&start=14962&by-date=false')

    save_dir = '/usr/src/data/images/'

    id = 20310

    while True:
        try:
            filename = save_dir + str(id).zfill(8) + '.png'
            url = scraper.save_image(filename)
            next_image = scraper.next()

            with open('/usr/src/data/url_filename.csv', 'a', encoding='utf-8') as fout:
                fout.write(','.join([filename, url]) + '\n')

            id += 1
        except Exception as e:
            print(e)
            next_image = scraper.next()

        if not next_image:
            break

            
        