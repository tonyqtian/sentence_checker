#from Datum import Datum
from Sentence import Sentence
from HolbrookCorpus import HolbrookCorpus
#from EditModel import EditModel
from SpellingResult import SpellingResult
#import types

import math
import enchant
from nltk.corpus import gazetteers
from nltk.corpus import names

# Modified version of Peter Norvig's spelling corrector
"""Spelling Corrector.

Copyright 2007 Peter Norvig. 
Open source code under MIT license: http://www.opensource.org/licenses/mit-license.php
"""

#import re, collections

class SpellCorrect:
    """Holds edit model, language model, corpus. trains"""
    
    
    def __init__(self, lm, confSet, tagger, wordTag):
        """initializes the language model."""
        self.languageModel = lm
        self.confusionSet = confSet
        self.tagger = tagger
        self.wordTagModel = wordTag
        self.dict = enchant.Dict('en')
        self.myDict = {}
        for word in names.words():
            self.myDict[word] = 1
        for word in gazetteers.words():
            self.myDict[word] = 2
    
    
    def evaluate(self, corpus):  
        """Tests this speller on a corpus, returns a SpellingResult"""
        numCorrect = 0
        numTotal = 0
        
        marked_err = 0
        marked_noerr = 0
        unmarked_err = 0
        unmarked_noerr = 0
        tmp = (0, 0, 0, 0)
        
        testData = corpus.generateTestCasesAllErr()
        for sentence in testData:
            if sentence.isEmpty():
                continue
            errorSentence = sentence.getErrorSentence()
            
            # None word error correction, ignore capitalized words
            hypothesis = self.nonwordCorrection(errorSentence)
            
            # Real word error correction, use confusion set
            hypothesis = self.realwordCorrection(hypothesis)
            
            tmp = sentence.isCorrection(hypothesis)
            marked_err += tmp[0]
            marked_noerr += tmp[1]
            unmarked_err += tmp[2]
            unmarked_noerr += tmp[3]
            
            if (tmp[0] + tmp[3]) == len(hypothesis):
                numCorrect += 1
