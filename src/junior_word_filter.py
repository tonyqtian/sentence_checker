#!/usr/bin/python 
#-*- encoding: utf-8 -*- 
'''
Created on 2012-8-10

@author: tianqiu
'''

word_set = set([])
# n 名词  v 动词  adj形容词   adv 副词   prep介词  conj连词 phr.短语   num数词
file_read = open('../data/basic_words_tmp.txt', 'r')
file_write = open('../data/basic_words_out.txt', 'w')
for line in file_read:
    word = line.strip()
    if word.isalpha():
        word_set.add(word)
    else:
        print word

wordList = sorted(list(word_set))
for w in wordList:
    file_write.write(w)
    file_write.write('\n')
print 'Finished.'