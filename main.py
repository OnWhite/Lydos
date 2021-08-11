import pathlib
import shutil
import os
import sys
from tkinter.filedialog import askdirectory, Tk
from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp

# graphic String
KV = '''
Screen:
        canvas.before:
                Color:
                        #backgroundcolor
                        rgba:(27/255,27/255,46/255,255/255)
                Rectangle:
                        pos: self.pos
                        size: self.size
                    
        RelativeLayout:                       
                #textfield for filename 
                MDTextField:
                        id:name
                        hint_text: "Table Name"
                        pos_hint: {'center_x': 0.5, 'center_y': 0.9}
                        size_hint: 0.3, 0.1
                        
                        line_color_focus: (93/255,160/255,161/255,255/255)
                        color_mode: 'custom'
                        #mode:"rectangle"
                        current_hint_text_color:(93/255,160/255,161/255,255/255)          
                        

                #Textfiled for the starting ID
                MDTextField:
                        id:name2
                        hint_text: "ID starting number"
                        pos_hint: {'center_x': 0.5, 'center_y': 0.8}
                        size_hint: 0.3, 0.1
                        line_color_focus: (93/255,160/255,161/255,255/255)
                        color_mode: 'custom'
                        current_hint_text_color:(93/255,160/255,161/255,255/255)
                #checkbox whether files are paired 
                CheckBox:
                        pos_hint: {'center_x': 0.52, 'center_y': 0.6}
                        on_active: app.setTruepaired()
                        size_hint_x: .10
                        size: dp(48), dp(48)
                #label describing the paired checkbox
                Label:
                        pos_hint: {'center_x': 0.59, 'center_y':  0.6}
                        text: "paired"
                        size_hint_x: .80
                        font_size:20
                #checkbox for file listing not multiplexed files
                CheckBox:
                        pos_hint: {'center_x': 0.365, 'center_y': 0.7}
                        on_active: app.setTrueFilesNotMultiplexed()
                        #color: (93/255,160/255,161/255,255/255)
                        size_hint_x: .10
                        size: dp(48), dp(48)
               #label describing file listing not multiplexed files checkbox
                Label:
                        pos_hint: {'center_x': 0.51, 'center_y': 0.7}
                        text: "FilesNotMultiplexed"
                        size_hint_x: .80
                        font_size:20
                #folder to select the output place
                MDIconButton:
                        id: button1
                        icon:'folder'
                        pos_hint: {'center_x': 0.365, 'center_y': 0.6}
                        text_color: (93/255,160/255,161/255,255/255)
                        theme_text_color: "Custom"
                        markup: False
                        on_release: app.setSaveplace()
                
                #button starting the reading process of the selected folder
                MDRaisedButton:
                        pos_hint: {'center_x': 0.412, 'center_y': 0.5}
                        id: auslesen
                        md_bg_color: (93/255,160/255,161/255,255/255)
                        theme_text_color: "Custom"
                        markup: False
                        text: "Read Files"
                        pos: (200,200)
                        on_release: app.readout()
                #button to open the manual/description
                MDRaisedButton:
                        id: reset
                        pos_hint: {'center_x': 0.575, 'center_y': 0.5}
                        color: (154/255,84/255,93/255,200/255)
                        text: "Exit"
                        md_bg_color: (93/255,160/255,161/255,255/255)
                        theme_text_color: "Custom"
                        markup: True
                        on_release: app.exit()
                Label:
                        id: name_label
                        pos_hint: {'center_x': 0.5, 'center_y': 0.2}
                        text: ""
                        font_size: 16
                        
                        
        '''


