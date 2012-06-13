'''
Created on May 14, 2012

@author: Tony
'''

class Tagger:
    
    def __init__(self, rebuild=False):
        if rebuild:
            from cPickle import dump
            output = open('tagger.pkl', 'wb')
            
            from nltk.tag import DefaultTagger, UnigramTagger, BigramTagger, TrigramTagger
            # Load the brown corpus.
            from nltk.corpus import brown
            brown_train = brown.tagged_sents()[100:]
            #unitagger = UnigramTagger(brown_train)
            #result = tagger.tag(brown.sents()[501])
            #bitagger = BigramTagger(brown_train)
            #tritagger = TrigramTagger(brown_train)
            
            def backoff_tagger(train_sents, tagger_classes, backoff= None):
                for cls in tagger_classes:
                    backoff = cls(train_sents, backoff= backoff)
                return backoff
            
            backoff = DefaultTagger('NN')
            self.tagger = backoff_tagger(brown_train, [UnigramTagger, BigramTagger, TrigramTagger], backoff= backoff)
            dump(self.tagger, output, -1)
            output.close()

        else:
            from cPickle import load
            input1 =  open('../data/brown_tagger_uniBiTri.pkl', 'rb')
            self.tagger = load(input1)
            input1.close()
    
    def tag(self, sent):
        return self.tagger.tag(sent)
    
    def evaluate(self, corpus):
        return self.tagger.evaluate(corpus)

def demo():
    myTagger = Tagger()
    
    from nltk.tag import untag
    # Load the brown corpus.
    from nltk.corpus import brown
    
    #brown_train = brown.tagged_sents()[100:]
    brown_test = brown.tagged_sents()[:100]
    test_sent = untag(brown_test[1])
    
    score = myTagger.evaluate(brown_test)
    print "Score: ", score
    result = myTagger.tag(test_sent)
    print result
    
    print myTagger.tag(['drink', 'some', 'water'])
    
if __name__ == '__main__': 
    demo()