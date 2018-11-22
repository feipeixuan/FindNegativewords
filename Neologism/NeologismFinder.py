#!/usr/bin/python
# coding=utf-8
"""
# @Time    : 2018/11/22 上午10:38
# @Author  : feipeixuan
# @File    : NeologismFinder
# @Software: PyCharm
"""

from config.TextUtil import TextUtil
import io
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# 基于互信息和信息熵的新词发现器
class NeologismFinder:

    # 构建关键词词典
    def constructVocablist(self,negativeCommentFile):
        keywords = TextUtil.generateKeyWords(negativeCommentFile)
        self.vocablist= set(keywords)














