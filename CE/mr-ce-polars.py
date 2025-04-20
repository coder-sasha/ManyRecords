import math
import time
import polars as pl
from polars import Float64


def get_divisors(n: int):
    divisors = set()
    for i in range(1, int(math.sqrt(n)) + 1):
        if n % i == 0:
            divisors.add(i)
            divisors.add(n // i)
    return divisors


def solve_rational_roots_row(a, b, c, d, tol=1e-6):
    if a == 0:
        return (None, None, None)

    a_int = int(round(a))
    d_int = int(round(d))
    if a_int == 0:
        a_int = 1

    divisors_a = get_divisors(abs(a_int))
    divisors_d = get_divisors(abs(d_int)) if d_int != 0 else {0}

    candidates = set()
    for p in divisors_d:
        for q in divisors_a:
            if q:
                candidates.add(p / q)
                candidates.add(-p / q)

    rational_roots = []
    for r in candidates:
        value = a * r**3 + b * r**2 + c * r + d
        if abs(value) < tol:
            rational_roots.append(r)

    rational_roots = sorted(set(rational_roots))

    if len(rational_roots) == 0:
        return (None, None, None)
    elif len(rational_roots) == 1:
        return (rational_roots[0], None, None)
    elif len(rational_roots) == 2:
        return (rational_roots[0], rational_roots[1], None)
    else:
        return (rational_roots[0], rational_roots[1], rational_roots[2])


def solve_batch(batch: pl.DataFrame) -> pl.DataFrame:
    results = [solve_rational_roots_row(a, b, c, d) for a, b, c, d in zip(batch["a"], batch["b"], batch["c"], batch["d"])]
    root1, root2, root3 = zip(*results)
    return batch.with_columns([
        pl.Series("root1", root1, dtype=pl.Float64),
        pl.Series("root2", root2, dtype=pl.Float64),
        pl.Series("root3", root3, dtype=pl.Float64),
    ])


def main():
    # Emojis for diagnostics: smile, thumb-up and oh-oh 
    SML = "\U0001F600"
    TUP = "\U0001F44D: "
    OOO = "\U0001F631\t "    
    start = time.time()

    data_name = "cubic_data_100_000_000_same.csv"
    res_name = "cubic_results.csv"

    df = pl.read_csv(data_name)

    # Strip and cast only if needed
    for col in ["a", "b", "c", "d"]:
        if df.schema[col] == pl.Utf8:
            df = df.with_columns(pl.col(col).str.strip_chars().cast(pl.Float64))
        else:
            df = df.with_columns(pl.col(col).cast(pl.Float64))

    # Process using map_batches for performance
    #df = df.lazy().map_batches(solve_batch).collect()
    
    new_schema = {
        "a": Float64,
        "b": Float64,
        "c": Float64,
        "d": Float64,
        "root1": Float64,
        "root2": Float64,
        "root3": Float64,
    }
   
    df = df.lazy().map_batches(solve_batch, streamable=True, schema=new_schema).collect()

    total = df.height
    no_roots = df.filter(pl.col("root1").is_null()).height

    print(f"{TUP}Total records: {total}, {no_roots} without roots, CPU time: {time.time() - start:.3f} sec")

    df.write_csv(res_name)
    print(f"{TUP}Results saved to {res_name}. Total running time: {time.time() - start:.3f} sec.{SML}")

if __name__ == "__main__":
    main()