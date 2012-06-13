from Datum import Datum
from Sentence import Sentence

import enchant

class HolbrookCorpus:
    corpus = [] # list of sentences
    
    def __init__(self, filename=None):
        if filename:
            self.read_holbrook(filename)
        else:
            self.corpus = []
        
    
    def processLine(self, line):
        self.dict = enchant.Dict('en')
        line = line.strip()
        #line = line.lower() 
        line = line.replace('"','') 
        line = line.replace(',', '')
        line = line.replace('.', ' . ') 
        line = line.replace('!', ' . ') 
        line = line.replace('?', ' ? ')
        #line = line.replace("'",'') 
        line = line.replace(":",'') 
        line = line.replace(";",' , ') 
        line = line.replace("  ",' ')
        if line == '':
            return None
        processed_tokens = Sentence() 
        processed_tokens.append(Datum("<s>")) #start symbol
        tokens = line.split()
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token == '':
                i += 1
                continue
            if not token.islower():
                if self.dict.check(token.lower()):
                    token = token.lower()
            if token == '<ERR':
                try:
                    if tokens[i+3] == '</ERR>':
                        targ = tokens[i+1]
                        targ_splits = targ.split('=')
                        correct_token = targ_splits[1][:-1] # chop off the trailing '>'
                        incorrect_token = tokens[i+2]
                    else:
                        #either targ or error has more than one word
                        end = i + tokens[i:].index('</ERR>') - 1
                        for j in range(i, end):
                            if tokens[j].endswith('>'):
                                break
                            
                        targ = tokens[i+1]
                        targ_splits = targ.split('=')
                        if i+1 == j:# one word in targ
                            correct_token = targ_splits[1][:-1] # chop off the trailing '>'
                        else:# more than one word in targ
                            correct_token = targ_splits[1]
                            if (i+2) <= (j-1):
                                for k in range(i+2, j):
                                    correct_token = correct_token + ' ' + tokens[k]
                            correct_token = correct_token + ' ' + tokens[j][:-1] # chop off the trailing '>'
                        
                        incorrect_token = tokens[j+1]
                        if (j+2) <= end:
                            for k in range(j+2, end+1):
                                incorrect_token = incorrect_token + ' ' + tokens[k]
                except IndexError:
                    print tokens
                    #raise RuntimeError
                    return None
#                    processed_tokens.append(Datum("</s>"))
#                    return processed_tokens

#                correct_token_splits = correct_token.split()
#                if len(correct_token_splits) > 2: # targ with multiple words
#                    #print 'targ with multiple words: "%s"' % targ
#                    for correct_word in correct_token_splits:
#                        processed_tokens.append(Datum(correct_word))
#                elif tokens[i+3] != '</ERR>':
#                    processed_tokens.append(Datum(correct_token))
#                else:
#                    incorrect_token = tokens[i+2]
#                    processed_tokens.append(Datum(correct_token, incorrect_token)) 

                processed_tokens.append(Datum(correct_token, incorrect_token))         
                i += tokens[i:].index('</ERR>') + 1 # update index
            else: # regular word
                processed_tokens.append(Datum(token))
                i += 1
        processed_tokens.append(Datum("</s>"))
        return processed_tokens
    
    def read_holbrook(self, filename):
        """Read in holbrook data, returns a list (sentence) of list(words) of lists(alternatives).
           The first item in each word list is the correct word."""
        f = open(filename)
        self.corpus = []
        for line in f:
            sentence = self.processLine(line)      
            if sentence:
                self.corpus.append(sentence)
    
    def generateTestCasesAllErr(self):
        """Returns a list of sentences with all error"""
        testCases = [] # list of Sentences
        for sentence in self.corpus:
            cleanSentence = sentence.cleanSentence()
            testSentence = Sentence(cleanSentence)
            for i in range(0, len(sentence)):
                datum_i = sentence.get(i)
                if datum_i.hasError():
                    testSentence.put(i, datum_i)
            testCases.append(testSentence)
        return testCases    
            
    def generateTestCases(self):  
        """Returns a list of sentences with exactly 1 elligible spelling error"""
        testCases = [] # list of Sentences
        for sentence in self.corpus:
            cleanSentence = sentence.cleanSentence()
            for i in range(0, len(sentence)):
                datum_i = sentence.get(i)
                if datum_i.hasError() and datum_i.isValidTest():
                #if datum_i.hasError():
                    testSentence = Sentence(cleanSentence)
                    testSentence.put(i, datum_i)
                    testCases.append(testSentence)
        return testCases
    
    
    def slurpString(self, contents):
        """Reads a clean corpus from string instead of file. Used for submission."""
        lines = contents.split('\n')
        self.corpus = []
        for line in lines:
            sentence = self.processLine(line)
            if sentence:
                self.corpus.append(sentence)
    
    def __str__(self):
        str_list = []
        for sentence in self.corpus:
            str_list.append(str(sentence))
        return '\n'.join(str_list)   
    