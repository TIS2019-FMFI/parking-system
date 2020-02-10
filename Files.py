from tkinter.filedialog import *

class File:
    def choosePhoto():
        fileName = askopenfile()
        print(fileName)
        return fileName.name
    
