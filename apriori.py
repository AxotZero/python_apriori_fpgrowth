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


def apriori(transactions, min_support=0.4):
    transactions = [frozenset(t) for t in transactions]

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

    return l_set