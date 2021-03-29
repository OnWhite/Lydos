import os
import sys
from tkinter.filedialog import askdirectory, Tk
import shutil
import tkinter as tk

import psutil as psutil
from fpdf import FPDF
import os
import sys
import psutil
import logging
from pygments import highlight
from kivy.lang import Builder

from kivymd.app import MDApp

from kivymd.uix.menu import MDDropdownMenu, RightContent




KV = '''
        

        

Screen:
        canvas.before:
                Color:
                        rgba:(27/255,27/255,46/255,255/255)
                Rectangle:
                        pos: self.pos
                        size: self.size
                    
        RelativeLayout:
                MDProgressBar:
                        orientation: "horizontal"
                        type: "determinate"
                        running_duration: 1
                        color: (93/255,160/255,161/255,255/255)
                        pos_hint: {'center_x': 0.5, 'center_y': 1}
                        size: self.size
                        value: app.getprogress()
                MDTextField:
                        id:name
                        hint_text: "Table Name"
                        pos_hint: {'center_x': 0.5, 'center_y': 0.9}
                        size_hint: 0.3, 0.1
                        
                        line_color_focus: (93/255,160/255,161/255,255/255)
                        color_mode: 'custom'
                        #mode:"rectangle"
                        current_hint_text_color:(93/255,160/255,161/255,255/255)
                        #line_color_normal:(93/255,160/255,161/255,255/255)
                
                CheckBox:
                        pos_hint: {'center_x': 0.365, 'center_y': 0.8}
                        on_active: app.setTrue()
                        #color: (93/255,160/255,161/255,255/255)
                        size_hint_x: .20
                Label:
                        pos_hint: {'center_x': 0.51, 'center_y': 0.8}
                        text: "IDs"
                        size_hint_x: .80
                        font_size:20
                MDIconButton:
                        id: button1
                        icon:'folder'
                        pos_hint: {'center_x': 0.365, 'center_y': 0.7}
                        text_color: (93/255,160/255,161/255,255/255)
                        theme_text_color: "Custom"
                        markup: False
                        on_release: app.setSaveplace()
                
                
                MDRaisedButton:
                        pos_hint: {'center_x': 0.412, 'center_y': 0.6}
                        id: auslesen
                        md_bg_color: (93/255,160/255,161/255,255/255)
                        theme_text_color: "Custom"
                        markup: False
                    
                        text: "Read Files"
                        pos: (200,200)
                    
                        on_release: app.auslesen()
                MDRaisedButton:
                        id: reset
                        pos_hint: {'center_x': 0.547, 'center_y': 0.6}
                        color: (154/255,84/255,93/255,200/255)
                        text: "ReadMe"
                        md_bg_color: (93/255,160/255,161/255,255/255)
                        theme_text_color: "Custom"
                        markup: True
                        on_release: app.runIt()
                        
        '''

class rheascript(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global IDs
        IDs=False
        global savefile
        savefile=""
        self.screen = Builder.load_string(KV)

    # Methode zum UI Fensterschließen

    def getprogress(self):
        global progress
        progress=20
        return progress
    # Fileexplorer
    def runIt(self):
        self.main()

    def browseFiles(self):

        Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        filename = askdirectory()  # show an "Open" dialog box and return the path to the selected file

        # globale Variable mit ausgeählter Datei
        global t
        t = filename
    def setTrue(self):
        global IDs
        IDs=True

    def Files(self):
        directories = os.listdir(t)

        # This would print all the files and directories
        my_file = open( self.screen.ids.name.text+".txt", "w+")
        my_file.write("SampleID\tR1IluminaOutput\tR2IluminaOutput\n")
        if directories.pop(0).__contains__("R1"):
            print("is your dir sorted")

        line = []

        for file in directories:
            for file2 in directories:
                if file.replace("R1","").replace("R2","")==file2.replace("R2","").replace("R1",""):
                    if file.__contains__("R1") and file2.__contains__("R2"):
                        line.append("\t"+file+"\t"+file2+"\t")
        if IDs==True:
            f=0
            for i in line:
                my_file.write(str(f) +i+"\n")
                print(len(line))
                f=f+1
        else:
            for i in line:
                my_file.write( i+"\n")
                print(len(line))
        my_file.close()
        if savefile=="":
            shutil.move("C:\\Users\\work\\PycharmProjects\\rheascript\\"+self.screen.ids.name.text+".txt", t.replace("/","\\"))
        else:
            shutil.move("C:\\Users\\work\\PycharmProjects\\rheascript\\"+self.screen.ids.name.text+".txt", savefile.replace("/","\\"))
        global progress
        progress = 100


    def build(self):
        return self.screen
    def Fehlermeldung(self):
        window = tk.Tk()
        window.title("Error")
        fehler = tk.Label(window)
        fehler.place(x=0, y=0)
        fehler.pack()
        window.mainloop()

    def einlesen(self):
        self.browseFiles()
    def setSaveplace(self):
        self.browseFiles()
        global savefile
        savefile=t

    def auslesen(self):
        self.browseFiles()
        self.Files()

    def syntax(self):
        os.system('start syntax.docx')


# main
# mainUi

if __name__ == '__main__':
    rheascript().run()
