class SpellingResult:
    numCorrect = 0
    numTotal = 0
    marked_err = 0
    marked_noerr = 0
    unmarked_err = 0
    unmarked_noerr = 0
    
    def __init__(self):
        self.numCorrect = 0
        self.numTotal = 0
        
        self.marked_err = 0
        self.marked_noerr = 0
        self.unmarked_err = 0
        self.unmarked_noerr = 0
    
#    def __init__(self, correct, total):
#        self.numCorrect = correct
#        self.numTotal = total

    def __init__(self, marked_err1, marked_noerr1, unmarked_err1, unmarked_noerr1, correct, total):
        self.marked_err = marked_err1
        self.marked_noerr = marked_noerr1
        self.unmarked_err = unmarked_err1
        self.unmarked_noerr = unmarked_noerr1
        
        self.numCorrect = correct
        self.numTotal = total
          
    def getAccuracy(self):
#        tmp = self.marked_err + self.marked_noerr + self.unmarked_err + self.unmarked_noerr
#        if tmp > 0:
#            return float(self.marked_err + self.unmarked_noerr) / tmp
#        elif self.numTotal == 0:
        if self.numTotal == 0:
            return 0.0
        else:
            return float(self.numCorrect) / self.numTotal

    def getPrecision(self):
        tmp = self.marked_err + self.marked_noerr
        if tmp > 0:
            return float(self.marked_err) / tmp
        else:
            return 0.0

    def getRecall(self):
        tmp = self.marked_err + self.unmarked_err
        if tmp > 0:
            return float(self.marked_err) / tmp
        else:
            return 0.0

    def getF1(self):
        tmp = self.marked_err*2 + self.marked_noerr + self.unmarked_err
        if tmp > 0:
            return float(self.marked_err*2) / tmp
        else:
            return 0.0
        
    def __str__(self):
        tmp = self.marked_err + self.marked_noerr + self.unmarked_err + self.unmarked_noerr
        if tmp > 0:
            return 'Correct: %d Total: %d Accuracy: %f \nPrecision: %f Recall: %f F1: %f' \
                % (self.numCorrect, self.numTotal, self.getAccuracy(), \
                   self.getPrecision(), self.getRecall(), self.getF1())
        return 'correct: %d total: %d accuracy: %f' % (self.numCorrect, self.numTotal, self.getAccuracy())
