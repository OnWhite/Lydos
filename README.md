# Lydos
A script making Rhea input files form your file explorer

### Idea
In order to use Rhea you need to multiplex your fastq files.
Rhea provides a perlscript with this capability for you, but it
needs a .tab file including the filenames needed 
to do so. This script automatizes the process of making this file.

### Usage
To use this script you need to enter

    - the filename of the .tab file 
    - from where automatically generated ids should start 
        NOTE: the ID value has to be a whole number,
                the first ID will have the number selected 
                the next IDs will ascend by one
    - whether you want a FilesNotMultiplexed.tab file, 
        it will list all the files and folders in your input folder that aren't in the outputfile 
    - where you want to save the file 
    - whether your data is paired or not, if so pairs need to have R1 and R2 in the filename,
        if not it needs to include R1 in the filenames 

then click the "Read Files" Button select the location of your fasta /fastq files

### Output
The Output will consist of your .tab file with the list of your filename pairs, and if selected so a file called FilesNotMultiplexed.tab.

### Defaultvalues
The defaultvalues are:

- filename:                 multiplexing_table.tab
- IDs:                      none
- FilesNotMultiplexed:      none
- Output Folder:            Input folder
- paired:                   no

### Furthure usage
In order to run the perlscript you need to move the multiplexing_table.tab to the dir in which the perlscript remultiplexor-paired.pl is located.
Note that there shouldn't be several multiplexing_table.tab files in the directory. Now just apply the perlscript according to it's  ReadMe.
