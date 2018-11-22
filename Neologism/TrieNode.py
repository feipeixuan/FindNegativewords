#!/usr/bin/python
# coding=utf-8
"""
# @Time    : 2018/11/22 上午11:58
# @Author  : feipeixuan
# @File    : TrieNode
# @Software: PyCharm
"""


# 单个节点
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

    # 查找一个关键词
    def search(self, word):
        node = self.root
        for letter in word:
            node = node.data.get(letter)
            if not node:
                return False
        return True

    # 判断是否有这个前缀的字典
    def starts_with(self, prefix):
        node = self.root
        for letter in prefix:
            node = node.data.get(letter)
            if not node:
                return False
        return True

    def get_start(self, prefix):
        def _get_key(pre, pre_node):
            words_list = []
            if pre_node.is_word:
                words_list.append(pre)
            for x in pre_node.data.keys():
                words_list.extend(_get_key(pre + str(x), pre_node.data.get(x)))
            return words_list

        words = []
        if not self.starts_with(prefix):
            return words
        if self.search(prefix):
            words.append(prefix)
            return words
        node = self.root
        for letter in prefix:
            node = node.data.get(letter)
        return _get_key(prefix, node)


