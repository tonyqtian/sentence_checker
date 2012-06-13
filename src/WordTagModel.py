'''
Created on May 15, 2012

@author: Tony
'''
import math, collections
from nltk.probability import LidstoneProbDist
#from nltk.probability import WittenBellProbDist
from nltk.model import NgramModel

def _estimator(fdist, bins):
    return LidstoneProbDist(fdist, 0.2)
    
class WordTagModel:

    def __init__(self):
        """Initialize your data structures in the constructor."""
        tag_corpus = []
        
#        from nltk.corpus import treebank
#        corpus = treebank.tagged_words()
#        for (word,tag) in treebank.tagged_words():
#            tag_corpus.append(tag)
        from nltk.corpus import brown 
        corpus = brown.tagged_words()
        for (word,tag) in brown.tagged_words():
            tag_corpus.append(tag)

        
        self.wordCounts = collections.defaultdict(int)
        self.tagCounts = collections.defaultdict(int)
        self.wordTagCounts = collections.defaultdict(int)
        self.wordTagList = {}
        self.totalTag = 0
        
        self.train(corpus)
        #estimator = lambda fdist, bins: LidstoneProbDist(fdist, 0.2) 
        #estimator = lambda fdist, bins: WittenBellProbDist(fdist, 0.2) 
        estimator = _estimator
        self.tagLM = NgramModel(2, tag_corpus, estimator)
        
#        from cPickle import dump
#        output = open('tagger.pkl', 'wb')
#        dump(tagger, output, -1)
#        output.close()
#        from cPickle import load
#        input1 =  open('../data/brown_tagger_uniBiTri.pkl', 'rb')
#        tagger = load(input1)
#        input1.close()
    
    def train(self, corpus):
        """Takes a HolbrookCorpus corpus, does whatever training is needed."""
        for (word,tag) in corpus:
            self.wordCounts[word] = self.wordCounts[word] + 1
            self.tagCounts[tag] = self.tagCounts[tag] + 1
            self.totalTag += 1
            self.wordTagCounts[(word,tag)] = self.wordTagCounts[(word,tag)] + 1
            if self.wordTagList.has_key(word):
                if tag not in self.wordTagList[word]:
                    self.wordTagList[word].append(tag)
            else:
                self.wordTagList[word] = []
                self.wordTagList[word].append(tag)
    

    def showTagList(self, word):
        if self.wordTagList.has_key(word):
            return self.wordTagList[word]
        else:
            return []
        
    def wordHasTag(self, (word,tag)):
        if self.wordTagList.has_key(word):
            if tag in self.wordTagList[word]:
                return True
            else:
                return False
        else:
            return False

        
    def entropy(self, (word,tag)=(None,None), tags=None):
        if tags == None:
            score = 0.0
            count = self.wordTagCounts[(word,tag)]
            if count > 0:
                score -= math.log(count, 2)
                #print "Word Tag count ", count
                score += math.log(self.tagCounts[tag], 2)
                #print "Tag count ", self.tagCounts[tag]
            else:
                #score = float('inf') # not smoothed
                score = 10000.0
            return score
        else:
            tokens = ""
            if len(tags) > 0:
                pre_tag = tags[0]
                for tag in tags:
                    tokens = tokens+' '+tag
                preCount = self.tagCounts[pre_tag]
#                try:
#                    preCount = self.tagCounts[pre_tag]
#                except ValueError:
#                    preCount = 1
                return self.tagLM.entropy(tokens.lstrip()) \
                         + math.log(preCount, 2) \
                         - math.log(self.totalTag, 2)
            else:
                return 10000.0


def demo():
    myModel = WordTagModel()
    
    sent = ['guarantee','NN']
    print "guarantee-NN entropy? ", myModel.entropy(sent) 
    print "guarantee has NN? ", myModel.wordHasTag(sent)
    print "guarantee list: ", myModel.showTagList('guarantee')
    
    sent = ['you', 'PPSS']
    print "you-PPSS entropy? ", myModel.entropy(sent) 
    print "you has PPSS? ", myModel.wordHasTag(sent)
    print "you list: ", myModel.showTagList('you')
    
    #sent = "DT NN"
    #print "DT NN", myModel.entropy(tags = sent) 
    #print "DT NN", myModel.entropy(tags = ['DT', 'NN']) 
    print "DO PPSS", myModel.entropy(tags = ['DO', 'PPSS'])
    
    
if __name__ == '__main__': 
    demo()