from nltk import pos_tag, word_tokenize


releventWordClasses = ["RP","RB","NN","VB","FW","JJ","JJR","JJS","NNP","NNS","POS","RBR","RBS","VBD","VBG","VBN","VBP","VBZ"]
releventWordClassesDict = {}
for tag in releventWordClasses:
    releventWordClassesDict[tag] = 0


particleDict = {}
totalWordCount = 0


from nltk.corpus import nps_chat
chatroom = nps_chat.posts()
wordList = []
for l in chatroom[1:4256]:
    wordList += l

for l in chatroom[4259:]:
    wordList += l

# from nltk.corpus import brown
# wordList = brown.words(categories='news')
# http://www.nltk.org/book/ch02.html
print(wordList)
wordList = pos_tag(wordList)

for word in wordList:
    totalWordCount += 1
    if word[1] == 'RP': # is particle
        if word[0] not in particleDict.keys():
            particleDict[word[0]] = 1
        else:
            particleDict[word[0]] += 1
    #one word can have multiple tags, but then will have multiple tuplets
    if word[1] in releventWordClasses:
        releventWordClassesDict[word[1]] += 1


print("totalWordCount:" + str(totalWordCount))
print("\n")
print("releventWordClassesDict:" + str(releventWordClassesDict))
print("\n")
for tag in releventWordClassesDict.keys():
    releventWordClassesDict[tag] = 100 * releventWordClassesDict[tag] / totalWordCount
print("releventWordClassesDictAsPercentage:" + str(releventWordClassesDict))


print("\n\n\n\n\n\n\n\n")

print("totalParticalCount:" + str(len(particleDict.keys())))
print("PARTICLEDICT:" + str(particleDict))
