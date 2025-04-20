"""
Dec 20 2024
Project ManyRecords 
mr-qe-polars.py 
This is polars based processing of 100M quadratic equations
"""

import time
import polars as pl
import math

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

pl.Config.set_tbl_rows(100_000_010)
# Read CSV file without a header and assign column names.
df = pl.read_csv(data_name, has_header=False, new_columns=["a", "b", "c"])

# Compute the discriminant: disc = b^2 - 4ac
df = df.with_columns(
    (pl.col("b") ** 2 - 4 * pl.col("a") * pl.col("c")).alias("disc")
)

# Compute the roots using vectorized expressions.
df = df.with_columns([
    pl.when(pl.col("disc") < 0)
      .then(None)
      .when(pl.col("disc") == 0)
      .then(-pl.col("b") / (2 * pl.col("a")))
      .otherwise(( -pl.col("b") + (pl.col("disc") ** 0.5) ) / (2 * pl.col("a")))
      .alias("r1"),
    pl.when(pl.col("disc") < 0)
      .then(None)
      .when(pl.col("disc") == 0)
      .then(None)
      .otherwise(( -pl.col("b") - (pl.col("disc") ** 0.5) ) / (2 * pl.col("a")))
      .alias("r2")
])

# Create a formatted solution string column.
df = df.with_columns(
    pl.concat_str([
        pl.lit("r1="), 
        pl.col("r1"), 
        pl.lit(" r2="), 
        pl.col("r2")
    ]).alias("solution")
)

print(f"{TUP}CPU time={(time.time() - start):.3f}")

df.write_csv(res_name)

print(f"{TUP}Total time={(time.time() - start):.3f} sec\ndone   :)")    