#            else:
#                correctSentence = sentence.getCorrectSentence()
#                flag = 0
#                for word in correctSentence:
#                    if word.startswith('[fm'):
#                        flag = 1
#                        break
#                if flag == 1:
#                    hypoCorrection = sentence.getMyCorrection(hypothesis)
#                    print "Snt No. ", numTotal+1, " Incorrect..."
#                    print "Error Snt>>> ", Sentence(errorSentence)
#                    print "Crrct Snt>>> ", Sentence(correctSentence)
#                    print "Hypo Sent>>> ", Sentence(hypoCorrection)
#                    print " "
            correctSentence = sentence.getCorrectSentence()
            hypoCorrection = sentence.getMyCorrection(hypothesis)
            print "Snt No. ", numTotal+1, " Incorrect..."
            print "Error Snt>>> ", Sentence(errorSentence)
            print "Crrct Snt>>> ", Sentence(correctSentence)
            print "Hypo Sent>>> ", Sentence(hypoCorrection)
            print " "
            numTotal += 1
            
        return SpellingResult(marked_err, marked_noerr, unmarked_err, unmarked_noerr, numCorrect, numTotal)
    
    def nonwordCorrection(self, sentence):
        """Takes a list of words, returns a corrected list of words."""
        if len(sentence) == 0:
            return []
        argmax_i = 0
        argmax_w = sentence[0]
        minscore = float('-inf')
        argmax = list(sentence) # copy it
        
        # skip start and end tokens
        for i in range(1, len(sentence) - 1):
            word = sentence[i]
            if not len(word):
                continue
            flag = 0
            if not word[0].isupper():
                if not self.dict.check(word):
                    if not self.dict.check(word.title()):
                        if not self.myDict.get(word.title() , 0):
                            if word.count(' '):
                                word_chop = word.split()
                                for tokens in word_chop:
                                    if not tokens[0].isupper():
                                        if not self.dict.check(tokens):
                                            if not self.dict.check(tokens.title()):
                                                if not self.myDict.get(tokens.title() , 0):
                                                    flag = 1
                            else:
                                flag = 1
            if flag == 1:                   
                argmax_i = i
                argmax_w = word
                minscore = self.languageModel.entropy(sentence)
                
                sgtList = self.dict.suggest(word)
                j = 1  #add punishment to edit distance
                for alternative in sgtList:
                    if alternative == word:
                        continue
                    sentence[i] = alternative
                    score = self.languageModel.entropy(sentence) + math.log(j,2)
                    if score <= minscore:
                        minscore = score
                        argmax_w = alternative
                    j *= 2
                    #j += 1
        
                sentence[i] = word # restores sentence to original state before moving on
                argmax[argmax_i] = argmax_w # correct it
        return argmax  
    
    def realwordCorrection(self, sentence):
        """Takes a list of words, returns a corrected list of words."""
        if len(sentence) == 0:
            return []
        argmax_i = 0
        argmax_w = sentence[0]
        minscore = float('-inf')
        argmax = list(sentence) # copy it
        
        # skip start and end tokens
        for i in range(1, len(sentence) - 1):
            word = sentence[i]
            if not len(word):
                continue

            if self.confusionSet.inDict(word):
                #print "Find word: ", word
                argmax_i = i
                argmax_w = word
                minscore = self.languageModel.entropy(sentence) - math.log(16, 2)
                
                sgtList = self.confusionSet.getList(word)
                for alternative in sgtList:
                    if alternative == word:
                        continue
                    sentence[i] = alternative
                    score = self.languageModel.entropy(sentence)
                    if score <= minscore:
                        minscore = score
                        argmax_w = alternative
        
                sentence[i] = word # restores sentence to original state before moving on
                argmax[argmax_i] = argmax_w # correct it
        return argmax  
    
        
    def syntaxCorrection(self, sentence, wild=False):
        """Takes a list of words, returns a corrected list of words."""
        if len(sentence) == 0:
            return []
        argmax_i = 0
        argmax_w = sentence[0]
        minscore = float('-inf')
        argmax = list(sentence) # copy it
        
        tagged_sent = self.tagger.tag(sentence)
        
        # skip start and end tokens
        for i in range(1, len(sentence) - 1):
            word = sentence[i]
            if not len(word):
                continue

            if self.confusionSet.isDistinct(word):
                #print "Find word: ", word
                argmax_i = i
                argmax_w = word
                this_tag = tagged_sent[i][1]
                pre_tag = tagged_sent[i-1][1]
                next_tag = tagged_sent[i+1][1]
                minscore = self.wordTagModel.entropy(tags = [pre_tag, this_tag]) \
                            + self.wordTagModel.entropy(tagged_sent[i]) \
                            + self.wordTagModel.entropy(tags = [this_tag, next_tag])
                
                sgtList = self.confusionSet.getDistinctList(word)
                for alternative in sgtList:
                    if alternative == word:
                        continue
                    sentence[i] = alternative
                    tagged_alter = self.tagger.tag(sentence)
                    this_tag = tagged_alter[i][1]
                    pre_tag = tagged_alter[i-1][1]
                    next_tag = tagged_alter[i+1][1]
                    score = self.wordTagModel.entropy(tags = [pre_tag, this_tag]) \
                                + self.wordTagModel.entropy(tagged_alter[i]) \
                                + + self.wordTagModel.entropy(tags = [this_tag, next_tag])
                    if score <= minscore:
                        minscore = score
                        argmax_w = alternative
        
                sentence[i] = word # restores sentence to original state before moving on
                argmax[argmax_i] = argmax_w # correct it
        return argmax  
            
            
    def correctCorpus(self, corpus): 
        """Corrects a whole corpus, returns a JSON representation of the output."""
        string_list = [] # we will join these with commas,  bookended with []
        sentences = corpus.corpus
        for sentence in sentences:
            uncorrected = sentence.getErrorSentence()
            corrected = self.correctSentence(uncorrected) # List<String>
            word_list = '["%s"]' % '","'.join(corrected)
            string_list.append(word_list)
        output = '[%s]' % ','.join(string_list)
        return output


