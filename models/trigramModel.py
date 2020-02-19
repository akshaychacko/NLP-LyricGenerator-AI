from creative_ai.utils.print_helpers import ppGramJson

class TrigramModel():

    def __init__(self):
        """
        Requires: nothing
        Modifies: self (this instance of the NGramModel object)
        Effects:  This is the NGramModel constructor. It sets up an empty
                  dictionary as a member variable.
        
        This function is done for you.
        """

        self.nGramCounts = {}

    def __str__(self):
        """
        Requires: nothing
        Modifies: nothing
        Effects:  Returns the string to print when you call print on an
                  NGramModel object. This string will be formatted in JSON
                  and display the currently trained dataset.
        
        This function is done for you.
        """

        return ppGramJson(self.nGramCounts)


###############################################################################
# Begin Core >> FOR CORE IMPLEMENTION, DO NOT EDIT ABOVE OF THIS SECTION <<
###############################################################################

    def trainModel(self, text):
        """
        Requires: text is a list of lists of strings
        Modifies: self.nGramCounts, a three-dimensional dictionary. For
                  examples and pictures of the TrigramModel's version of
                  self.nGramCounts, see the spec.
        Effects:  this function populates the self.nGramCounts dictionary,
                  which has strings as keys and dictionaries as values,
                  where those inner dictionaries have strings as keys
                  and dictionaries of {string: integer} pairs as values.
        """
        for i in text:
            for x in range(len(i) - 2):
                if i[x] not in self.nGramCounts:
                    self.nGramCounts[i[x]] = {}
                if i[x + 1] not in self.nGramCounts[i[x]]:
                    self.nGramCounts[i[x]][i[x + 1]] = {}
                if i[x + 2] not in self.nGramCounts[i[x]][i[x + 1]]:
                    self.nGramCounts[i[x]][i[x + 1]][i[x + 2]] = 0
                    
                self.nGramCounts[i[x]][i[x + 1]][i[x + 2]] += 1
                

        

    def trainingDataHasNGram(self, sentence):
        """
        Requires: sentence is a list of strings
        Modifies: nothing
        Effects:  returns True if this n-gram model can be used to choose
                  the next token for the sentence. For explanations of how this
                  is determined for the TrigramModel, see the spec.
        """
        return bool(self.nGramCounts[sentence[-2]][sentence[-1]])

    
    def getCandidateDictionary(self, sentence):
        """
        Requires: sentence is a list of strings, and trainingDataHasNGram
                  has returned True for this particular language model
        Modifies: nothing
        Effects:  returns the dictionary of candidate next words to be added
                  to the current sentence. For details on which words the
                  TrigramModel sees as candidates, see the spec.
        """
        return self.nGramCounts[sentence[-2]][sentence[-1]]
            

###############################################################################
# End Core
###############################################################################

###############################################################################
# Main
###############################################################################

if __name__ == '__main__':
    '''
   # An example trainModel test case
    uni = TrigramModel()
    text = [ [ 'a','brown' ] ]
    uni.trainModel(text)
    # Should print: { 'brown' : 1 }
    print(uni)
    uni = TrigramModel()
    text = [ ['a', 'rose', 'is', 'a', 'flower', 'is', 'a', 'rose'], ['the', 'rose', 'died'] ]
    uni.trainModel(text)
    # Should print: { 'brown': 2, 'dog': 1, 'fox': 1, 'lazy': 1, 'the': 2 }
    print(uni)

    bigram = TrigramModel()

    text = [['the', 'test', 'the'], ['test']]

    bigram.trainModel(text)
    print(bigram)
    # An example trainingDataHasNGram test case
    uni = TrigramModel()
    sentence = "Eagles fly in the sky"
    print(uni.trainingDataHasNGram(sentence)) # should be False
    uni.trainModel(text)
    print(uni.trainingDataHasNGram(sentence)) # should be True
    
    print(uni.getCandidateDictionary(sentence))
    '''
    # An example trainModel test case
    uni = TrigramModel()
    text = [ [ 'brown' ] ]
    uni.trainModel(text)
    # Should print: { 'brown' : 1 }
    print(uni)

    text = [ ['the', 'brown', 'fox'], ['the', 'lazy', 'dog'] ]
    uni.trainModel(text)
    # Should print: { 'brown': 2, 'dog': 1, 'fox': 1, 'lazy': 1, 'the': 2 }
    print(uni)

    # An example trainingDataHasNGram test case
    uni = TrigramModel()
    sentence = "the lazy dog"
    print(uni.trainingDataHasNGram(sentence)) # should be False
    uni.trainModel(text)
    print(uni.trainingDataHasNGram(sentence)) # should be True
