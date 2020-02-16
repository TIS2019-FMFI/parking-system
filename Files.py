from tkinter.filedialog import *
from PIL import Image, ImageTk
from shutil import copyfile
import ctypes.wintypes
import datetime
import pathlib


CSIDL_PERSONAL= 5       # My Documents
SHGFP_TYPE_CURRENT= 0

class File:
    def __init__(self):
        pass
    
    def choosePhoto(self, ecv):
        path = askopenfile(filetypes=[("Image File",'.jpg')])
        im = Image.open(path.name)
        print(im.size)
        im = im.resize(self.getNewSize(im), Image.ANTIALIAS)
        tkimage = ImageTk.PhotoImage(im)
        
        buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
        ctypes.windll.shell32.SHGetFolderPathW(0, CSIDL_PERSONAL, 0, SHGFP_TYPE_CURRENT, buf)

        time = self.getTimeInString()
        #time = time.replace('-', '.').replace(':', '.')
        #time = time.replace(':', '.')
        name = "{0} {1}".format(time, ecv)
        newPath = buf.value + '\\Parkovanie\\photos\\' + name + '.jpg'

        # Skusi prekopirovat fotku. Ak vyhodi chybu, tak najprv pozadovany priecinok vytvori
        # A potom skusi znova nakopirovat
        try:
            copyfile(path.name, newPath)
        except:
            pathlib.Path(buf.value + "\\Parkovanie\\photos\\").mkdir(parents=True, exist_ok=True)
            copyfile(path.name, newPath)

        return (tkimage, newPath)

    def deletePhoto(self, name):
        if pathlib.Path(name).exists():
            pathlib.Path(name).unlink()
    
    def getTimeInString(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S").replace(':', '.')

    def getNewSize(self, image):
        width, height = image.size

        # Cheme, aby vyska obrazka bola vzdy okolo 100px
        factor = height // 100
        new_width = round(width / factor)
        new_height = round(height / factor)

        return (new_width, new_height)
        

    
