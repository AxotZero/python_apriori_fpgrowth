from itertools import combinations, chain

# generate rules
def generate_rule(freq_item_table, min_confidance=0.15):
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
                rules.append(
                    (
                        (tuple(p), tuple(m-p)), # p -> (m-p)
                        m_support,
                        confidance,
                        lift
                    )
                )
    rules.sort(key=lambda x: x[1])
    return rules