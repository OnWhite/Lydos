import shutil
import tkinter as tk
import os
from tkinter.filedialog import askdirectory, Tk
from kivy.lang import Builder
from kivymd.app import MDApp

# graphic string
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
                #topprogressbar
                MDProgressBar:
                        orientation: "horizontal"
                        type: "determinate"
                        running_duration: 1
                        color: (93/255,160/255,161/255,255/255)
                        pos_hint: {'center_x': 0.5, 'center_y': 1}
                        size: self.size
                        value: app.getprogress()
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
                        
                # checkbox for automatised ids
                CheckBox:
                        pos_hint: {'center_x': 0.365, 'center_y': 0.8}
                        on_active: app.setTrue()
                        #color: (93/255,160/255,161/255,255/255)
                        size_hint_x: .20
               #label describing the ids checkbox
                Label:
                        pos_hint: {'center_x': 0.51, 'center_y': 0.8}
                        text: "IDs"
                        size_hint_x: .80
                        font_size:20
                #foleder to select the output place
                MDIconButton:
                        id: button1
                        icon:'folder'
                        pos_hint: {'center_x': 0.365, 'center_y': 0.7}
                        text_color: (93/255,160/255,161/255,255/255)
                        theme_text_color: "Custom"
                        markup: False
                        on_release: app.setSaveplace()
                
                #button starting the read process of the selected folder
                MDRaisedButton:
                        pos_hint: {'center_x': 0.412, 'center_y': 0.6}
                        id: auslesen
                        md_bg_color: (93/255,160/255,161/255,255/255)
                        theme_text_color: "Custom"
                        markup: False
                        text: "Read Files"
                        pos: (200,200)
                        on_release: app.auslesen()
                #button to open the manual/description
                MDRaisedButton:
                        id: reset
                        pos_hint: {'center_x': 0.547, 'center_y': 0.6}
                        color: (154/255,84/255,93/255,200/255)
                        text: "ReadMe"
                        md_bg_color: (93/255,160/255,161/255,255/255)
                        theme_text_color: "Custom"
                        markup: True
                        
                        
        '''

class rheascript(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # setting global variables with default values
        global IDs
        IDs=False
        global savefile
        savefile=""
        # load the Kivy String to start the UI
        self.screen = Builder.load_string(KV)



    def getprogress(self):
        # progressbar showing when the programm is finished
        global progress
        progress=20
        return progress



    def browseFiles(self):
        # a method showing a file explorer window to select files
        # draw the explorer (tkinter)
        Tk().withdraw()
        # get the selected filename
        filename = askdirectory()
        # save it in a global variable
        global selectedfile
        selectedfile = filename

    def setTrue(self):
        # method showing which value the IDs checkbox has
        # runs when the box in the UI is checked
        global IDs
        if IDs==False:
            # when checkbox starts with an unchecked box set it as checked
            IDs=True
        else:
            # checkbox starts with an checked box set it als unchecked
            IDs = False

    def Files(self):
        # Method to make the .tab table for rhea
        if selectedfile!= "":
            directories = os.listdir(selectedfile)
            # creating a .tab table with the selected name default is "samples-sequences"
            if self.screen.ids.name.text=="":
                mainfile = open("samples-sequences.tab", "w+")
            else:
                mainfile = open( self.screen.ids.name.text+".tab", "w+")

            # creating the first line following the rhea syntax
            mainfile.write("#Sample_ID\tR1-Ilumina-Output\tR2-Ilumina-Output\n")


            line = []

            #running through the dir to find R1 and R2 pairs
            for file in directories:
                for file2 in directories:
                    # if the dat name exept the R1 or R2 are the same
                    if file.replace("R1","").replace("R2","")==file2.replace("R2","").replace("R1",""):
                        # if the two files are the of the same pair
                        if file.__contains__("R1") and file2.__contains__("R2"):
                            # add string line to list
                            line.append("\t"+file+"\t"+file2+"\t")

            # creating a file where all files that are not multiplexed are saved
            notinmainfilefile = open("FilesNotMultiplexed.tab", "w+")
            # iterating through the dir chosen
            for file in directories:
                f=0
                # if filename is inside the list of paired files
                for i in line:
                    if i.__contains__(file):
                        # set a bookmark
                        f=1
                if f==0:
                    # if no bookmark found -> save in the filesNotMultiplexed.tab file
                    notinmainfilefile.write(file+"\n")


            if IDs==True:
                # if the user wants automated ids
                f=0
                # counter for the id indexes
                for i in line:
                    mainfile.write(str(f) +i+"\n")
                    # writing in the .tab outputfile
                    f=f+1

            else:
                # without ids
                for i in line:
                    mainfile.write( i+"\n")
            # close files
            mainfile.close()
            notinmainfilefile.close()

            if savefile=="":
                # save mainfile and notinmainfilefile at the inputfiles' place
                shutil.move("C:\\Users\\mitarbeiter\\PycharmProjects\\rheascript\\" + self.screen.ids.name.text +".tab", selectedfile.replace("/", "\\"))
                shutil.move("C:\\Users\\mitarbeiter\\PycharmProjects\\rheascript\\FilesNotMultiplexed.tab", selectedfile.replace("/", "\\"))
            else:
                # save at the selected place
                shutil.move("C:\\Users\\mitarbeiter\\PycharmProjects\\rheascript\\"+self.screen.ids.name.text+".tab", savefile.replace("/","\\"))
                shutil.move(
                    "C:\\Users\\mitarbeiter\\PycharmProjects\\rheascript\\FilesNotMultiplexed.tab",
                    savefile.replace("/","\\"))



    def build(self):
        return self.screen

    def Fehlermeldung(self):
        #never used
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
        savefile=selectedfile

    def auslesen(self):
        self.browseFiles()
        self.Files()




# main
# mainUi

if __name__ == '__main__':
    rheascript().run()
