#!/usr/bin/env python
import sys
sys.dont_write_bytecode = True # Suppress .pyc files
import random
import tweepy

import spacy
nlp = spacy.load('en_core_web_sm')

from creative_ai.pysynth import pysynth
from creative_ai.utils.menu import Menu
from creative_ai.data.dataLoader import *
from creative_ai.models.musicInfo import *
from creative_ai.models.languageModel import LanguageModel

TEAM = 'BORN2BWILD'
LYRICSDIRS = ['country']
TESTLYRICSDIRS = ['country']
MUSICDIRS = ['gamecube']
WAVDIR = 'wav/'

consumer_key = 'sHr529n6UOSqFTh9d8Z0rQuvZ'
consumer_secret = 'PkxsoHvzVOrxtXBVDYG3WsgvDZDKG5OjXKhzNGBrm08NrkVn45'
access_token = '1070157648354557952-8yxfR0ovGwIWRPIcslFUQqf1sKKYn7'
access_token_secret = 'wI5VNWHgoTEDWKbmWksLwK1ndvyrDjBEMw28hvRemUXhG'
 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

def recognizeNouns(token, line):
    word = nlp(token)
    string = ' '.join(line)
    sentence = nlp(string)
    isNoun = False

    if word[0].pos_ == "NOUN":
        isNoun = True
    if word[0].pos_ == "PROPN":
        isNoun = True

    return isNoun

def replaceNoun(word):
    lang = LanguageModel()
    
    options = {'PERSON': 1, 'GPE': 1, 'PRODUCT': 3, 'unmodified': 30}
               
    Names = ["Billy Bob", "Suzy Lee", "Annabella", "Joe", "Bart", "Billy Ray", "Bo", "Carolina", "Charles Ray", "Daisy", "Dixie", "Forrest", "Garth", "Georgina", "Jim Bob", "Raleigh"]
    Places = ["Houston", "Austin", "El Paso", "Texas", "Dallas", "Mexico", "Mississippi", "Alabama", "Georgia", "North Carolina", "West Virginia", "Tenessee", "Kentucky", "Jackson", "Raleigh", "New Orleans", "Atlanta", "Winston-Salem", "Charleston", "Charlotte", "Nashville", "Memphis"]
    Objects = ['divorce', 'mama', 'cruel heart', 'lyin fool', 'wacky tabacky', 'red solo cup', 'dirt', 'dip', 'ranch', 'cows', 'truck', 'pickup', 'tractor', 'whiskey', 'tequila', 'moonshine', 'beer', 'blue jeans', 'corn', 'tractor', 'truck', 'guitar', 'strawberry wine', 'banjo', 'cigarettes']
        
    x = lang.weightedChoice(options)
    
    if x == "PERSON":
        word = random.choice(Names)
    if x == "GPE":
        word = random.choice(Places)
    if x == "PRODUCT":
        word = random.choice(Objects)

    return word

def output_models(val, output_fn = None):
    """
    Requires: nothing
    Modifies: nothing
    Effects:  outputs the dictionary val to the given filename. Used
              in Test mode.
    """
    from pprint import pprint
    if output_fn == None:
        print("No Filename Given")
        return
    with open('TEST_OUTPUT/' + output_fn, 'wt') as out:
        pprint(val, stream=out)

def sentenceTooLong(desiredLength, currentLength):
    """
    Requires: nothing
    Modifies: nothing
    Effects:  returns a bool indicating whether or not this sentence should
              be ended based on its length.
    """
    STDEV = 1
    val = random.gauss(currentLength, STDEV)
    return val > desiredLength

def printSongLyrics(verseOne, verseTwo, verseThree, chorus):
    """
    Requires: verseOne, verseTwo, and chorus are lists of lists of strings
    Modifies: nothing
    Effects:  prints the song.
    
    """

    repeat = chorus[0:2]
    verses = [verseOne, chorus, verseTwo, verseThree, chorus, chorus, repeat, repeat]
    
    twitt = []
    twitt1 = []
    twitt2 = []
    twitt3 = []
    twitt4 = []
    for verse in verses:
        for line in verse:
            for x in range(len(line)):
                isNoun = recognizeNouns(line[x], line)
                if isNoun == True:
                    line[x] = replaceNoun(line[x])
            print((' '.join(line)).capitalize())
    
        print()

    first = True;
    for i in verseOne:
        for x in i:
            if (first == True):
                twitt1.append(x.capitalize())
                first = False;
            else:
                twitt1.append(x)
        twitt1.append('\n')
        first = True;
        
    for i in verseTwo:
        for x in i:
            if (first == True):
                twitt2.append(x.capitalize())
                first = False;
            else:
                twitt2.append(x)
        twitt2.append('\n')
        first = True;

    for i in verseThree:
        for x in i:
            if (first == True):
                twitt3.append(x.capitalize())
                first = False;
            else:
                twitt3.append(x)
        twitt3.append('\n')
        first = True;
            
    for i in chorus:
        for x in i:
            if (first == True):
                twitt4.append(x.capitalize())
                first = False;
            else:
                twitt4.append(x)
        twitt4.append('\n')
        first = True;


    api.update_status(' '.join(twitt4))
    api.update_status(' '.join(twitt3))
    api.update_status(' '.join(twitt2))
    api.update_status('2018s newest hit song!!\n\n' + ' '.join(twitt1))

