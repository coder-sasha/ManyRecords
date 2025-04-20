# ManyRecords
(develop an acceptable solution for a file containing many quadratic equation records)

## Python solutions for the problem similar to 1BR

This project is inspired by Gunnar Morling's work 1BRC:  
- https://www.morling.dev/blog/one-billion-row-challenge
- https://github.com/gunnarmorling/1brc  

as well as some problems that I had to solve in the line of my own work.  
However, it is not a canonical 1BCR implementation.  
I was more interested in finding an acceptable solution for:  
1) solving quadratic equations;  
3) solving cubical equations;  
2) executing some OHLCV related calculations, like VWAP or moving averages;  

Mind that at the moment it is merely a storage of scripts, not ready for a distribution project.  
There is ManyRecordsExplanation.pdf, telling all about the data, scripts and performance results.
The folder QE is for Quadratic Equations.  
The folder CE ofr Cubical Equations.  

## Creating the data
Begin by installing the requirements:
```
python3 -m pip install -r requirements.txt
```
There are two QnD scripts that help quickly create necessary data files: `make-many-qe-records.py` and `make-many-qe-same-records.py`
```
> python3 make-many-qe-records.py
Create data file data_1000000_.csv populated with '1_000_000' x 3' random numbers from -1000.0 to 1000.0
Just update the code if you want different dimensions...

Creating CSV input data_1000000.csv, 3 x 1000000...
generating 1000000 records CSV files: 100%|██████████████████████████████████████████| 10/10 [00:13<00:00,  1.38s/file]
Created data_1000000.csv in 13.858
File           : data_1000000.csv
Size (bytes)   : 261671487
Created        : 2024-17-23 16:11
Permissions    : 666
:)

> python make-many-qe-same-records.py
Creating CSV file(s), 3 x 1000...
Created data_1000_same.csv in 0.001
File           : data_1000_same.csv
Size (bytes)   : 21342
Created        : 2024-17-23 16:21
Permissions    : 666
:)
```

## Running scripts
There are several scripts that demonstrates usage of different instruments for solving quadratic equations (QE-):
1) mr-qe-use-csv.py - simple 'pythonic' code for solving quadratic equations, using CSV module for reading and writing;
2) mr-qe-pandas.py - using Pandas DataFrame for reading and storing data; 
3) mr-qe-polars.py - using Polars DataFrame for reading and storing data;

All scripts open the file qe_data_<number_of_records>_same.csv and write into qe_results.csv file.  

