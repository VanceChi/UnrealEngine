from pprint import pprint
records = []
with open('sample_master.txt', 'r') as file:
    for line in file:
        parts = line.strip().split()
        records.append(parts)
    pprint(records)

