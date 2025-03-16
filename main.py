import re
import json

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
    
    def auto_correct(self, word):
        result = self.search_with_prefix()
        
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

print(input)
