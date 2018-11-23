#!/usr/bin/python
# coding=utf-8
"""
# @Time    : 2018/11/22 上午10:38
# @Author  : feipeixuan
# @File    : NeologismFinder
# @Software: PyCharm
"""


import io
import math
import sys

reload(sys)
sys.setdefaultencoding('utf8')
from util.TextUtil import TextUtil
from neologism.TrieNode import Trie, TrieNode


# 基于互信息和信息熵的新词发现器
class NeologismFinder:

    def __init__(self):
        self.prefixTrie = Trie();
        self.suffixTrie = Trie();
        self.keywords = set()
        # 一共多少个关键字
        self.countKeywords = 0
        # 每个字出现的频数
        self.characters = {}

    # 构建关键词词典
    def constrcutTrie(self, filename):
        keywords = TextUtil.generateKeyWords(filename)
        for keyword in keywords:
            self.keywords.add(tuple(keyword))
            self.prefixTrie.insert(keyword)
            keyword.reverse()
            self.suffixTrie.insert(keyword)
            self.countKeywords += 1
            for character in keyword:
                keyword = set(keyword)
                if character not in self.characters:
                    self.characters[character] = 0
                self.characters[character] += 1

    # 利用左右信息熵和互信息得到分数
    def computeScore(self):
        scores = {}
        for keyword in self.keywords:
            keyword = list(keyword)

            keywordFrequency = self.prefixTrie.get_starts_with(keyword).frequency
            if keywordFrequency <= 20:
                continue

            # 计算互信息
            keywordProb = keywordFrequency * 1.0 / self.countKeywords
            sumProb = 1.0

            for character in keyword:
                sumProb *= self.characters[character] * 1.0 / self.countKeywords

            mScore = keywordProb * math.log(keywordProb / sumProb, 2)

            # 计算左右信息熵，取较小值

            rChild = self.prefixTrie.get_starts_with(keyword)
            elScore = 0
            if len(rChild.data) != 0:
                frequency = 0
                characters = rChild.data
                for character in characters:
                    frequency += characters[character].frequency
                for character in characters:
                    prob = characters[character].frequency * 1.0 / frequency
                elScore += prob * math.log(prob, 2)

            keyword.reverse()
            lChild = self.suffixTrie.get_starts_with(keyword)
            erScore = 0
            if len(lChild.data) != 0:
                frequency = 0
                characters = lChild.data
                for character in characters:
                    frequency += characters[character].frequency
                for character in characters:
                    prob = characters[character].frequency * 1.0 / frequency
                erScore += prob * math.log(prob, 2)

            eScore = max(elScore,erScore)
            score = mScore+eScore
            keyword.reverse()
            scores[score] = keyword

        # 按照分数排序
        items = scores.items()
        items.sort()
        return [value for key, value in items]

    # 产生有问题的词汇列表
    def generateNegativeKeyWords(self,keywords):
        negativeWords=[]
        stopwords = TextUtil.getStopWords("../util/stopword.txt")
        for keyword in keywords:
            flag = True
            for stopword in stopwords:
                stopword = set(stopword)
                if stopword.issubset(keyword):
                    flag = False
                    break
            if not flag:
                continue
            for negativeWord in negativeWords:
                tmpNegativeWord=set(negativeWord)
                if tmpNegativeWord.issubset(keyword):
                    negativeWords.remove(negativeWord)
            negativeWords.append(keyword)

        return  negativeWords


def main():
    finder = NeologismFinder()
    finder.constrcutTrie("../data/负样本评论.txt")
    keywords = finder.computeScore()
    negativeKeyWords=finder.generateNegativeKeyWords(keywords)
    file_object = io.open('../data/结果文件.txt', 'w', encoding="utf-8")

    for negativeKeyWord in negativeKeyWords:
        line = ''.join(negativeKeyWord)
        if len(line) < 2 or len(negativeKeyWord)<2:
            continue
        file_object.write(line + " " + str(len(negativeKeyWord)) + "\n")

main()
