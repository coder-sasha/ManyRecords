"""
Dec 20 2024
Project ManyRecords
mr-qe-use-csv.py 
This is using CSV module to read an equation from file and write results 
"""

import csv
import math
import time

# emoji constants
SML = "\U0001F600"      # smile
TUP = "\U0001F44D:\t"   # thumb up
OOO = "\U0001F631\t "   # o-oh face

data_name = 'qe_data_100_000_000_same.csv'
results_name = 'simple_res_100_000_000.csv'

# counters
tqe = 0     # number of quadratic equations
tle = 0     # number of linear equations
no_rts = 0  # number of equations with no roots

start = time.time()
total = 0
try:
    with open(data_name, 'r', newline='') as fin, open(results_name, 'w', newline='') as fout:
        reader = csv.reader(fin)
        writer = csv.writer(fout)
        # write the header of the resuls file
        writer.writerow(["a, b, c, root1, root2"])
        
        for row in reader:
            # row is expected to have exactly three members: pa,pb,pc
            try:
                pa, pb, pc = map(float, row)
            except ValueError:
                # if conversion fails skip and take next row
                continue

            r1, r2 = None, None
            total += 1
            if pa == 0:
                if pb != 0:
                    r1 = round(pc / pb, 3)
                    tle += 1
            else:
                tqe += 1
                a2 = pa * 2
                discr = pb * pb - 2 * a2 * pc
                if discr < 0:
                    no_rts += 1
                elif discr > 0:
                    sqrt_disc = math.sqrt(discr)
                    r1 = round((-pb + sqrt_disc) / a2, 3)
                    r2 = round((-pb - sqrt_disc) / a2, 3)
                else:
                    r1 = round(-pb / a2, 3)

            # write the result as a single formatted string in one column.
            writer.writerow([f"{row[0]}, {row[1]}, {row[2]}, {r1}, {r2}"])

except Exception as exp:
    print(f"{OOO}Failed to complete all equations from {data_name}! Error: {exp}")
else:
    run_time = time.time() - start
    print(f"{TUP}{total} records, {tqe} quadratic equations, {no_rts} without roots, {tle} linear equations\t time={run_time:.3f} sec\n{SML}")
