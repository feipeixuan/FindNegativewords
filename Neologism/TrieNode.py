#!/usr/bin/python
# coding=utf-8
"""
# @Time    : 2018/11/22 上午11:58
# @Author  : feipeixuan
# @File    : TrieNode
# @Software: PyCharm
"""


# 单个节点（子元素+频数)
class TrieNode(object):
    def __init__(self):
        self.data = {}
        self.frequency = 0


# 字典树
class Trie(object):

    def __init__(self):
        self.root = TrieNode()

    # 插入一个关键词
    def insert(self, word):
        node = self.root
        # 遍历每个字
        for letter in word:
            child = node.data.get(letter)
            if not child:
                node.data[letter] = TrieNode()
            node = node.data[letter]
            node.frequency += 1

    # 判断是否有这个前缀的字典
    def starts_with(self, prefix):
        node = self.root
        for letter in prefix:
            node = node.data.get(letter)
            if not node:
                return False
        return True

    # 得到以此为前缀的关键字
    def get_starts_with(self,prefix):
        words=[]
        if not self.starts_with(prefix):
            return words
        else:
            node=self.root
            for letter in prefix:
                node = node.data.get(letter)
            return node

# trie=Trie()
# trie.insert(["11222","222"])
# trie.insert(["333","222"])
# print(trie.get_starts_with(["333"]))


