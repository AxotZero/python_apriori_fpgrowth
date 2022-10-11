from collections import defaultdict
from generate_rule import generate_rule

from math import ceil


class FPNode:
    def __init__(self, item=None, count=0, parent=None):
        self.item = item
        self.parent = parent
        self.childs = {} # key: child_item, value: child_node
        self.count = count
        self.next = None


class HeaderNode:
    def __init__(self):
        self.node = None
        self.count = 0


def construct_header_table(item_set_table, min_support_count=100):
    # generate header_table from item_set 
    header_table = defaultdict(HeaderNode)
    for item_set, count in item_set_table.items():
        for item in item_set:
            header_table[item].count += count
    
    # prune header table
    header_table = {k:v for k, v in header_table.items() if v.count >= min_support_count}
    if len(header_table) == 0:
        return None
    
    # build fp_tree
    fp_root = FPNode()
    for item_set, count in item_set_table.items():
        item_set = [item for item in item_set if item in header_table]
        item_set.sort(key=lambda a: (header_table[a].count, a)) # reverse
        node = fp_root
        for item in item_set:
            # build fp_node
            if item in node.childs:
                node.childs[item].count += count
                node = node.childs[item]
            else:
                node.childs[item] = FPNode(item, count, node)
                node = node.childs[item]

                # link header table
                if header_table[item].node is None:
                    header_table[item].node = node
                else:
                    n = header_table[item].node
                    while n.next:
                        n = n.next
                    n.next = node

    return header_table


def mine_tree(header_table=None, min_support_count=100, freq_item_table={}, prev_item_set=set()):
    # sort header table by count and key
    header_table = {k:v for k, v in sorted(list(header_table.items()), 
                                           key=lambda x: (x[1].count, x[0]))}
    for item, header_node in header_table.items():
        freq_set = prev_item_set | {item}
        freq_item_table[frozenset(freq_set)] = freq_item_table.get(frozenset(freq_set), 0) + header_node.count
        
        # generate new item set table
        item_set_table = {}
        fp_node = header_node.node
        while fp_node:
            # traverse the path
            item_set = []
            node = fp_node
            while node.item is not None:
                item_set.append(node.item)
                node = node.parent
            item_set_table[frozenset(item_set[1:])] = fp_node.count

            fp_node = fp_node.next

        # construct conditional fp header table
        new_header_table = construct_header_table(item_set_table, min_support_count)
        if new_header_table is not None:
            mine_tree(new_header_table, min_support_count, freq_item_table, freq_set)


def fp_growth(transactions, min_support=0.4, min_confidance=0.15, return_rule=True, save_path=None):
    # build base item set table
    item_set_table = {}
    for trx in transactions:
        trx = frozenset(trx)
        item_set_table[trx] = item_set_table.get(trx, 0) + 1

    # build fp_tree
    min_support_count = ceil(min_support * len(transactions)) 
    header_table = construct_header_table(item_set_table, min_support_count)
    if header_table is None:
        return []

    # mine tree
    freq_item_table = {}
    mine_tree(header_table, min_support_count, freq_item_table, prev_item_set=set())
    # convert support_count to support 
    for k in freq_item_table:
        freq_item_table[k] /= len(transactions)

    if return_rule:
        rules = generate_rule(freq_item_table, min_confidance, save_path)
        return rules
    return freq_item_table