"""
Dec 20 2024
Project ManyRecords 
mr-qe-pandas.py 
This is QnD pandas script to solve quadratic equation
a,b,c - parameters of square equation
"""

import math
import time
import pandas as pd

def solve(params):
 
    try:
        pa, pb, pc = params
        ret = 'None, None'
        
        if not pa:
            # pa is 0: the equation is linear
            if pb != 0:
                ret = f"r1={round((pc / pb), 3)},r2=None"
            return ret    

        if pa:
            two_a = pa * 2
            discr = pb * pb - 2 * two_a * pc
            if discr < 0:
                return ret    
                
            if discr > 0:
                sqrt_disc = math.sqrt(discr)
                ret = f"r1={round((-pb + sqrt_disc) / two_a, 3)} r2={round((-pb - sqrt_disc) / two_a, 3)}"
            else:
                ret = f"r1={round(-(pb / two_a), 3)},r2=None"
                
        return ret
    except Exception as exp:
        print(f"{OOO}Failed to parse equation parameters {params}! Error: {str(exp)}")
        exit(1)
    

# emojis for diagnostics: smile, thumb-up and oh-oh 
SML = "\U0001F600"
TUP = "\U0001F44D: "
OOO = "\U0001F631\t "

# counters
no_rts = 0      # total number of equations with no roots: (None, None)
ttl_rec = 0     # total number of equations           

# reading data and writing results from/into CSV file
data_name = 'qe_data_100_000_000_same.csv'
res_name = 'qe_results_same.csv'

start = time.time()    

try:
    df_eq = pd.read_csv(data_name, header=0, index_col=False)
except Exception as exp:
    print(f"{OOO}Failed to complete all equations from {data_name}! Error: {str(exp)}")
else:    
    ttl_rec = len(df_eq)
    # solve all equations
    roots_df = df_eq.apply(solve, axis=1)
    df_eq['roots'] = roots_df
    
    # count rows without roots
    no_rts = df_eq['roots'].value_counts()['None, None']
    print(f"{TUP}{len(df_eq)} records, {no_rts} without roots, calculation time={(time.time() - start):.3f} sec")	

    df_eq.to_csv(res_name, index=False)    
    print(f"{TUP}Total running time={(time.time() - start):.3f} sec\n{SML}")	            
