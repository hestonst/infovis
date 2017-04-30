from nltk import pos_tag, word_tokenize
# download('all')
import re
import copy
from html.entities import name2codepoint
from dateutil.parser import parse as dateParse
# adds support for parsing in 20 languages
import csv

names = ["Giovanna Grippe"]
releventWordClasses = ["ENG_RP","ENG_RB","ENG_NN","ENG_VB","ENG_FW","ENG_JJ","ENG_JJR","ENG_JJS","ENG_NNP","ENG_NNS","ENG_POS","ENG_RBR","ENG_RBS","ENG_VBD","ENG_VBG","ENG_VBN","ENG_VBP","ENG_VBZ" ]
releventWordClassesList = [["ENG_RP",0],["ENG_RB",0],["ENG_NN",0],["ENG_VB",0],["ENG_FW",0],["ENG_JJ",0],["ENG_JJR",0],["ENG_JJS",0],["ENG_NNP",0],["ENG_NNS",0],["ENG_POS",0],["ENG_RBR",0], ["ENG_RBS",0],["ENG_VBD",0],["ENG_VBG",0],["ENG_VBN",0],["ENG_VBP",0],["ENG_VBZ",0]]


# nltk.help.upenn_tagset():
# FW -foreign word
# JJ: adjective or numeral, ordinal
# JJR: adjective, comparative
# JJS: adjective, superlative
# NNP: noun, proper, singular
# NN: noun, common, singular or mass
# NNS: noun, common, plural
# RB: adverb
# RBR: adverb, comparative
# RBS: adverb, superlative
# RP: particle


# POS: genitive marker
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




filepath = "messages.htm"
file = open(filepath, "r")
dom = file.read()
dom = unescape(dom)
file.close()

regex = re.compile('<div class="message_header"><span class="user">[^<]*</span><span class="meta">[^<]*</span></div></div><p>[^<]*')
listOfMessages = regex.findall(dom)

regex = re.compile('<div class="message_header"><span class="user">[^<]*')
# length of fixed string, 47
regex2 = re.compile('class="meta">[^<]*')
# length of fixed string, 13
regex3 = re.compile('<p>[^<]*')

listOfMessages = list(filter(lambda subdom: (regex.findall(subdom)[0][47:] in names), listOfMessages))

def formatMessage(subDom):
    date = dateParse(regex2.findall(subDom)[0][13:]).date()
    message = pos_tag(word_tokenize(regex3.findall(subDom)[0][3:]))
    return {'date' : date, 'message' : message}

listOfMessages = list(map(formatMessage, listOfMessages))



months = {}

for entry in listOfMessages:
    if (str(entry["date"].day) + "-" + str(entry["date"].month) + "-" + str(entry["date"].year)) not in months:
        months[str(entry["date"].day) + "-" + str(entry["date"].month) + "-" + str(entry["date"].year)] = copy.deepcopy(releventWordClassesList)
    for word in entry["message"]:
        #one word can have multiple tags, but then will have multiple tuplets
        if ("ENG_" + word[1]) in releventWordClasses:
            for tup in months[str(entry["date"].day) + "-" + str(entry["date"].month) + "-" + str(entry["date"].year)]:
                if tup[0] == ("ENG_" + word[1]):
                    tup[1] = tup[1] + 1

# print(months)

filepath = "wordTagsByMonth.csv"
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
