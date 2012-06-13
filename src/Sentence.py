class Sentence:
    """Contains a list of Datums."""
    
    def __init__(self, sentence=[]):
        if(type(sentence) == type([])):
            self.data = list(sentence) 
        else:
            self.data = list(sentence.data)
    
    def getErrorSentence(self):
        """Returns a list of strings with the sentence containing all errors."""
        errorSentence = []
        for datum in self.data:
            if datum.hasError():
                errorSentence.append(datum.error)
            else:
                errorSentence.append(datum.word)
        return errorSentence
    
    def getCorrectSentence(self):
        """Returns a list of strings high lighting all corrections."""
        correctSentence = []
        for datum in self.data:
            if datum.hasError():
                correctSentence.append(datum.word)
            else:
                lenth = len(datum.word)
                dummy = '-'*lenth
                correctSentence.append(dummy)
        return correctSentence
    
    def getMyCorrection(self, candidate):
        """Returns a list of strings high lighting my corrections."""
        myCorrect = []
        i = 0
        for datum in self.data:
            try:
                if datum.hasError():
                    if datum.error == candidate[i]:
                        lenth = len(datum.word)
                        dummy = '-'*lenth
                        myCorrect.append(dummy)
                    else:
                        myCorrect.append(candidate[i])
                else:
                    if datum.word == candidate[i]:
                        lenth = len(datum.word)
                        dummy = '-'*lenth
                        myCorrect.append(dummy)
                    else:
                        myCorrect.append(candidate[i])
            except KeyError:
                myCorrect.append('<Err>')
            finally:
                i += 1
        return myCorrect
    
    def isCorrection(self, candidate):
        """Checks if a list of strings is a correction of this sentence."""
#        if len(self.data) != len(candidate):
#            return False
#        for i in range(0,len(self.data)):
#            if not candidate[i] == self.data[i].word:
#                return False
#        return True

        marked_err = 0
        marked_noerr = 0
        unmarked_err = 0
        unmarked_noerr = 0
        if len(self.data) != len(candidate):
            return (marked_err, marked_noerr, unmarked_err, unmarked_noerr)        
        for i in range(0,len(self.data)):
            if candidate[i] == self.data[i].word:
                if self.data[i].hasError():
                    marked_err += 1
                else:
                    unmarked_noerr += 1
            else:
                if self.data[i].hasError():
                    if candidate[i] == self.data[i].error:
                        unmarked_err += 1
                    else:
                        marked_noerr += 1
                else:
                    marked_noerr += 1
        return (marked_err, marked_noerr, unmarked_err, unmarked_noerr)
    
    def getErrorIndex(self):
        for i in range(0, len(self.data)):
            if self.data[i].hasError():
                return i
        return -1
    
    def len(self):
        return len(self.data)
    
    def get(self, i):
        return self.data[i]
    
    def put(self, i, val):
        self.data[i] = val
    
    def cleanSentence(self):
        """Returns a new sentence with all datum's having error removed."""
        sentence = Sentence()
        for datum in self.data:
            clean = datum.fixError()
            sentence.append(clean)
        return sentence
    
    def isEmpty(self):
        return len(self.data) == 0
    
    def append(self, item):    
        self.data.append(item)
    
    def __len__(self):
        return len(self.data)
    
    def __str__(self):
        str_list = []
        for datum in self.data:
            str_list.append(str(datum))
        return ' '.join(str_list)
