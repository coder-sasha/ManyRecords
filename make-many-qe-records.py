"""
Dec 11 2024
Project ManyRecords 
make-many-records.py

The QnD script to write files, containning a big number (rows) of CS numbers (columns):
1,2,3 - parameters of square equation
"""

import time
import os
import datetime

import numpy as np
from tqdm import tqdm

# creation conditions
nfiles = 1
# number of rows
rows = 1_000_000
# file name
fname = f"qe_data_{rows}.csv"
# number of columns
columns = 3

nmil = int(rows / 100_000)
mode = 'w'

print("Create data file data_1000000_.csv populated with '1_000_000' x 3' random numbers from -1000.0 to 1000.0")
print("Just update the code if you want different dimensions.\n")
print(f"Creating CSV input {fname}, {columns} x {rows}...")

start = time.time()
try:
    for t in tqdm(range(1, nmil+1), desc=f"generating {rows} records CSV files"	, unit="file"):
        # get array populated  with random values
        nmbrs = np.random.uniform(-10000, 10000, (rows, columns))
        if t > 1:
            mode = 'a'
        with open(fname, mode) as fout:
            np.savetxt(fout, nmbrs, delimiter=',', fmt='%.2f')            
        
except Exception as exp:
   print(f"Failed to complete generation of all {nfiles} files!\tError: {str(exp)}")
else:
    s = os.stat(fname)
    info = {
        "File": fname,
        "Size (bytes)": s.st_size,
        "Created": datetime.datetime.fromtimestamp(s.st_ctime).strftime("%Y-%m-%d %H:%M"),
        "Permissions": oct(s.st_mode)[-3:]
    }

    print(f"Created {fname} in {time.time() - start:.3f}")
    print("\n".join(f"{key:15}: {value}" for key, value in info.items()))    
    print(':)')