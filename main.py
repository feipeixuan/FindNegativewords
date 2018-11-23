#!/usr/bin/python
# --coding=utf8
# -*- coding: utf-8 -*-


"""
# @Time    : 2018/11/21 下午6:24
# @Author  : feipeixuan
# @File    : main
# @Software: PyCharm
"""

from util.TextUtil import TextUtil
import io
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def main():
    filename="data/负样本评论.txt"
    keywords=TextUtil.generateKeyWords(filename)
    keywords=set(keywords)
    print(len(keywords))


main()