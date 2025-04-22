# ManyRecords  
## C++ solution for the ManyRecords Quadrartic Equations

This is merely a storage folder, not a distribution.  

## Creating the data
Use `make-many-qe-records.py` or `make-many-qe-same-records.py` to generate CSV data file of any size.


## Build executable with provided CMake file  
mkdir build
cd build
cmake -DCMAKE_BUILD_TYPE=Release ..
cmake --build .

This creates the folder bin and build the executable  mr-qe-par  
All executables open the file qe_data_1000_same.csv and write into qe_data_1000_same_res.csv.  

## Have the data ready...  
ls -l
-rwxrwxr-x 1 ... 59240 Dec 26 17:49 mr-qe-par
-rw-rw-r-- 1 ... 21346 Dec 26 20:04 qe_data_1000_same.csv
-rw-rw-r-- 1 ... 51225 Dec 26 20:04 qe_data_1000_same_res.csv

## ... and run the programm  
./mr-qe-par
1008 equations. Reading time: 48us
Start solving...
CPU time: 531us
Savign Results
1008 saved. 2 without roots
ret=0   Total running time : 3ms





