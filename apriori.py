from pdb import set_trace as bp
from itertools import combinations, chain
from collections import defaultdict


def generate_lk_set(item_set, transactions, min_support):
    lk_set = defaultdict(int)
    ret_item_set = set()
    
    # compute support_count
    for item in item_set:
        for trx in transactions:
            if item.issubset(trx):
                lk_set[item] += 1
        
    # prune item by support
    for k in list(lk_set.keys()):
        lk_set[k] /= len(transactions)
        if lk_set[k] < min_support:
            del lk_set[k]
        else:
            ret_item_set.add(k)
    
    return ret_item_set, lk_set


def apriori(transactions, min_support=0.4, min_confidance=0.15):

    # generate L1 set and C1 set
    item_set = set(frozenset([item]) for trx in transactions for item in trx)
    item_set, l_set = generate_lk_set(item_set, transactions, min_support)

    # generate frequent set
    k = 2
    while len(item_set):
        # self join
        item_set = set(a.union(b) for a in item_set for b in item_set if len(a.union(b)) == k)
        # generate item_set and Lk_set filtered by min_support
        item_set, lk_set = generate_lk_set(item_set, transactions, min_support)
        # update frequent set
        l_set.update(lk_set)
        k += 1
        
    # generate rules
    rules = []
    for m in l_set:

        m_support = l_set[m]
        # generate all subsets of m excludes m itself
        subsets = chain(*[combinations(m, i + 1) for i in range(len(m)-1)])
        subsets = set(frozenset(s) for s in subsets)

        # generate rules that satisfy p -> (m-p) > min_confidance
        for p in subsets:
            p_support = l_set[p]
            confidance = m_support / p_support
            if confidance > min_confidance:
                remain_support = l_set[m-p]
                lift = m_support / (remain_support * p_support)
                rules.append(
                    (
                        (tuple(p), tuple(m-p)), # p -> (m-p)
                        m_support,
                        confidance,
                        lift
                    )
                )
    return rules


def test_apriori():
    transactions = [
        (1, 3, 4),
        (2, 3, 5),
        (1, 2, 3, 5),
        (2, 5),
        (1, 3, 5)
    ]
    transactions = [frozenset(t) for t in transactions]
    apriori(transactions)
