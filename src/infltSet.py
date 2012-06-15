'''
Created on Jun 8, 2012

@author: Tony
'''
class inflectionSet:
    
    def __init__(self, filename=None):
        if filename == None:
            filename = '../data/inflect.txt'
        conf_input =  open(filename)
        
        self.inflect = {}
        
        for line in conf_input:
            line = line.strip()
            word = line.split('\t')
            head_word = word[0].split('/')
            head_word = head_word[0]
            next_word = word[1].split('/')
            next_word = next_word[0]
            
            if head_word == next_word:
                pass
            else:
                try:
                    self.inflect[head_word].add(next_word)
                except KeyError:
                    self.inflect[head_word] = set([])
                    self.inflect[head_word].add(next_word)

    def isHeadWord(self, head_word):
        return self.inflect.has_key(head_word)
        
    def getWordSet(self, head_word):
        try:
            return self.inflect[head_word]
        except KeyError:
            return set([])
        
def demo():
    myInflt = inflectionSet()
    
    test_word = 'lie'
    print "Check", test_word, ": ", myInflt.isHeadWord(test_word)
    print "Check", test_word, ": ", myInflt.getWordSet(test_word)
    
if __name__ == '__main__': 
    demo()