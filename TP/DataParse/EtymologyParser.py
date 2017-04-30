import EtymTagger
from nltk import pos_tag, word_tokenize

def readFromFacebook(namesArray, filepathIn, filePathOut):
    """
    Reads from the htm output by facebook specified. Returns a list of strings
    corresponding to different messages sent by the facebook users in
    namesArray.
    Parameters:
        namesArray - names of FB users
        filepath - the location of the facebook message .htm
    """
    import ReadFacebookDOM
    allMessages = ReadFacebookDOM.readInfo(namesArray, filepathIn)
    parseEtymologies(allMessages, filePathOut)


def readFromTXT(filepathIn, filePathOut):
    """
    Reads from a txt file. Returns a list of strings
    corresponding to lines in the .txt
    Parameters:
        filepath - the location of the facebook message .htm
    """
    fileIn = open(filepathIn,'r')
    allMessages = []
    for line in fileIn:
        allMessages += [line]
    parseEtymologies(allMessages,filePathOut)

def parseEtymologies(listOfMessages, filePathOut):
    """
    Produces a count of different etymologies in the given messages.
    Prints and saves output to output.txt
    Parameters:
        listOfMessages - the location of the facebook message .htm
    """
    outFile = open(filePathOut, 'w')

    releventWordClasses = ["JJ", "NN", "NNS", "RB", "VB", "VBP"]
    # nltk.help.upenn_tagset():
    # FW -foreign word
    # JJ: adjective or numeral, ordinal
    # JJR: adjective, comparative #not in etymology database
    # JJS: adjective, superlative #not in etymology database
    # NNP: noun, proper, singular #no proper nouns
    # NN: noun, common, singular or mass
    # NNS: noun, common, plural
    # RB: adverb
    # RBR: adverb, comparative
    # RBS: adverb, superlative
    # RP: particle
    # POS: genitive marker
    # VB: verb, base form
    # VBD: verb, past tense # present, but would give false negatives
    # VBG: verb, present participle or gerund # """"
    # VBN: verb, past participle # not in database
    # VBP: verb, present tense, not 3rd person singular
    # VBZ: verb, present tense, 3rd person singular  # not in database

    setOfWords = set({})
    wordCountInOriginalDocument = 0
    for message in listOfMessages:
        for word in word_tokenize(message):
            wordCountInOriginalDocument += 1
            if str(pos_tag([word])[0][1]) in releventWordClasses:
                setOfWords.add(word)

    etymologyDict = EtymTagger.produceReport(setOfWords)


    # # read python dict back from the file
    # pkl_file = open('myfile.pkl', 'rb')
    # mydict2 = pickle.load(pkl_file)
    # pkl_file.close()

    for category in etymologyDict.keys():
        out = str(category) + "\t" + str(etymologyDict[category])
        outFile.write(str(out) + "\n")
    outFile.write("word_count_with_redundancies" + "\t" \
        + str(wordCountInOriginalDocument))


readFromTXT('input/Academic/English.txt','erase.txt')
