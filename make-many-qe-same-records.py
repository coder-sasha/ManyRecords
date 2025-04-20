"""
Dec 11 2024
Project ManyRecords
make-records.py 
The QnD script to write files, containning a big number of rows and 3 columns,
representing parameters of square equation.

This one make-many-same-records.py creates files populated by repetitive records, 
generated from the list qes (seee below)
Makes it easy to verify results.

"""

import time
import os
import datetime
import random

SML = "\U0001F600"
TUP = "\U0001F44D: "
OOO = "\U0001F631\t "

# initial equations
qes = ['1.0, -5.0, 6.0', 
    '2.0, -4.0, -6.00', 
    '3.00, 2.0, -8.00', 
    '-6990.52, 3908.31, 2086.26', 
    '-19.3, -5373.83, 9865.65'
]

# number of files
nfiles = 1
# default number of rows
rows = 1000
# created file name
fname = f"qe_data_{rows}_same.csv"
columns = 3
mode = 'w'
print(f"Creating CSV file(s), {columns} x {rows}...")

tr = 0
start = time.time()
try:
    with open(fname, mode) as fout:
        for r in range(rows+1):
            for q in qes:
                # random number of repetitions
                repeat = random.randint(1, 3)
                for r in range(repeat):
                    fout.write(f"{q}\n")            
                    tr += 1
                    
            if tr > rows:
                break
                
except Exception as exp:
   print(f"{OOO}Failed to complete generation of all {nfiles} files!\tError: {str(exp)}")
else:
    # display created file information
    s = os.stat(fname)
    info = {
        "File": fname,
        "Size (bytes)": s.st_size,
        "Created": datetime.datetime.fromtimestamp(s.st_ctime).strftime("%Y-%m-%d %H:%M"),
        "Permissions": oct(s.st_mode)[-3:]
    }

    print(f"Created {fname} in {time.time() - start:.3f}")
    print("\n".join(f"{key:15}: {value}" for key, value in info.items()))  
    print(SML)