from pathlib import Path

class Images:
    '''
    class for iterating through the image data files
    '''
    def __init__(self):
        self._load()
        self.length = len(self.image_paths)
        self.index = 0

    def __len__(self):
        return self.length
    
    def next(self):
        if self.index == self.length:
            return False
        path = self.image_paths[self.index]
        self.index += 1
        return path

    def _load(self):
        base = Path('/usr/src/data/images')
        image_paths = base.glob('*')
        image_paths = [str(path) for path in image_paths]
        self.image_paths = sorted(image_paths)
        

if __name__ == "__main__":
    images = Images()
    print(images.next())