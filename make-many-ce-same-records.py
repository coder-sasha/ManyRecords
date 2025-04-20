"""
Dec 11 2024
Project ManyRecords: make-many-similar.py 
The QnD script to write files, containning a big number of rows and 3 columns.
Each row represents 3 parameters of a square equation: a,b,c
The file serves as input for performance testing programs in Python and C++.

This script creates files populated by repetitive records, generated from the list below.
Having many similar records makes it easy to verify results.
"""

import time
import os
from datetime import datetime
import random

# creation conditions
ces = ['2,-9,13,-6', 
       '1,-6,11,-6',
       '1,2,-1,-2', 
       '1,-4, 7, -4',
       '1,0,-2,4', 
       '1,2,3,4', 
       '0,2,-1,-2',
       '3,0,1,-2',       
       '1,0,3,1']

# number of files
nfiles = 1

# default number of rows
rows = 100_000_000

# created file name
fname = f'cubic_data_{rows}_same.csv'
columns = 4
mode = 'w'
print(f"Creating CSV file(s), {columns} x {rows}...")

tr = 0
start = time.time()
try:
    with open(fname, mode) as fout:
        fout.write('a,b,c,d')
        for r in range(rows+1):
            for q in ces:
                # random number of repetitions
                repeat = random.randint(1, 3)
                for r in range(repeat):
                    fout.write(f"{q}\n")            
                    tr += 1
                    
            if tr > rows:
                break
                
except Exception as exp:
   print(f"Failed to complete generation of all {nfiles} files!\tError: {str(exp)}")
else:
    # display created file information
    s = os.stat(fname)
    info = {
        "File": fname,
        "Size (bytes)": s.st_size,
        "Created": datetime.fromtimestamp(s.st_ctime).strftime("%Y-%m-%d %H:%M"),
        "Permissions": oct(s.st_mode)[-3:]
    }

    print(f"Created {fname} in {time.time() - start:.3f}")
    print("\n".join(f"{key:15}: {value}" for key, value in info.items()))  
    print('done\t:)')