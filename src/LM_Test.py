'''
Created on May 14, 2012

@author: Tony
'''

def demo():
    from nltk.corpus import treebank 
    #from nltk.probability import LidstoneProbDist
    #from nltk.probability import WittenBellProbDist
    from nltk.probability import SimpleGoodTuringProbDist
    from nltk.model import NgramModel
    estimator = lambda fdist, bins: SimpleGoodTuringProbDist(fdist, len(fdist)+1) 
    #estimator = lambda fdist, bins: LidstoneProbDist(fdist, 0.2) 
    #estimator = lambda fdist, bins: WittenBellProbDist(fdist, 0.2) 
    
    tag_corpus = []
    for (word,tag) in treebank.tagged_words():
        tag_corpus.append(tag)
    lm = NgramModel(2, tag_corpus, estimator) 
    print lm 
    lm1 = NgramModel(1, tag_corpus, estimator) 
    print lm1 
    print tag_corpus[:20]

    sent = "NN"
    print lm1.entropy(sent) 
    
    sent = "DT "
    print lm1.entropy(sent) 

    sent = "VBZ"
    print lm1.entropy(sent) 
    
    sent = "JJ"
    print lm1.entropy(sent) 
    
    sent = "RB"
    print lm1.entropy(sent) 
    
    sent = "DT NN"
    print lm.entropy(sent) 

#    text = lm.generate(100) 
#    import textwrap 
#    print '\n'.join(textwrap.wrap(' '.join(text))) 
    
if __name__ == '__main__': 
    demo()