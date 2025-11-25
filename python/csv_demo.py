import csv
import io

csv_string = """a,b,c
1,2,3
4,5,6
"""

with io.StringIO(csv_string) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row["a"], row["b"], row["c"])
