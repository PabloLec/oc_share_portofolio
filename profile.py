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

    for r in results:
        print(r)
    print("\n\n")

    append_to_csv(1)
    nb_of_shares += 1

for r in results:
    print(r)

exit()

optimized.MONEY_INVESTED = 5000
print("\nMoney = 5000 - No filter")
print(timeit.repeat(stmt="optimized.main()", repeat=10, number=10, globals=globals()), "s")

print("Peak memory (MiB):", int(getrusage(RUSAGE_SELF).ru_maxrss / 1024))

exit()

optimized.FILTER_DATA = True
optimized.REDUCTION_FACTOR = 2
print("\nMoney = 500 - Reduction Factor 2")
print(timeit.repeat(stmt="optimized.main()", number=10, globals=globals()), "s")

print("Peak memory (MiB):", int(getrusage(RUSAGE_SELF).ru_maxrss / 1024))

optimized.REDUCTION_FACTOR = 5
print("\nMoney = 500 - Reduction Factor 5")
print(timeit.repeat(stmt="optimized.main()", number=10, globals=globals()), "s")

print("Peak memory (MiB):", int(getrusage(RUSAGE_SELF).ru_maxrss / 1024))

optimized.REDUCTION_FACTOR = 10
print("\nMoney = 500 - Reduction Factor 10")
print(timeit.repeat(stmt="optimized.main()", number=10, globals=globals()), "s")

print("Peak memory (MiB):", int(getrusage(RUSAGE_SELF).ru_maxrss / 1024))

optimized.MONEY_INVESTED = 5000
print("\nMoney = 5000 - Reduction Factor 10")
print(timeit.repeat(stmt="optimized.main()", number=10, globals=globals()), "s")

print("Peak memory (MiB):", int(getrusage(RUSAGE_SELF).ru_maxrss / 1024))

optimized.MONEY_INVESTED = 50000
print("\nMoney = 50000 - Reduction Factor 10")
print(timeit.repeat(stmt="optimized.main()", number=10, globals=globals()), "s")

print("Peak memory (MiB):", int(getrusage(RUSAGE_SELF).ru_maxrss / 1024))
