from tkinter.filedialog import *
from PIL import Image, ImageTk
import ctypes.wintypes
from shutil import copyfile
import datetime

CSIDL_PERSONAL= 5       # My Documents
SHGFP_TYPE_CURRENT= 0

class File:
    def choosePhoto():
        path = askopenfile(filetypes=[("Image File",'.jpg')])
        im = Image.open(path.name)
        im = im.resize((150, 100), Image.ANTIALIAS)
        tkimage = ImageTk.PhotoImage(im)
        
        buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
        ctypes.windll.shell32.SHGetFolderPathW(0, CSIDL_PERSONAL, 0, SHGFP_TYPE_CURRENT, buf)

        name = str(datetime.datetime.now())[:-7]
        name = name.replace('-', '.')
        name = name.replace(':', '.')
        newPath = buf.value + '\\Parkovanie\\photos\\' + name + '.jpg'
        copyfile(path.name, newPath)

        return (tkimage, newPath)
    
def getTime():
    return datetime.datetime.now()
    
