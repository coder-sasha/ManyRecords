"""
Dec 20 2024
Project ManyRecords: 
ce-pandas.py 
This is pandas based script to solve cubic equations
a,b,c,d are parameters of an equation fromteh data file
These files serve as input for performance testing programs in Python and C++.
"""

import math
import time
import pandas as pd


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
# def solve_cubic(a: float, b: float, c: float, d: float, tol: float = 1e-6)->tuple:
def solve_cubic(params: list, tol: float = 1e-6)->str:	

    a,b,c,d,r = params
    ret = 'None, None, None'
    # ensure we have a cubic equation   
    if a == 0:
        return ret
    
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
    roots = list(set(rational_roots))
    
    # return up to three roots
    if len(roots) == 3:
        ret = f"{roots[0]}, {roots[1]}, {roots[2]}"
    elif len(roots) == 2:
        ret = f"{roots[0]}, {roots[1]}, None"
    elif len(roots) == 1:
        ret = f"{roots[0]}, None, None"
        
    return ret    

# Emojis for diagnostics: smile, thumb-up and oh-oh 
SML = "\U0001F600"
TUP = "\U0001F44D: "
OOO = "\U0001F631\t "

# Counters
tce = 0       # Total number of cubic equations
tqe = 0       # Total number of quadratic equations (a == 0 )
tle = 0       # Total number of linear equations (a and b are 0)
no_rts = 0    # Total number of equations with no roots: (None, None, None))

# Reading data and writing results from/into CSV file
data_name = 'cubic_data_100_000_000_same.csv'         	    # Input CSV with rows: a,b,c,d
res_name = 'cubic_results_100_000_000.csv'	     	        # Output CSV with a,b,c,d and roots

total = 0
start = time.time()    
try:
    df_eq = pd.read_csv(data_name, header=0, index_col=False)
except Exception as exp:
	print(f"{OOO}Failed to read equations from {data_name}! Error: {str(exp)}")
else: 
    total = len(df_eq)
    df_eq['roots'] = [None] * len(df_eq)

    # solve all equations
    roots_df = df_eq.apply(solve_cubic, axis=1)
    df_eq['roots'] = roots_df

    # count number of equations without roots
    no_rts = df_eq['roots'].value_counts()['None, None, None']
    print(f"{TUP}{total} records, {len(df_eq)} equations, {no_rts} without roots, calculations time={(time.time() - start):.3f} sec")	

    # save results into CSV
    df_eq.to_csv(res_name, index=False)
    print(f"{TUP}Total running time={(time.time() - start):.3f} sec\n{SML}")	
            
            
"""
> python ce_pandas.py
👍: 100000005 records, 100000005 equations, 44442124 without roots, calculations time=509.068 sec
👍: Total running time=570.530 sec
😀
"""