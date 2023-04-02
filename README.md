# Efficient Apriori Algorithm for Large Dataset

## Prerequisites

- pandas
- numpy
- itertools
- collections

## Getting Started

List of python scripts that can be run:
-	1_reversed_hash_table.py
-	2_hash_table_dict.py
-	3_trie.py

1. Make sure that trans.txt is in the same folder.
2. In the terminal and directory of the folder, (e.g. "python ./2_hash_table_dict.py")
3. All the code are designed to call the apriori algorithm 1 time. If want to test it to call the apriori function each time for 5 min_freqs value, run the code commented below of the current one.

## Method and Results

*Note: Since the min_freqs values are increasing, we can use the result from the first run of the apriori algorithm with min_freqs = 0.0001 and then just delete size-k itemsets using the other min_freqs value. The result will be the same with running the apriori algorithm for each min_freqs. So, we can remove the repetition of running apriori algorithm to only once. So the duration of my codes are only running calling the apriori algorithm once and then delete the frequent itemsets that do not meet the minimum support. I tested both approaches (single and 5 times run) and the results are attached.

1. Reversed Hash Table
-	Create a reversed hash table (dictionary) with each item as keys and transaction ids where the item appears as values.
-	Counting step: count number of intersection to find the transactions that contain all items in the set.
Total Duration:  95.233076 s (single run)
Total Duration: 196.383979 s (5 times run)

2. Normal Index Hash Table
-	Hash table keys: transaction id, values: items
-	Utilizing python dictionary property to get the key value of k-itemset in O(1) time.
-	Counting step: for items in each transaction, generate k-item subset combinations and add count to the corresponding itemset if appear in the dictionary keys.
-	Reducing the time of iterating each transaction by only iterating through transactions who have minimum k-items
Total Duration: 47.115571 s (single run)
Total Duration: 97.803752 s (5 times run)

3. Trie (Prefix Tree)
-	Implement Trie data structure to store all the transactions.
-	Add pruning method, so that inside the trie, infrequent items (below min_sup) are pruned and the tree will be much smaller in size that will make the process more efficient.
-	Counting step: generates k-item subset combinations from a given list of ids in the transaction, then checking every subset to the candidate itemsets to see if they are frequent. After that, traversing the trie and count how many transactions that contain a given subset.
Total Duration: 57.711648 s (single run)
Total Duration: 131.496428 s (5 times run)

## Outputs

> The result should output this:
-------------------------------------------------
    min_freq = 0.0001 results:
    Number of size-1 frequent patterns= 731
    Number of size-2 frequent patterns= 8200
    Number of size-3 frequent patterns= 8201
    Number of size-4 frequent patterns= 1828
    Number of size-5 frequent patterns= 100
    Total number of frequent patterns = 19060
    =================================================
    min_freq = 0.0002 results:
    Number of size-1 frequent patterns= 592
    Number of size-2 frequent patterns= 4564
    Number of size-3 frequent patterns= 2831
    Number of size-4 frequent patterns= 359
    Number of size-5 frequent patterns= 5
    Total number of frequent patterns = 8351
    =================================================
    min_freq = 0.0003 results:
    Number of size-1 frequent patterns= 527
    Number of size-2 frequent patterns= 3080
    Number of size-3 frequent patterns= 1384
    Number of size-4 frequent patterns= 134
    Number of size-5 frequent patterns= 1
    Total number of frequent patterns = 5126
    =================================================
    min_freq = 0.0004 results:
    Number of size-1 frequent patterns= 474
    Number of size-2 frequent patterns= 2258
    Number of size-3 frequent patterns= 814
    Number of size-4 frequent patterns= 50
    Total number of frequent patterns = 3596
    =================================================
    min_freq = 0.0005 results:
    Number of size-1 frequent patterns= 440
    Number of size-2 frequent patterns= 1747
    Number of size-3 frequent patterns= 525
    Number of size-4 frequent patterns= 27
    Total number of frequent patterns = 2739
    =================================================
    Total Duration:  47.115571 s