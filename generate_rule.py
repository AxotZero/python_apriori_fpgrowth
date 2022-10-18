from itertools import combinations, chain

# generate rules
def generate_rule(freq_item_table, min_confidance=0.15, save_path=None):
    rules = []
    for m in freq_item_table:
        m_support = freq_item_table[m]
        # generate all subsets of m excludes m itself
        subsets = chain(*[combinations(m, i) for i in range(1, len(m))])
        subsets = set(frozenset(s) for s in subsets)

        # generate rules that satisfy p -> (m-p) > min_confidance
        for p in subsets:
            p_support = freq_item_table[p]
            confidance = m_support / p_support
            if confidance > min_confidance:
                remain_support = freq_item_table[m-p]
                lift = m_support / (remain_support * p_support)
                rule = [
                    p, 
                    m-p,
                    m_support,
                    confidance,
                    lift
                ]
                for i in range(2, len(rule)):
                    rule[i] = round(rule[i], 3)
                rules.append(rule)
    if save_path:
        write_csv(rules, save_path)

    return rules


def write_csv(rules, path):
    with open(path, 'w') as f:
        f.write('antecedent,consequent,support,confidence,lift\n')
        for ant, con, sup, conf, lift in rules:
            ant_str = '{' + ' '.join([str(i) for i in ant]) + '}'
            con_str = '{' + ' '.join([str(i) for i in con]) + '}'
            f.write(f'{ant_str}, {con_str}, {sup}, {conf}, {lift}\n')