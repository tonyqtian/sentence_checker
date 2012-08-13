'''
Created on 2012-8-2

@author: tianqiu
'''

class inflectionSet(object):
    '''
    classdocs
    '''


    def __init__(self, filename= '../data/inflect.txt'):
        '''
        Constructor
        '''
        inf_input =  open(filename, 'r')
        safe_input = open('../data/basic_words_list.txt', 'r')
        self.safe_set = set([])
        for wd in safe_input:
            wd = wd.strip()
            self.safe_set.add(wd)
            
        self.inflectDict = {}
        self.invertIndex = {}
        for line in inf_input:
            word = line.split('\t')
            if len(word) == 2:
                former, later = word
                headWord, dummy = former.split('/')
                tailWord, dummy = later.split('/')
                try:
                    self.inflectDict[headWord].add(tailWord)
                except KeyError:
                    self.inflectDict[headWord] = set([])
                    self.inflectDict[headWord].add(tailWord)
                try:
                    self.invertIndex[tailWord].add(headWord)
                except KeyError:
                    self.invertIndex[tailWord] = set([])
                    self.invertIndex[tailWord].add(headWord)                
            else:
                print "Incorrect input form..."
        
        # remove uni-key in inflection dict
        keyList = self.inflectDict.keys()
        for word in keyList:
            if len(self.inflectDict[word]) == 1:
                for w in self.inflectDict[word]:
                    if len(self.invertIndex[w]) == 1:
                        del self.invertIndex[w]
                    else:
                        self.invertIndex[w].remove(word)
                del self.inflectDict[word]

        # remove head key in invert index
        keyList = self.inflectDict.keys()
        for word in keyList:
            if self.invertIndex.has_key(word):
                del self.invertIndex[word]
                
#        # test: show multi-invert index
#        for word in self.invertIndex:
#            if len(self.invertIndex[word]) > 1:
#                print word , ": " , self.invertIndex[word]

    def inDict(self, word):
        if self.inflectDict.has_key(word):
            return True
        elif self.invertIndex.has_key(word):
            return True
        else:
            return False
        
    def inDictSafe(self, word):
        if word in self.safe_set:
            return True
        else:
            return False
        
    def getHead(self, word):
        if self.inflectDict.has_key(word):
            return word
        elif self.invertIndex.has_key(word):
            if len(self.invertIndex[word]) == 1:
                for w in self.invertIndex[word]:
                    return w
            else:
                return self.invertIndex[word]
        else:
            return ''
        
    def getInfSet(self, word):
        if self.inflectDict.has_key(word):
            return self.inflectDict[word]
        elif self.invertIndex.has_key(word):
            if len(self.invertIndex[word]) == 1:
                for w in self.invertIndex[word]:
                    return self.inflectDict[w]
            else:
                listSet = set([])
                for w in self.invertIndex[word]:
                    listSet = listSet.union(self.inflectDict[w])
                return listSet
        else:
            return set([])
        
def demo():
    myInf = inflectionSet()
    
#    safe_input = open('../data/basic_words_list.txt', 'r')
#    output = open('../data/basic_inflection_list.txt', 'w')
#    for wd in safe_input:
#        wd = wd.strip()
#        inf_list = myInf.getInfSet(wd)
#        if len(inf_list):
#            line = wd + '\t'
#            for w in inf_list:
#                if not w == wd:
#                    line = line + w + ','
#            line = line.strip(',')
#            line = line + '\n'
#            output.write(line) 
       
    testWord = 'thieves'
    print "Check inDict: ", myInf.inDict(testWord)
    print "Check getHead: ", myInf.getHead(testWord)
    print "Check getInfSet: ", myInf.getInfSet(testWord)
    
if __name__ == '__main__': 
    demo()