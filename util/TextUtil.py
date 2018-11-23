#!/usr/bin/python
# --coding=utf8
# -*- coding: utf-8 -*-

import re
from enum import Enum
import io
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


# 字符类型
class CharType(Enum):
    chinese = 1
    number = 2
    english = 3

# 转码utf-8转unicode
def strToUnicode(value):
    value=value.decode("utf-8")
    value=value.replace(",","").replace(" ","").replace("，","")
    return value


# 文本处理工具类
class TextUtil:

    # 得到停用词列表
    @staticmethod
    def getStopWords(filename):
        fo = io.open(filename, "r", encoding="utf-8")
        stopwords = set()

        while True:
            line = fo.readline()
            line = line.decode("utf-8")
            if not line:
                break
            stopword = line.replace("\n", "")
            stopword=tuple(stopword)
            stopwords.add(stopword)

        fo.close()
        stopword = " ".decode("utf-8")
        stopwords.add(tuple(stopword))

        return stopwords

    # 输出字符的类型
    @staticmethod
    def getCharType(ch):
        ch = ch.lower()
        if u'\u4e00' <= ch <= u'\u9fff':
            return CharType.chinese
        elif '0' <= ch <= '9':
            return CharType.number
        elif 'a' <= ch <= 'z':
            return CharType.english

    # 拆分文本从而得到词
    # 1.汉字单字 2.数字连续组合 3.字符连续组合
    @staticmethod
    def splitText(text):

        words = []
        lastType = CharType.chinese
        lastIndex = 0

        for i in range(len(text)):
            ch = text[i]
            currentType = TextUtil.getCharType(ch)
            if (currentType == CharType.chinese):
                words.append(strToUnicode(str(ch)))

            if (currentType != lastType):
                if (lastType != CharType.chinese):
                    words.append(strToUnicode(text[lastIndex:i]))
                lastType = currentType
                lastIndex = i

            if ((i + 1) >= len(text) and currentType != CharType.chinese):
                words.append(strToUnicode(text[lastIndex:]))

        return words

    # 利用正则表达式过滤无效文本，只保留数字+汉字+英文+常用特殊字符，其他全部去掉
    @staticmethod
    def cleanText(text):
        cop = re.compile(u"[^\u4e00-\u9fa5^\s\,\，^a-z^A-Z^0-9]")
        return cop.sub("", text)

    # 过滤大于20个长度的文本
    @staticmethod
    def filterText(text):
        if len(text)>20:
            return True
        else:
            return False

    # 过滤一些关键字
    @staticmethod
    def filterKeyWord(keyword):
        for stopword in TextUtil.stopwords:
            if stopword in keyword:
                return True
        return False


    # 读出多行文本,只是进行了最基本的过滤操作
    @staticmethod
    def getTexts(filename):
        fo = io.open(filename, "r", encoding="utf-8")
        lines = fo.readlines();
        texts = []
        for line in lines:
            line = line.decode("utf-8")
            strs = line.split(":")
            if len(strs) < 2:
                continue
            else:
                #TODO 暂时没有进行去重
                text = line[len(strs[0]) + 1:]
                text = TextUtil.cleanText(text)
                if TextUtil.filterText(text):
                    continue
                texts.append(text)
        return texts

    # 产生Ngram词
    @staticmethod
    def generateNgram(text, n):
        keywords = []
        for i in range(2, n + 1):
            for j in range(0, len(text) - i):
                keyword=text[j:j + i]
                # if TextUtil.filterKeyWord(keyword):
                #     continue
                keywords.append(keyword)
        return keywords

    # 产生全部的关键字
    @staticmethod
    def generateKeyWords(filename):
        # stopwords=TextUtil.getStopWords("../config/stopword.txt")
        # TextUtil.stopwords=stopwords
        texts = TextUtil.getTexts(filename)
        keywords = []
        for i in range(len(texts)):
            text = TextUtil.splitText(texts[i])
            keywords.extend(TextUtil.generateNgram(text, 7))

        #TODO 删除包含空格，逗号的关键字
        return keywords

# keywords=TextUtil.generateKeyWords("../data/负样本评论.txt")
# print(keywords)