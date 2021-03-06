import pathlib

from csv import reader


MONEY_INVESTED = 500

PROJECT_DIR = pathlib.Path(__file__).parent.absolute()
DATASETS = list(pathlib.Path(PROJECT_DIR).glob("*.csv"))
SHARES_LIST = None


def load_dataset(dataset: int) -> None:
    global SHARES_LIST

    with open(dataset, newline="") as f:
        r = reader(f)

        # Ignore csv columns header.
        next(r)

        # Ignore negative and null cost shares.
        shares_raw = [x for x in r if x[1][0] != "-" and x[1] != "0.0"]
        SHARES_LIST = [(x, float(y), (float(y) / 100) * float(z)) for [x, y, z] in shares_raw]


def find_best_portofolio(money_invested: int, shares: list) -> None:
    best_portofolio = [0, [], 0]

    for i in range(1, len(shares) + 1):

        possible_portofolios = combinations(shares, i)
        for portofolio in possible_portofolios:

            portofolio_cost = sum([x[1] for x in portofolio])

            if portofolio_cost > money_invested:
                continue

            portofolio_profit = sum([x[2] for x in portofolio])

            if portofolio_profit > best_portofolio[0]:
                portofolio_names = [x[0] for x in portofolio]
                best_portofolio = [portofolio_profit, portofolio_names, portofolio_cost]

    print(best_portofolio)


def combinations(iterable, r):
    pool = tuple(iterable)
    n = len(pool)

    if r > n:
        return
    indices = list(range(r))

    yield tuple(pool[i] for i in indices)

    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return

        indices[i] += 1

        for j in range(i + 1, r):
            indices[j] = indices[j - 1] + 1

        yield tuple(pool[i] for i in indices)


def main() -> None:
    global SHARES_LIST

    for dataset in DATASETS:
        print("Processing: ", dataset, "\n")

        load_dataset(dataset=dataset)

        find_best_portofolio(money_invested=MONEY_INVESTED, shares=SHARES_LIST)


if __name__ == "__main__":
    main()