def NgramLM(corpus):
    corpus_words = []
    for sentence in corpus.corpus:
        for datum in sentence.data:
            token = datum.word
            corpus_words.append(token)
    #from nltk.corpus import brown 
    from nltk.probability import LidstoneProbDist
    #from nltk.probability import WittenBellProbDist 
    from nltk.model import NgramModel
    estimator = lambda fdist, bins: LidstoneProbDist(fdist, 0.2) 
    #    estimator = lambda fdist, bins: WittenBellProbDist(fdist, 0.2) 
    #lm = NgramModel(2, brown.words(categories='news'), estimator) 
    lm = NgramModel(3, corpus_words, estimator)
    return lm 


def LM(corpus_name):
    from nltk.model import NgramModel
    from nltk.probability import LidstoneProbDist
    #from nltk.probability import WittenBellProbDist
    if corpus_name.lower() == 'reuters':
        from nltk.corpus import reuters 
        corpus = reuters.words()
    elif corpus_name.lower() == 'brown':
        from nltk.corpus import brown 
        corpus = brown.words()
        
    estimator = lambda fdist, bins: LidstoneProbDist(fdist, 0.2) 
    #estimator = lambda fdist, bins: WittenBellProbDist(fdist, 0.2) 
    lm = NgramModel(4, corpus, estimator)
    return lm

    
def main(reinitial):
    """Trains all of the language models and tests them on the dev data. Change devPath if you
       wish to do things like test on the training data."""
    
    print "Preparing dev corpus..."
    #devPath = '../data/holbrook-tagged-dev.dat'
    #devPath = '../data/CLEC_tagged.dat'
    devPath = '../data/CLEC_handmade.dat'
    devCorpus = HolbrookCorpus(devPath)

    if reinitial == True:
        from cPickle import dump     
        
        from confSet import confusionSet
        print "Load confusion set..."
        myConfSet = confusionSet()
        print "Dump confusion set..."
        output1 = open('../data/myCondfSet.pkl', 'wb')
        dump(myConfSet, output1, -1)
        output1.close()
        
        from TaggerTest import Tagger
        print "Load brown tagger..."
        myTagger = Tagger()
        print "Dump brown tagger..."
        output2 = open('../data/myBrown_tagger.pkl', 'wb')
        dump(myTagger, output2, -1)
        output2.close()
        
#        from CustomLanguageModel import CustomLanguageModel
#        print "Load custom language model..."
#        customLM = CustomLanguageModel(trainingCorpus)
#        print "Dump custom language model..."
#        output4 = open('../data/myCustomLM.pkl', 'wb')
#        dump(customLM, output4, -1)
#        output4.close()

#        trainPath = '../data/holbrook-tagged-train.dat'
#        trainPath = '../data/CLEC_noerr.dat'
#        trainingCorpus = HolbrookCorpus(trainPath)        
#        customLM = NgramLM(trainingCorpus) 
    
    if reinitial == False:
        from cPickle import load
        
        print "Loading confusion set from pickle..."
        input1 =  open('../data/myCondfSet.pkl', 'rb')
        myConfSet = load(input1)
        input1.close()
        
        print "Loading Brown tagger from pickle..."
        input2 =  open('../data/myBrown_tagger.pkl', 'rb')
        myTagger = load(input2)
        input2.close() 

#        print "Loading Training from pickle..."
#        input4 =  open('../data/myCustomLM.pkl', 'rb')
#        customLM = load(input4)
#        input4.close()
    
    #customLM = NgramLM(trainingCorpus)
    print "Preparing training LM..."
    customLM = LM('reuters')
#    print "Loading WordTagModel..."
#    from WordTagModel import WordTagModel
#    myWordTag = WordTagModel()
    myWordTag = []

#    from pickle import dump
#    output3 = open('../data/myBrown_wordTagModel.pkl', 'wb')
#    dump(myWordTag, output3, -1)
#    output3.close()

#    import pickle
#    print "Loading word-tag model from pickle..."
#    input3 =  open('../data/myBrown_wordTagModel.pkl', 'rb')
#    myWordTag = pickle.load(input3)
#    input3.close()
    
    print "Initializing the Checker..."
    customSpell = SpellCorrect(customLM, myConfSet, myTagger, myWordTag)
    print "Correcting Test Set and Evaluating..."
    customOutcome = customSpell.evaluate(devCorpus)
    print str(customOutcome)
    print "Finished"

if __name__ == "__main__":
    reinit = True
    main(reinit)