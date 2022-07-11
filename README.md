# folder_sizes

## Overview
A small program that scans a directory and returns the sizes of each folder within that directory.

## Usage
    python folder_sizes.py -h
provides the list of options

    --sort flag     sort the display by folder size (A=Ascending,
                  D=Descending) (Defaulted to Alphabetical)
    --units unit    change units of memory displayed (GB, MB, or
                  KB) (Defaulted to BYTES)
    --head boolean  display top 10 folders in sort (True or False)
                  (Defaulted to False)
    --log boolean   log results to a text file called
                  "results.txt" in directory of program (True or
                  False) (Defaulted to False)
    --thresh int    will only show folders with size above given
                  threshold in units provided. If units is not
                  set, the default will be BYTES

### Ex:
    python folder_sizes.py --path C:\TestFolder --units gb --sort d