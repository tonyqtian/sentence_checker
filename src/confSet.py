'''
Created on May 15, 2012

@author: Tony
'''
class confusionSet:
    
    def __init__(self, filename=None):
        if filename == None:
            filename = '../data/confsets.txt'
        conf_input =  open(filename)
        
        self.distinct = {}
        self.overlap = {}
        self.match = {}
        
        for line in conf_input:
            word = line.split('|')
            wordLen = len(word)
            flag = word[wordLen - 1]
            
            if flag == '0\n':
                self.distinct[word[0]] = []
                for i in range(1,wordLen -1):
                    self.distinct[word[0]].append(word[i])
                    
            elif flag == '1\n':
                self.match[word[0]] = []
                for i in range(1,wordLen -1):
                    self.match[word[0]].append(word[i])
                    
            elif flag == '2\n':
                self.overlap[word[0]] = []
                for i in range(1,wordLen -1):
                    self.overlap[word[0]].append(word[i])
                    
    
    def isDistinct(self, word):
        if self.distinct.has_key(word):
            return True
        else:
            return False
    
    def isMatch(self, word):
        if self.match.has_key(word):
            return True
        else:
            return False
        
    def isOverlap(self, word):
        if self.overlap.has_key(word):
            return True
        else:
            return False
        
    def getDistinctList(self, word):
        if self.distinct.has_key(word):
            return self.distinct[word]
        else:
            return []

    def getMatchList(self, word):
        if self.match.has_key(word):
            return self.match[word]
        else:
            return []

    def getOverlapList(self, word):
        if self.overlap.has_key(word):
            return self.overlap[word]
        else:
            return []
        
def demo():
    myConf = confusionSet()
    
    print "Check bellow: ", myConf.isDistinct('bellow')
    print "Check bellow: ", myConf.getDistinctList('bellow')
    
if __name__ == '__main__': 
    demo()