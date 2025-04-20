
import os
import sys
import difflib

def check_files_difference(p2file1, p2file2):
    """Compares two files and prints the differences in unified diff format."""
    print("Checking difference between: ", p2file1, p2file2)

    for f in [p2file1, p2file2]:
        if not os.path.isfile(f):
            print(f"file '{f}' does not exist!")
            exit(1)

        s = os.stat(f)
        print(f"{f} is\t\t{s.st_size} bytes")

    with open(p2file1, 'r') as file1, open(p2file2, 'r') as file2:
        file1_lines = file1.readlines()
        file2_lines = file2.readlines()

    diff = difflib.unified_diff(file1_lines, file2_lines, fromfile=p2file1, tofile=p2file2)
       
    for line in diff:
        print(line, end='')

# run
if len(sys.argv) > 2:
    check_files_difference(sys.argv[1], sys.argv[2])
else:
    print("Files names?..")
