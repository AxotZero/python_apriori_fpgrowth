from pdb import set_trace as bp

from collections import defaultdict

from apriori import apriori
from fp_growth import fp_growth
from generate_rule import generate_rule


def read_ibm_data(path='inputs/ibm-2022.txt'):
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


if __name__ == '__main__':
    ibm2022_data = read_ibm_data('inputs/ibm-2022.txt')
    kaggle_data = read_kaggle_data('inputs/kaggle.txt')

    ## run ibm-2022 data
    min_support = 0.1
    min_confidance = 0.1
    generate_rule(apriori(ibm2022_data, min_support), min_confidance, save_path='outputs/ibm-2022-apriori.csv')
    generate_rule(fp_growth(ibm2022_data, min_support), min_confidance, save_path='outputs/ibm-2022-fp_growth.csv')

    ## run kaggle data
    min_support = 0.01
    min_confidance = 0.01
    generate_rule(apriori(kaggle_data, min_support), min_confidance, save_path='outputs/kaggle-apriori.csv')
    generate_rule(fp_growth(kaggle_data, min_support), min_confidance, save_path='outputs/kaggle-fp_growth.csv')
