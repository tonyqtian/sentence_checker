'''
Created on Jun 8, 2012

@author: Tony
'''
import time
import MySQLdb
connection = MySQLdb.connect(host = "192.168.1.96", port = 3306, \
                      user = "root", passwd = "123qwe")
connection.select_db("corpus")
cursor = connection.cursor()

print "Fetching data..."
cursor.execute("""select contents from clec_doc """)
data = cursor.fetchall()
print "Fetch OK. Starting..."
connection.close()

filename = '../data/CLEC_corpus_raw.dat'
cps_output =  open(filename, 'w')

import nltk.data
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
from replacer import RegexpReplacer
myReplacer = RegexpReplacer()

count = 0.0
for page in data:
    for block in page:
        lines = block.split('\r\n')
        for line in lines:
            line = line.strip()
            if line.startswith('<ST'):
                pass
            else:
                # do some minor change then tokenize
                line0 = myReplacer.replace(line)
                sentences = tokenizer.tokenize(line0)
                for sent in sentences:
                    sent = sent.strip()
                    sent = sent + '\n'
                    cps_output.write(sent)
                    count += 1
                    if count % 300 == 0:
                        print "Executed  %d, %.02f%% completed , Time:%s" % (count, count/300, time.ctime())

cps_output.close()
print "Finished."