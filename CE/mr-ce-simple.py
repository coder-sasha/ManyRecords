"""
Dec 23 2024
ManyRecords
The simple cubic equation solver

Samples, 3 roots:
2,-9,13,-6 => 1,3/2,2
1,-6,11,-6 => 1,2,3
1,2,-1,-2  => 1, -1, -2

Samples, 3 roots:
1,-4, 7, -4 => 1
1,0,-2,4    => -2

Samples, no roots:
1,2,3,4
1,0,3,1

"""

import csv
import math
import time

def get_divisors(n: int)->set:
    """ returns a set of positive divisors of n """
    divisors = set()
    for i in range(1, int(math.sqrt(n)) + 1):
        if n % i == 0:
            divisors.add(i)
            divisors.add(n // i)

    return divisors

"""
Solve the cubic equation a*x^3 + b*x^2 + c*x + d = 0 for rational roots only.
Use the Rational Root Theorem: candidates are factors of d divided by factors of a.
Returns a tuple of three roots. 
If no rational roota are not found root remain None.
"""
def solve_cubic(a: float, b: float, c: float, d: float, tol: float = 1e-6)->tuple:
	
    # ensure we have a cubic equation
    if a == 0:
        return (None, None, None)
    
    # convert a and d to integers for divisor calculation.
    a_int = int(round(a))
    d_int = int(round(d))
    if a_int == 0:
        a_int = 1

    # get positive divisors for |a| and |d|
    divisors_a = get_divisors(abs(a_int))
    divisors_d = get_divisors(abs(d_int)) if d_int != 0 else {0}
    
    # generate candidate rational roots: ±(factor of d)/(factor of a)
    possible_roots = set()
    for p in divisors_d:
        for q in divisors_a:
            if q != 0:
                possible_roots.add(p / q)
                possible_roots.add(-p / q)
    
    # test each candidate in the cubic equation.
    rational_roots = []
    for r in possible_roots:
        value = a * r**3 + b * r**2 + c * r + d
        if abs(value) < tol:
            rational_roots.append(r)
    
    # remove duplicates and sort
    rational_roots = list(set(rational_roots))
    
    # return up to three roots
    if len(rational_roots) == 0:
        return (None, None, None)
    elif len(rational_roots) == 1:
        return (rational_roots[0], None, None)
    elif len(rational_roots) == 2:
        return (rational_roots[0], rational_roots[1], None)
    else:
        return (rational_roots[0], rational_roots[1], rational_roots[2])

# Emojis for diagnostics: smile, thumb-up and oh-oh 
SML = "\U0001F600"
TUP = "\U0001F44D: "
OOO = "\U0001F631\t "

# Counters
tce = 0       # Total number of cubic equations
tqe = 0       # Total number of quadratic equations (a == 0 )
tle = 0       # Total number of linear equations (a and b are 0)
no_rts = 0    # Total number of equations with no roots: (None, None, None))

# reading from a CSV and writing results 
data_file = 'cubic_data_1000.csv'         	    # Input CSV with rows: a,b,c,d
results_file = 'cubic_results_1000.csv'     	        # Output CSV with a,b,c,d and roots

total = 0
start = time.time()

try:
    with open(data_file, 'r', newline='') as fin, open(results_file, 'w', newline='') as fout:
        reader = csv.reader(fin)
        writer = csv.writer(fout)
        
        # write header row
        writer.writerow(["a", "b", "c", "d", "r1", "r2", "r3"])
        
        for row in reader:
            total += 1
            try:
                # convert input strings to floats; row should have four values
                a, b, c, d = map(float, row)
            except Exception as e:
                # skip malformatted rows
                continue
                
            # ccount the equation type
            if a == 0:
                if b == 0:
                    tle += 1
                else:
                    tqe += 1
            else:
                tce += 1            
                
            # solve cubic equation for rational roots
            r1, r2, r3 = solve_cubic(a, b, c, d)
            if r1 is None and r2 is None and r3 is None:
                no_rts += 1            
            writer.writerow([a, b, c, d, r1, r2, r3])
except Exception as exp:
    print(f"{OOO}Failed to process {data_file}! Error: {exp}")
else:
    elapsed = time.time() - start
    print(f"{TUP}Processed {total} recors in {elapsed:.3f} seconds")
    print(f"cubic: {tce}, quadratic: {tqe}, linear: {tle}, no roots: {no_rts}\n{SML}")

"""
HP Server
----------
CE> python mr-ce-simple.py
👍: Processed 100000006 recors in 403.991 seconds
cubic: 88891257, quadratic: 11108748, linear: 0, no roots: 44442124
😀

CE> pypy mr-ce-simple.py
Processed 100000006 recors in 309.957 seconds
cubic: 88891257, quadratic: 11108748, linear: 0, no roots: 44442124
"""