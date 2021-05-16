import pathlib

from csv import reader
from math import ceil

MONEY_INVESTED = 500

# Sort data by price clusters and ignore least profitable ones to speed up process.
FILTER_DATA = False
REDUCTION_FACTOR = 10

PROJECT_DIR = pathlib.Path(__file__).parent.absolute()
DATA_SETS = list(pathlib.Path(PROJECT_DIR).glob("*.csv"))
SHARES_LIST = None


def load_dataset(dataset: int) -> None:
    global SHARES_LIST

    with open(dataset, newline="") as f:
        r = reader(f)

        # Ignore csv columns header.
        next(r)

        # Ignore negative and null cost shares.
        shares_raw = [x for x in r if x[1][0] != "-" and x[1] != "0.0"]
        SHARES_LIST = [(x, int(float(y) * 100), float(z)) for [x, y, z] in shares_raw]

        if FILTER_DATA:
            SHARES_LIST = cluster_dataset(SHARES_LIST)


def print_result(best_outcome: list) -> None:
    print("- Cost:", sum(best_outcome[2]) / 100, "€")
    print("- Profit:", best_outcome[0] / 100, "€")
    print("- Selected shares:\n    -", "\n    - ".join(best_outcome[1]))


def cluster_dataset(dataset: list) -> list:
    """Creates clusters of shares grouped by cost.
    Filters out the least profitable ones.

    Args:
        dataset (list): Original dataset.

    Returns:
        list: Filtered dataset.
    """

    # Set clusters length to 1% of total length.
    cluster_length = round(len(dataset) / 100)

    if cluster_length <= 1:
        print(" ! Dataset is too small to be clustered, dataset will not be modified !")
        return dataset

    shares_left_by_cluster = cluster_length / REDUCTION_FACTOR

    if shares_left_by_cluster < 1:
        print("\n ! Reduction factor too big for this dataset, reduction factor set to", cluster_length, " !\n")

    remove_n_first_shares = int(cluster_length - ceil(shares_left_by_cluster))

    # Sort and group shares by cost.
    dataset.sort(key=lambda x: x[1])
    clusters = [dataset[i : i + cluster_length] for i in range(0, len(dataset), cluster_length)]
    print("Previous dataset length:", len(dataset))

    i = 0
    for cluster in clusters:
        if len(cluster) < cluster_length:
            continue

        # Sort clusters by profit %.
        dataset.sort(key=lambda dataset: dataset[2])

        clusters[i] = cluster[remove_n_first_shares:]
        i += 1

    dataset = list([y for x in clusters for y in x])
    print("Filtered dataset length:", len(dataset), "\n")

    return dataset


def find_best_portofolio(money_invested: int, shares: list) -> None:
    """Finds the best portofolio share distribution using a dynamic programmation
    algorithm.
    It considers every share possible and determines if adding it to portofolio
    is worth by comparing potential profit with previous share results.

    Args:
        money_invested (int): Total portofolio cost.
        shares (list): List of selectable shares.
    """

    # *100 to allow working with decimals.
    money_invested *= 100

    # Matrix of [Profit, Name, Cost] * money_invested
    matrix = [[0, [], []] for x in range(money_invested + 1)]

    # Named list index for readability.
    m_profit = 0
    m_name = 1
    m_cost = 2

    # Iterate through all selectable shares
    for i in range(1, len(shares) + 1):
        current_share = shares[i - 1]

        name = current_share[0]
        cost = current_share[1]
        profit = (cost / 100) * current_share[2]

        # Iterate from 0 to money_invested.
        # For each possible portofolio cost, check if currently considered
        # share would be a more profitable choice.
        for m in range(money_invested, cost, -1):

            # Best possible profit with previous share minus current share cost.
            best_profit_minus_cost = matrix[m - cost]

            # Best possible profit with previous share at the same total cost.
            best_same_cost_profit = matrix[m][m_profit]

            # Possible profit if current share is added to portofolio.
            current_profit = best_profit_minus_cost[m_profit] + profit

            # If adding current share is more profitable. Else keep previous share result.
            if current_profit > best_same_cost_profit:
                # Add current share to the portofolio.
                matrix[m][m_profit] = current_profit
                matrix[m][m_name] = best_profit_minus_cost[m_name] + [name]
                matrix[m][m_cost] = best_profit_minus_cost[m_cost] + [cost]


def main() -> None:
    global SHARES_LIST

    for dataset in DATA_SETS:
        load_dataset(dataset=dataset)

        # If total cost of all shares is <= MONEY_INVESTED, then all shares
        # could just be returned to have O(1) time complexity
        # on great MONEY_INVESTED values.

        find_best_portofolio(money_invested=MONEY_INVESTED, shares=SHARES_LIST)


if __name__ == "__main__":
    main()
