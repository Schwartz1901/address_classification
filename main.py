import re
import json
from collections import deque

import time
import os

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self, data = None):
        self.root = TrieNode()
        for d in data:
            self.insert(d)
       

    ## INSERT WORD INTO TRIE
    def insert(self, word):
        node = self.root
        for c in word:
            if c not in node.children:
                node.children[c] = TrieNode()
            node = node.children[c]
        node.is_end = True


    ## SEACH IF A WORD CAN BE REPRESENTED BY THE TRIE
    def in_trie(self, word):
        node = self.root
        for c in word:
            if c not in node.children:
                return False
            node = node.children[c]
        return node.is_end
    
    ## DFS UTILITY FUNCTION
    def _dfs(self, node, prefix, result):
        if (node.is_end):
            result.append(prefix)

        for char, child_node in node.children.items():
            self._dfs(child_node, prefix + char, result)


    # PRINT ALL WORD WITH THE PREFIX. WHEN PREFIX IS EMPTY, PRINT ALL WORDS REPRESENTED BY THE TRIE
    def search_with_prefix(self, prefix = ""):
        result = []
        node = self.root
        for p in prefix:
            if p not in node.children:
                print([])
                return
            node = node.children[p]
        self._dfs(node, prefix, result)
        return result
    
    def find_closest(self, target, max_distance=4):
        """Find the closest word in the Trie based on minimum edit distance using BFS."""
        queue = deque([(self.root, "", 0)])  # (node, current_word, edit_distance)
        closest_match = None
        min_distance = float("inf")

        while queue:
            node, current_word, _ = queue.popleft()

            if node.is_end:
                distance = self._edit_distance(target, current_word)
                if distance < min_distance:
                    min_distance = distance
                    closest_match = current_word

            if min_distance == 0:  # Exact match found, exit early
                return closest_match

            for char, next_node in node.children.items():
                queue.append((next_node, current_word + char, 0))

        return closest_match if min_distance <= max_distance else None

    def _edit_distance(self, s1, s2):
        """Compute the edit distance between two words using DP (iterative)."""
        len1, len2 = len(s1), len(s2)
        dp = [[0] * (len2 + 1) for _ in range(len1 + 1)]

        for i in range(len1 + 1):
            for j in range(len2 + 1):
                if i == 0:
                    dp[i][j] = j
                elif j == 0:
                    dp[i][j] = i
                elif s1[i - 1] == s2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

        return dp[len1][len2]
        
## Edit distance

# main
with open("all_raw.json", "r", encoding="utf-8") as f:
    test_list = json.load(f)

(input,output) = ([test["pred_no_correct"] for test in test_list], [test["address_info"] for test in test_list])

with open("list_district.txt", "r", encoding="utf-8") as f:
    list_district= [district.strip() for district in f]

with open("list_province.txt", "r", encoding="utf-8") as f:
    list_province= [province.strip() for province in f]

with open("list_ward.txt", "r", encoding="utf-8") as f:
    list_ward= [ward.strip() for ward in f]

trie = Trie(list_district)

# Measure Search Time for Test Cases
test_queries = ["Tân", "Hanoi", "Can Tho", "Sai Gon"]
for q in test_queries:
    start_time = os.times()
    print(trie.find_closest(q))
    end_time = os.times()
    print({(end_time[0] - start_time[0])})