import math, collections

class CustomLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.unigramCounts = collections.defaultdict(int)
    self.bigramCounts = collections.defaultdict(int)
    self.smoothedUnigramCounts = collections.defaultdict(int)
    self.smoothedBigramCounts = collections.defaultdict(int)
    self.continuationCounts = collections.defaultdict(int)
    self.preContinuationCounts = collections.defaultdict(int)
    self.total = 0
    self.smoothedTotal = 0
    self.totalContinuation = 0
    self.train(corpus)


  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    for sentence in corpus.corpus:
      pre = ''  
      for datum in sentence.data:  
        token = datum.word
        if pre == '':
            self.unigramCounts[token] = self.unigramCounts[token] + 1
            self.smoothedUnigramCounts[token] = self.smoothedUnigramCounts[token] + 1
            self.total += 1
            self.smoothedTotal += 1
            pre = token
        else:
            self.unigramCounts[token] = self.unigramCounts[token] + 1
            self.smoothedUnigramCounts[token] = self.smoothedUnigramCounts[token] + 1
            self.total += 1
            self.smoothedTotal += 1
            bitoken = (pre, token)
            self.bigramCounts[bitoken] = self.bigramCounts[bitoken] + 1
            self.smoothedBigramCounts[bitoken] = self.smoothedBigramCounts[bitoken] + 1
            pre = token
            
    wordlist = self.smoothedUnigramCounts.keys()  # bigram +1 smooth
    for word in wordlist:
        for wordR in wordlist:
            bitoken = (word, wordR)
            self.smoothedBigramCounts[bitoken] = self.smoothedBigramCounts[bitoken] + 1
            self.smoothedUnigramCounts[word] = self.smoothedUnigramCounts[word] + 1
            self.smoothedUnigramCounts[wordR] = self.smoothedUnigramCounts[wordR] + 1
            self.total += 2

    wordlist = self.bigramCounts.keys()  # count continuation
    for word in wordlist:
        self.preContinuationCounts[word[0]] = self.preContinuationCounts[word[0]] + 1
        self.continuationCounts[word[1]] = self.continuationCounts[word[1]] + 1
        self.totalContinuation += 1 


  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    num_countBi = 0
    num_countUni = 0
    
    delta = 0.75
    score = 0.0 
    score1 = 0.0
    score2 = 0.0
    pre = ''
    for token in sentence:
        if pre == '':
            pre = token
        else:  
            bitoken = (pre, token)
            countBi = self.bigramCounts[bitoken]
            countPre = self.unigramCounts[pre]
            countUni = self.unigramCounts[token]
            continuation = self.continuationCounts[token]
            preCont = self.preContinuationCounts[pre]
            
#            if countPre > 0:
#                if countBi <= 0:
#                    countBi = 1
#                afterCountBi = countBi - delta
#                if afterCountBi < 0:
#                    afterCountBi = 0
#                if continuation <= 0:
#                    continuation = 1
#                theLambda = delta * preCont * continuation / self.totalContinuation
#                afterCount = afterCountBi + theLambda
#                score += math.log(afterCount)
#                score -= math.log(countPre)
            if countBi > 0:
                afterCountBi = countBi - delta
                if afterCountBi < 0:
                    afterCountBi = 0
                if continuation <= 0:
                    continuation = 1
                theLambda = delta * preCont * continuation / self.totalContinuation
                afterCount = afterCountBi + theLambda
                score += math.log(afterCount)
                score -= math.log(countPre)
            else:
                countBi = self.smoothedBigramCounts[bitoken]
                countPre = self.smoothedUnigramCounts[pre]
                if countBi > 0 and countPre > 0:
                    score += math.log(countBi)
                    score -= math.log(countPre)
                elif countBi > 0:
                    score += math.log(countBi)
                    score -= math.log(self.total + 1)
                elif countPre > 0:
                    score += math.log(1)
                    score -= math.log(countPre)
                else:
                    score += math.log(1)
                    score -= math.log(self.total + 1)
                    
            pre = token
                
    return score

  def entropy(self, sentence):
    return -self.score(sentence)