from collections import defaultdict

from apriori import apriori



def read_ibm_data(path):
    d = defaultdict(set)
    with open(path, 'r') as f:
        for l in f.readlines():
            cid, tid, iid = l.split()
            d[int(tid)].add(int(iid))
    return [frozenset(v) for v in dict(d).values()]


def read_kaggle_data(path):
    pass


def write_csv(rules, path):
    """
    rules: 
        - a list of tuple (relationship, support, confidence, lift)
        - relationship: [p, m-p]
    """
    with open(path, 'w') as f:
        f.write('relationship,support,confidence,lift\n')
        for rel, sup, conf, lift in rules:
            f.write(f'{set(rel[0])} -> {set(rel[1])}, {sup}, {conf}, {lift}\n')


if __name__ == '__main__':
    ibm_data = read_ibm_data('inputs/ibm-2021.txt')

    # run apriori on ibm data
    aprior_rules = apriori(ibm_data, min_support=0.02, min_confidance=0.6)
    write_csv(aprior_rules, 'outputs/ibm-2021-apriori2.csv')

    # run fp-growth on ibm data








