import optimized
import bruteforce
from resource import getrusage, RUSAGE_SELF
import timeit
import pathlib
import csv


def append_to_csv(n):
    with open("/home/pablo/openclassrooms/P7/oc_share_portofolio/dataset3.csv", "a") as f:
        for i in range(n):
            writer = csv.writer(f)
            writer.writerow(["Action-1", "20", "5"])

    bruteforce.DATASETS = list(pathlib.Path(bruteforce.PROJECT_DIR).glob("*3.csv"))
    optimized.DATASETS = bruteforce.DATASETS


def add_money(n):
    bruteforce.MONEY_INVESTED += n
    optimized.MONEY_INVESTED += n


nb_of_shares = 1
results = []

for i in range(1, 26):
    bruteforce.main()
    ram = int(getrusage(RUSAGE_SELF).ru_maxrss / 1024)
    results.append((nb_of_shares, ram))

    append_to_csv(1)
    nb_of_shares += 1

for r in results:
    print(r)
