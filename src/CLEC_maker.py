'''
Created on Jun 8, 2012

@author: Tony
'''
import time

filename = '../data/CLEC_corpus_raw.dat'
cps_input =  open(filename, 'r')

filename = '../data/CLEC_corpus.dat'
output =  open(filename, 'w')

count = 0.0
for line in cps_input:
    line = line.strip()
    if line == '':
        continue
    line = line.replace('[',' [') 
    line = line.replace(']','] ') 
    line = line.replace('  ',' ') 
    line = line.replace('  ',' ')
    sent = line + '\n'
    output.write(sent)
    count += 1
    if count % 300 == 0:
        print "Executed  %d, %.02f%% completed , Time:%s" % (count, count/300, time.ctime())
