'''
Created on 2012-8-11

@author: tianqiu
'''

class inflectionBasicSet(object):
    '''
    classdocs
    '''
    
    def __init__(self, filename= '../data/basic_inflection_list.txt'):
        '''
        Constructor
        '''
        inf_input =  open(filename, 'r')
        self.inflectDict = {}
        
        for line in inf_input:
            if line.startswith('#'):
                continue
            line = line.strip()
            word = line.split('\t')
            if len(word) == 2:
                headWord, later = word
                wd = later.split(',')
                for tailWord in wd:
                    try:
                        self.inflectDict[headWord].add(tailWord)
                    except KeyError:
                        self.inflectDict[headWord] = set([])
                        self.inflectDict[headWord].add(tailWord)

    def inDict(self, word):
        if self.inflectDict.has_key(word):
            return True
        else:
            return False
        
    def getHead(self, word):
        if self.inflectDict.has_key(word):
            return word
        else:
            return ''
        
    def getInfSet(self, word):
        if self.inflectDict.has_key(word):
            return self.inflectDict[word]
        else:
            return set([])

def demo():
    myInf = inflectionBasicSet()
    
    testWord = 'practise'
    print "Check inDict: ", myInf.inDict(testWord)
    print "Check getHead: ", myInf.getHead(testWord)
    print "Check getInfSet: ", myInf.getInfSet(testWord)
    
if __name__ == '__main__': 
    demo()