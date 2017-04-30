import json
import csv
import ast

academicDict = {}

with open('output/Academic/EnglishAcademicStats.txt', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
    academicDict['english'] = {}
    for row in spamreader:
        academicDict['english'][row[0]] = ast.literal_eval(row[1])

with open('output/Academic/FrenchAcademicStats.txt', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
    academicDict['french'] = {}
    for row in spamreader:
        academicDict['french'][row[0]] = ast.literal_eval(row[1])

with open('output/Academic/GermanAcademicStats.txt', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
    academicDict['german'] = {}
    for row in spamreader:
        academicDict['german'][row[0]] = ast.literal_eval(row[1])

with open('output/Academic/PortugueseAcademicStats.txt', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
    academicDict['portuguese'] = {}
    for row in spamreader:
        academicDict['portuguese'][row[0]] = ast.literal_eval(row[1])

with open('output/Academic/RussianAcademicStats.txt', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
    academicDict['russian'] = {}
    for row in spamreader:
        academicDict['russian'][row[0]] = ast.literal_eval(row[1])

with open('output/Academic/SpanishAcademicStats.txt', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
    academicDict['spanish'] = {}
    for row in spamreader:
        academicDict['spanish'][row[0]] = ast.literal_eval(row[1])


for language in academicDict:
    red = academicDict[language]["word_count_with_redundancies"]
    ratio = 10000 / red
    for key in academicDict[language]:
        if type(academicDict[language][key]) == dict:
            for lang in academicDict[language][key]:
                academicDict[language][key][lang] = round(academicDict[language][key][lang]*ratio)
        else:
            academicDict[language][key] = round(academicDict[language][key]*ratio)

print(json.dumps(academicDict))
