from nltk import pos_tag, word_tokenize

import DetectLanguage

# download('all')
import re
import copy

from html.entities import name2codepoint

import locale, datetime

import csv

names = ["Giovanna Grippe"]
facebookLocal = "pt_BR" #for data parsing
dateFormat = '%a, %d de %B de %Y'
releventWordClasses = ["RP","RB","NN","VB","FW","JJ","JJR","JJS","NNP","NNS","POS","RBR","RBS","VBD","VBG","VBN","VBP","VBZ" ]
releventWordClassesList = [["RP",0],["RB",0],["NN",0],["VB",0],["FW",0],["JJ",0],["JJR",0],["JJS",0],["NNP",0],["NNS",0],["POS",0],["RBR",0],["RBS",0],["VBD",0],["VBG",0],["VBN",0],["VBP",0],["VBZ",0] ]

# nltk.help.upenn_tagset():
# FW -foreign word
# JJ: adjective or numeral, ordinal
# JJR: adjective, comparative
# JJS: adjective, superlative
# NNP: noun, proper, singular
# NN: noun, common, singular or mass
# NNS: noun, common, plural
# POS: genitive marker
# RB: adverb
# RBR: adverb, comparative
# RBS: adverb, superlative
# RP: particle
# VB: verb, base form
# VBD: verb, past tense
# VBG: verb, present participle or gerund
# VBN: verb, past participle
# VBP: verb, present tense, not 3rd person singular
# VBZ: verb, present tense, 3rd person singular


def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return chr(int(text[3:-1], 16))
                else:
                    return chr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = chr(name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)




filepath = "input/messagesGio.htm"
file = open(filepath, "r")
dom = file.read()
dom = unescape(dom)
file.close()

particleList = []

regex = re.compile('<div class="message_header"><span class="user">[^<]*</span><span class="meta">[^<]*</span></div></div><p>[^<]*')
listOfMessages = regex.findall(dom)

regex = re.compile('<div class="message_header"><span class="user">[^<]*')
# length of fixed string, 47
regex2 = re.compile('class="meta">[^<]*')
# length of fixed string, 13
regex3 = re.compile('<p>[^<]*')

listOfMessages = list(filter(lambda subdom: (regex.findall(subdom)[0][47:] in names), listOfMessages))
listOfMessages = list(filter(lambda message: (DetectLanguage.detect_language(message) == "english"), listOfMessages))

print(listOfMessages)

def formatMessage(subDom):
    locale.setlocale(locale.LC_ALL, "pt_BR")
    dateString = regex2.findall(subDom)[0]
    dateString = dateString[13:16] + dateString[dateString.index(','):dateString.index('à')-1]
    # current format: Quinta... recognized: Qui
    date = datetime.datetime.strptime(dateString, dateFormat)
    message = pos_tag(word_tokenize(regex3.findall(subDom)[0][3:]))
    print(message)
    return {'date' : date, 'message' : message}

listOfMessages = list(map(formatMessage, listOfMessages))



months = {}

for entry in listOfMessages:
    if (str(entry["date"].day) + "-" + str(entry["date"].month) + "-" + str(entry["date"].year)) not in months:
        months[str(entry["date"].day) + "-" + str(entry["date"].month) + "-" + str(entry["date"].year)] = copy.deepcopy(releventWordClassesList)
    for word in entry["message"]:
        if word[1] == "RP": # is particle
            print(word[0])
        #one word can have multiple tags, but then will have multiple tuplets
        if word[1] in releventWordClasses:
            for tup in months[str(entry["date"].day) + "-" + str(entry["date"].month) + "-" + str(entry["date"].year)]:
                if tup[0] == word[1]:
                    tup[1] = tup[1] + 1

# print(months)

filepath = "wordTagsByMonthGio.csv"
file = open(filepath, "w")
with file as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['Month'] + releventWordClasses)
    for key, value in months.items():
        vals = []
        for val in value:
            vals += [val[1]]
        spamwriter.writerow([key] + vals)




# pretty Print to JSON:
# print(json.dumps(months, sort_keys=True, indent=4, separators=(',', ': ')))
