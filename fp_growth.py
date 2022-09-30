from pdb import set_trace as bp


def fp_growth(transactions, support, confidance):
    pass


def test_fp_growth():
    transactions = [
        (1, 3, 4),
        (2, 3, 5),
        (1, 2, 3, 5),
        (2, 5),
        (1, 3, 5)
    ]
    transactions = [frozenset(t) for t in transactions]
    fp_growth(transactions)

test_fp_growth()