class Lydos(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # setting global variables with default values
        global paired
        paired = False
        global FNMdat
        FNMdat = False
        global savefile
        savefile = ""
        # load the Kivy String to start the UI
        self.screen = Builder.load_string(KV)

    @staticmethod
    def browseFiles():
        # a method showing a file explorer window to select files
        # draw the explorer (tkinter)
        Tk().withdraw()
        # get the selected filename
        filename = askdirectory()
        # save it in a global variable
        global selectedfile
        selectedfile = filename

    @staticmethod
    def setTruepaired():
        # method showing which value the paired checkbox has
        # runs when the box in the UI is checked
        global paired
        if not paired:
            # when checkbox starts with an unchecked box set it as checked
            paired = True
        else:
            # checkbox starts with an checked box set it als unchecked
            paired = False

    @staticmethod
    def exit():
        # kill the Mainwindow
        sys.exit()

    @staticmethod
    def setTrueFilesNotMultiplexed():
        # method showing which value the FilesNotMultiplexed checkbox has
        # runs when the box in the UI is checked
        global FNMdat
        if not FNMdat:
            # when checkbox starts with an unchecked box set it as checked
            FNMdat = True
        else:
            # checkbox starts with an checked box set it als unchecked
            FNMdat = False

    def Files(self):
        # Method to make the .tab table for rhea
        if selectedfile != "":
            directories = os.listdir(selectedfile)
            # creating a .tab table with the selected name default is "samples-sequences"
            global fehlermeldung
            filename = self.screen.ids.name.text + ".tab"
            if len(str(filename).strip("/\\: * ?\"<>|")) != len(str(filename)):
                self.screen.ids.name_label.text = "Your Filename shouldn't contain  / \\ : * ? \" < > |"
                return ""
            # creating a .tab table with the selected name default is "samples-sequences"
            if self.screen.ids.name.text == "":
                filename = "multiplexing_table.tab"

            mainfile = open(filename, "w+")

            if not paired:
                # creating the first line following the rhea syntax
                mainfile.write("#Sample_ID\tR1-Ilumina-Output\n")

                line = []

                # running through the dir to find R1 and R2 pairs
                for file in directories:
                    if file.__contains__("R1"):
                        # add string line to list
                        line.append("\t" + file + "\t")
            else:
                # creating the first line following the rhea syntax
                mainfile.write("#Sample_ID\tR1-Ilumina-Output\tR2-Ilumina-Output\n")

                line = []

                # running through the dir to find R1 and R2 pairs
                for file in directories:
                    for file2 in directories:
                        # if the dat name exept the R1 or R2 are the same
                        if file.replace("R1", "").replace("R2", "") == file2.replace("R2", "").replace("R1", ""):
                            # if the two files are the of the same pair
                            if file.__contains__("R1") and file2.__contains__("R2"):
                                # add string line to list
                                line.append("\t" + file + "\t" + file2 + "\t")
            if FNMdat:
                # creating a file where all files that are not multiplexed are saved
                notinmainfilefile = open("FilesNotMultiplexed.tab", "w+")
                # iterating through the dir chosen
                for file in directories:
                    f = 0
                    # if filename is inside the list of paired files
                    for i in line:
                        if i.__contains__(file):
                            # set a bookmark
                            f = 1
                    if f == 0:
                        # if no bookmark found -> save in the filesNotMultiplexed.tab file
                        notinmainfilefile.write(file + "\n")
                notinmainfilefile.close()

            if self.screen.ids.name2.text != "":
                if not self.screen.ids.name2.text.isnumeric():
                    self.screen.ids.name_label.text = "Your ID is not a whole number"
                    return ""

                # if the user wants automated ids
                f = int(self.screen.ids.name2.text)
                # counter for the id indexes
                if len(line) < 2:
                    # Error
                    self.screen.ids.name_label.text = "There aren't enough R1/R2 (paired) files"
                    return ""

                for i in line:
                    mainfile.write(str(f) + i + "\n")
                    # writing in the .tab outputfile
                    f = f + 1

            else:
                if len(line) < 2:
                    # Error
                    self.screen.ids.name_label.text = "There aren't enough R1/R2 (paired) files"
                    return ""
                # without ids
                for i in line:
                    mainfile.write(i + "\n")
            # close files
            mainfile.close()

            if savefile == "":
                try:
                    # save mainfile and notinmainfilefile at the inputfiles' place
                    shutil.move(str(pathlib.Path("test.py").parent.absolute()) + "\\" + filename,
                                selectedfile.replace("/", "\\"))
                except IOError:
                    # Error
                    self.screen.ids.name_label.text = "The file " + filename + " already exists"
                    os.remove(filename)
                    return ""
                if FNMdat:
                    try:
                        shutil.move(str(pathlib.Path("test.py").parent.absolute()) + "\\FilesNotMultiplexed.tab",
                                    selectedfile.replace("/", "\\"))
                    except IOError:
                        # Error
                        self.screen.ids.name_label.text = "The file FilesNotMultiplexed.tab already exists"
                        os.remove("FilesNotMultiplexed.tab")
                        return ""
            else:
                try:
                    # save at the selected place
                    shutil.move(str(pathlib.Path("test.py").parent.absolute()) + "\\" + filename,
                                savefile.replace("/", "\\"))
                except IOError:
                    # Error
                    self.screen.ids.name_label.text = "The file " + filename + " already exists"
                    os.remove(filename)
                    return ""
                if FNMdat:
                    try:
                        shutil.move(str(pathlib.Path("test.py").parent.absolute()) +
                                    "\\FilesNotMultiplexed.tab",
                                    savefile.replace("/", "\\"))
                    except IOError:
                        # Error
                        self.screen.ids.name_label.text = "The file FilesNotMultiplexed.tab already exists"
                        os.remove("FilesNotMultiplexed.tab")
                        return ""
            self.screen.ids.name_label.text = "Your File(s) are ready"

            return ""

    def build(self):
        Window.size = (800, 500)
        Window.set_icon('archive-search-outline.png')
        self.icon = "archive-search-outline.png"
        return self.screen

    def setSaveplace(self):
        # method to set the place for the outputfile
        self.browseFiles()
        global savefile
        savefile = selectedfile

    def readout(self):
        # start browser/ main algorithm
        self.browseFiles()
        self.Files()


if __name__ == '__main__':
    Lydos().run()
