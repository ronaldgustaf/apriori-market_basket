import pandas as pd
import numpy as np
from itertools import combinations
from collections import defaultdict

import time

# class for trie data structure
class TrieNode:
    def __init__(self, item):
        self.item = item
        self.count = 0
        self.children = {}


class Trie:
    def __init__(self, hash_table):
        self.root = TrieNode(None)
        self.hash_table = hash_table
        for ids in hash_table.values():
            self.insert(ids, self.root)

    def insert(self, ids, node):
        for id in ids:
            if id not in node.children:
                node.children[id] = TrieNode(id)
            node = node.children[id]
            node.count += 1

    def count_occurrences(self, C, k):

        for transaction, ids in list(self.hash_table.items()):
            if len(ids) < k:
                del self.hash_table[transaction]

        C_count = {ids: 0 for ids in C}

        for ids in self.hash_table.values():

            for ids_comb in  self.get_k_item_subsets(ids, k):
                if frozenset(ids_comb) in C_count:
                    C_count[frozenset(ids_comb)] += 1

        return C_count

    def get_k_item_subsets(self, ids, k):
        for i in range(1, k + 1):
            yield from combinations(ids, i)

    def prune(self, min_sup):
        self._prune(self.root, min_sup)

    def _prune(self, node, min_sup):
        for child_key in list(node.children.keys()):
            child = node.children[child_key]
            if child.count < min_sup:
                del node.children[child_key]
            else:
                self._prune(child, min_sup)

# functions for apriori algorithm
def delete_below_min_sup(item_set, min_sup):
    return {k:v for k,v in item_set.items() if v >= min_sup}

def self_join(L, n_items):
    s = set()
    for k in L.keys():
        s |= k

    joined_C = set()
    for c1 in L.keys():
        for c2 in L.keys():
            if len(c1.union(c2)) == n_items:
                joined_C.add(c1.union(c2))

    return joined_C

def prune_candidates(C, L, k):
    pruned_C = set()

    for candidate in C:
        subsets = [frozenset(subset) for subset in combinations(candidate, k-1)]
        if all(subset in L for subset in subsets):
            pruned_C.add(candidate)
            
    return pruned_C

# min_freq = min_sup/n_transaction, get min_sup array
n_transaction = 700000
min_freqs = [0.0001, 0.0002, 0.0003, 0.0004, 0.0005]
min_sup_arr = [min_freq * n_transaction for min_freq in min_freqs]

# trans.txt preprocessing, convert into numpy array of sets
df = pd.read_csv("trans.txt", header=None, names=["id"])
df = df.apply(lambda x: x.str.replace("\t", ","))
df["id"] = df["id"].apply(lambda x: [s for s in x.split(',')])

hash_table = defaultdict(list)

for i, transaction in df["id"].iteritems():
    transaction.sort(key = int)
    hash_table[i] = transaction

def apriori(hash_table, min_sup):
    # counting 1-itemset occurence from transactions
    C1 = {}

    for ids in hash_table.values():
        for id in ids:
            if id not in C1.keys():
                C1[id] = 1
            else:
                C1[id] += 1
    # remove itemset that does not meet min_sup
    L1 = delete_below_min_sup(C1, min_sup)
    L1 = {frozenset([k]): v for k, v in L1.items()}

    # inserting all transactions to trie
    trie = Trie(hash_table)
    # prune nodes that are below min_sup
    trie.prune(min_sup)

    # running apriori algorithm
    k = 2
    current_L = L1
    frequent_ids = {}

    while(current_L):

        frequent_ids[k-1] = current_L
        Ck = self_join(current_L, k)
        Ck = prune_candidates(Ck, current_L, k)
        # count occurrences using the trie
        Ck_count = trie.count_occurrences(Ck, k)
        current_L = delete_below_min_sup(Ck_count, min_sup)
        k += 1

    return frequent_ids

if __name__ == "__main__":

    start_time = time.time()

    print("RUNNING APRIORI ALGORITHM")
    result_min_sup_0 = apriori(hash_table, min_sup_arr[0])

    count_result = {0:{}, 1:{}, 2:{}, 3:{}, 4:{}}

    for i, min_sup in enumerate(min_sup_arr):
        for k in result_min_sup_0:
            if i == 0:
                count_result[i][k] = len(result_min_sup_0[k])
            else:
                count_result[i][k] = len(delete_below_min_sup(result_min_sup_0[k], min_sup))

    # printing the result based on the question requirement
    for i in count_result:
        print(f"min_freq = {min_freqs[i]} results:")
        total = 0
        for k in count_result[i]:
            if count_result[i][k] > 0:
                print(f"Number of size-{k} frequent patterns= {count_result[i][k]}")
                total += count_result[i][k]
        print(f"Total number of frequent patterns = {total}")
        print("=================================================")

#### Run the code below to run the apriori algorithm for each min_freqs (calling it 5 times) ####

    # result = {}
    # for i, min_sup in enumerate(min_sup_arr):
    #     print(f"running for {min_freqs[i]}")
    #     result[min_freqs[i]] = apriori(hash_table, min_sup)

    # # printing the result based on the question requirement
    # for min_freq in result:
    #     print(f"min_freq = {min_freq} results:")
    #     total = 0
    #     for k in result[min_freq]:
    #         if len(result[min_freq][k]) > 0:
    #             print(f"Number of size-{k} frequent patterns= {len(result[min_freq][k])}")
    #             total += len(result[min_freq][k])
    #     print(f"Total number of frequent patterns = {total}")
    #     print("=================================================")
    
    duration = time.time() - start_time
    print(f"Total Duration: {duration: 4f} s")