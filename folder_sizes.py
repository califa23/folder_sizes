import os
from glob import glob
import re

# https://note.nkmk.me/en/python-os-path-getsize/#:~:text=Use%20os.,in%20a%20directory%20(folder).&text=This%20function%20was%20added%20in,listdir()%20in%20earlier%20versions.
# function to get the size of a directory in bytes
def get_dir_size(path='.'):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total

# https://www.geeksforgeeks.org/python-program-to-sort-a-list-of-tuples-by-second-item/
# function to sort list of tuples by folder size(second value in tuple)
def Sort_Tuple(tup, sort):
    if sort == 'A':
        lst = len(tup)
        for i in range(0, lst):
            for j in range(0, lst-i-1):
                if (tup[j][1] > tup[j + 1][1]):
                    temp = tup[j]
                    tup[j]= tup[j + 1]
                    tup[j + 1]= temp
    else:
        lst = len(tup)
        for i in range(0, lst):
            for j in range(0, lst-i-1):
                if (tup[j][1] < tup[j + 1][1]):
                    temp = tup[j]
                    tup[j]= tup[j + 1]
                    tup[j + 1]= temp
    return tup

def convert_to_units(size, units):
    if units == 'GB':
        size = size/1000000000
    if units == 'MB':
        size = size/1000000
    if units == 'KB':
        size = size/1000
    return size

def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def main(path, sort, units, head, log, thresh):
    # set defaults
    if path == None:
        path = '.'
    if sort == None:
        sort = None
    if units == None:
        units = 'bytes'
    if(head == 'True' or head == 'true'):
        head = True
    else:
        head = False
    if(log == 'True' or log == 'true'):
        log = True
        result_log = open("results.txt", 'w')
    else:
        log = False

    if path == '.':
        print('Scanning all folders in current directory...')
    else:
        print('Scanning all folders in ' + path + '...')
    # define list to store folder names and sizes
    names_and_sizes = []
    
    # populate above list with tuples containing the folder name and the folder size
    location = glob(path+"\\*\\", recursive = True)
    for folder in location:
        splitted = folder.rstrip('\\').split('\\')
        name = splitted[len(splitted)-1]
        size = get_dir_size(folder)

        tu = (name,size)
        names_and_sizes.append(tu)


    # sort list by folder size
    if sort != None:
        names_and_sizes = Sort_Tuple(names_and_sizes, sort.upper())

    # display list of folders and sizes by size order
    count = 1
    for tup in names_and_sizes:
        if head == True and count == 10:
            break
        name = tup[0]
        size = tup[1]
        size = convert_to_units(size, units.upper()) # convert to units
        if thresh != None:
            if(int(size) < int(thresh)):
                continue
        size = round(size,2)   # round to 100s decimal place
        size = str(size) + ' ' + str(units.upper())
        print(f"{name : <40}{size : >40}")
        if log == True:
            result_log.write(f"{name : <40}{size : >40}")
            result_log.write('\n')
        count+=1
    
    if len(names_and_sizes) == 0:
        print('No folders found in directory or directory does not exist')

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='List all folders and their sizes in the given path')
    parser.add_argument('--path', metavar='path', required=False,
                        help='the path to desired folder to be read (Defaulted to current directory)')
    parser.add_argument('--sort', metavar='flag', required=False,
                        help='sort the display by folder size (A=Ascending, D=Descending) (Defaulted to Alphabetical)')
    parser.add_argument('--units', metavar='unit', required=False,
                        help='change units of memory displayed (GB, MB, or KB) (Defaulted to BYTES)')
    parser.add_argument('--head', metavar='boolean', required=False,
                        help='display top 10 folders in sort (True or False) (Defaulted to False)')
    parser.add_argument('--log', metavar='boolean', required=False,
                        help='log results to a text file called "results.txt" in directory of program (True or False) (Defaulted to False)')
    parser.add_argument('--thresh', metavar='int', required=False,
                        help='will only show folders with size above given threshold in units provided. If units is not set, the default will be BYTES')


    args = parser.parse_args()

    # safe input checks
    if args.sort != None and args.sort != 'a' and args.sort != 'A' and args.sort != 'd' and args.sort != 'D':
        print('ERROR: Bad input value for --sort. Use either A or D')
        quit()
    
    if args.units != None and args.units != 'gb' and args.units != 'GB' and args.units != 'mb' and args.units != 'MB' and args.units != 'kb' and args.units != 'KB' and args.units != 'bytes' and args.units != 'BYTES':
        print('ERROR: Bad input value for --units. Use either GB, MB, KB, or BYTES')
        quit()

    if args.head != None and args.head != 'true' and args.head != 'True' and args.head != 'false' and args.head != 'False':
        print('ERROR: Bad input value for --head. Use either True or False')
        quit()
    
    if args.log != None and args.log != 'true' and args.log != 'True' and args.log != 'false' and args.log != 'False':
        print('ERROR: Bad input value for --log. Use either True or False')
        quit()

    if(args.thresh != None and (isInt(str(args.thresh)) == False or  int(args.thresh) < 1)):
        print('ERROR: Bad input value for --thresh. Please use a non-zero positive integer')
        quit()


    main(path=args.path, sort=args.sort, units=args.units, head=args.head, log=args.log, thresh=args.thresh)
    