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
        inf_input =  open(filename)
        
        self.inflectDict = {}
        self.invertIndex = {}
        for line in inf_input:
            word = line.split('\t')
            wordLen = len(word)
            if wordLen == 2:
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
    
    testWord = 'thieves'
    print "Check inDict: ", myInf.inDict(testWord)
    print "Check getHead: ", myInf.getHead(testWord)
    print "Check getInfSet: ", myInf.getInfSet(testWord)
    
if __name__ == '__main__': 
    demo()