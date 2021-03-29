from pathlib import Path
import os
import shutil
from tkinter import Tk
from tkinter.filedialog import askdirectory
import xlrd
import csv
from pip._vendor.msgpack.fallback import xrange

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askdirectory() # show an "Open" dialog box and return the path to the selected file
print(filename)
"""
txt_folder = Path('C:/Users/work/OneDrive - Werner Heisenberg Gymnasium/Desktop/Seminararbeit files/SelectedData_Sophia_Fasta').rglob('*.fastq')
files=""
for x in txt_folder:
    files = files+""+ x+""
print(files)


"""
#!/usr/bin/python


# open the output csv

my_file = open("result.txt","w+")
my_file.write("SampleID\tR1IluminaOutput\tR2IluminaOutput")

original = r'C:\Users\work\PycharmProjects\rheascript\result.txt'
target = r'+path+'

shutil.move(original,target)
