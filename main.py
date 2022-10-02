from collections import defaultdict

from apriori import apriori
from fp_growth import fp_growth



def read_ibm_data(path='inputs/ibm-2021.txt'):
    """
    return a list of list, which each element represent a transaction
    """
    d = defaultdict(list)
    with open(path, 'r') as f:
        for l in f.readlines():
            cid, tid, iid = l.strip().split()
            d[int(tid)].append(int(iid))
    return list(dict(d).values())
    

def read_kaggle_data(path='inputs/kaggle.txt'):
    d = defaultdict(list)
    with open(path, 'r') as f:
        for l in f.readlines():
            tid, date, item = l.strip().split(',')
            d[int(tid)].append(item)
    return list(dict(d).values())


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
    min_support = 0.015
    min_confidance = 0.001

    ibm_data = read_ibm_data()
    kaggle_data = read_kaggle_data()

    # run apriori on ibm data
    rules = apriori(ibm_data, min_support=min_support, min_confidance=min_confidance)
    write_csv(rules, 'outputs/ibm-2021-apriori.csv')

    # run fp-growth on ibm data
    rules = fp_growth(ibm_data, min_support=min_support, min_confidance=min_confidance)
    write_csv(rules, 'outputs/ibm-2021-fp_growth.csv')

    # run apriori on kaggle data
    rules = apriori(kaggle_data, min_support=min_support, min_confidance=min_confidance)
    write_csv(rules, 'outputs/kaggle-apriori.csv')

    # run fp_growth on kaggle data
    rules = fp_growth(kaggle_data, min_support=min_support, min_confidance=min_confidance)
    write_csv(rules, 'outputs/kaggle-fp_growth.csv')









