from tkinter.filedialog import *
from PIL import Image, ImageTk
import ctypes.wintypes
from shutil import copyfile

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

        print(path.name)
        print(buf.value)

        #Permision denied vyskoci tu
        #copyfile(path.name, buf.value)

        return (tkimage, path.name)
    