def trainLyricModels(lyricDirs, test=False):
    """
    Requires: lyricDirs is a list of directories in data/lyrics/
    Modifies: nothing
    Effects:  loads data from the folders in the lyricDirs list,
              using the pre-written DataLoader class, then creates an
              instance of each of the NGramModel child classes and trains
              them using the text loaded from the data loader. The list
              should be in tri-, then bi-, then unigramModel order.
              Returns the list of trained models.
              
    """
    model = LanguageModel()

    for ldir in lyricDirs:
        lyrics = prepData(loadLyrics(ldir))
        model.updateTrainedData(lyrics)

    return model

def trainMusicModels(musicDirs):
    """
    Requires: musicDirs is a list of directories in data/midi/
    Modifies: nothing
    Effects:  works exactly as trainLyricsModels, except that
              now the dataLoader calls the DataLoader's loadMusic() function
              and takes a music directory name instead of an artist name.
              Returns a list of trained models in order of tri-, then bi-, then
              unigramModel objects.
    """
    model = LanguageModel()

    for mdir in musicDirs:
        music = prepData(loadMusic(mdir))
        model.updateTrainedData(music)

    return model

def runLyricsGenerator(models):
    """
    Requires: models is a list of a trained nGramModel child class objects
    Modifies: nothing
    Effects:  generates a verse one, a verse two, and a chorus, then
              calls printSongLyrics to print the song out.
    """
    verseOne = []
    verseTwo = []
    chorus = []
    verseThree = []

    for _ in range(4):
        verseOne.append(generateTokenSentence(models, 25))
        verseTwo.append(generateTokenSentence(models, 25))
        chorus.append(generateTokenSentence(models, 25))
        verseThree.append(generateTokenSentence(models, 25))
    printSongLyrics(verseOne, verseTwo, verseThree, chorus)

def runMusicGenerator(models, songName):
    """
    Requires: models is a list of trained models
    Modifies: nothing
    Effects:  uses models to generate a song and write it to the file
              named songName.wav
    """

    verseOne = []
    verseTwo = []
    chorus = []

    for i in range(4):
        verseOne.extend(generateTokenSentence(models, 7))
        verseTwo.extend(generateTokenSentence(models, 7))
        chorus.extend(generateTokenSentence(models, 9))

    song = []
    song.extend(verseOne)
    song.extend(verseTwo)
    song.extend(chorus)
    song.extend(verseOne)
    song.extend(chorus)

    pysynth.make_wav(song, fn=songName)

###############################################################################
# Begin Core >> FOR CORE IMPLEMENTION, DO NOT EDIT OUTSIDE OF THIS SECTION <<
###############################################################################

def generateTokenSentence(model, desiredLength):
    """
    Requires: models is a list of trained NGramModel objects sorted by
              descending priority: tri-, then bi-, then unigrams.
              desiredLength is the desired length of the sentence.
    Modifies: nothing
    Effects:  returns a list of strings where each string is a word in the
              generated sentence. The returned list should NOT include
              any of the special starting or ending symbols.
              For more details about generating a sentence using the
              NGramModels, see the spec.
    """


    # takes a dictionary of words that have been analyzed into tri/bi/unigrams
    # (words w/ weighted probability about the word and following words)

    nlp = spacy.load("en_core_web_sm")
    sentence = ["^::^", "^:::^"]
    nextToken = ''
    
    while (sentenceTooLong(desiredLength, len(sentence) - 2) == False) and nextToken != '$:::$':
        nextToken = model.getNextToken(sentence, filter=None)
        sentence.append(nextToken)
    if nextToken == '$:::$':
        sentence.remove('$:::$')
        lastWord = sentence[-1]
        doc = nlp(lastWord)
        while doc[0].pos_ == "DET" or doc[0].pos_ == "CONJ" and len(sentence) > 3:
            sentence.remove(lastWord)
            lastWord = sentence[-1] 
            doc = nlp(lastWord)
    return sentence[2: ]

###############################################################################
# End Core
###############################################################################

###############################################################################
# Main
###############################################################################

PROMPT = [
    'Generate country music song lyrics',
    'Generate a song using data from Nintendo Gamecube',
    'Quit the music generator'
]

def main():
    """
    Requires: Nothing
    Modifies: Nothing
    Effects:  This is your main function, which is done for you. It runs the
              entire generator program for both the reach and the core.
              It prompts the user to choose to generate either lyrics or music.
    """

    mainMenu = Menu(PROMPT)

    lyricsTrained = False
    musicTrained = False

    print('Welcome to the {} music generator!'.format(TEAM))
    while True:
        userInput = mainMenu.getChoice()

        if userInput == 1:
            if not lyricsTrained:
                print('Starting lyrics generator...')
                lyricsModel = trainLyricModels(LYRICSDIRS)
                lyricsTrained = True

            runLyricsGenerator(lyricsModel)

        elif userInput == 2:
            if not musicTrained:
                print('Starting music generator...')
                musicModel = trainMusicModels(MUSICDIRS)
                musicTrained = True

            songName = input('What would you like to name your song? ')
            
            runMusicGenerator(musicModel, WAVDIR + songName + '.wav')

        elif userInput == 3:
            print('Thank you for using the {} music generator!'.format(TEAM))
            sys.exit()

# This is how python tells if the file is being run as main
if __name__ == '__main__':
    main()

    # lang = LanguageModel()
    # file = ()
    # x = trainLyricModels("/Users/happyperformer/Desktop/Creative_AI_3022_Repository/creative_ai/data/lyrics/test.txt")
    
    # lang.updateTrainedData(x, prepped=True)
    # variable = 10
    # x = generateTokenSentence(lang, variable)
    # print (x)
