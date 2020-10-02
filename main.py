import csv
import re
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from gensim.parsing import remove_stopwords

spamlist = []
hamlist = []

def writeFile(randomList, name):
    w = csv.writer(open(name, 'w'))
    for key, value in randomList.items():
        w.writerow([key, value])


def word_count(lst):
    counts = dict()
    for item in lst:
        words = word_tokenize(item)
        for word in words:
            if word in counts:
                counts[word] += 1
            else:
                counts[word] = 1
    return counts


def stemSentence(sent):
    stem = PorterStemmer()
    token_words = word_tokenize(sent)
    stem_sentence = []
    for word in token_words:
        stem_sentence.append(stem.stem(word))
        stem_sentence.append(" ")
    return "".join(stem_sentence)


with open('sms-spam-corpus.csv', newline='') as f:
    reader = csv.DictReader(f, delimiter=',')
    for row in reader:
        if row['v1'] == 'spam':
            spamlist.append(stemSentence(remove_stopwords(re.sub(r'[^A-Za-z]+', r' ', row['v2']).lower())))
        else:
            hamlist.append(remove_stopwords(re.sub(r'[^A-Za-z]+', r' ', row['v2']).lower()))
    spamdict = word_count(spamlist)
    hamdict = word_count(hamlist)
field_names = ['word', 'count']
# writeFile(spamdict, 'spamdict.csv')
# writeFile(hamdict, 'hamdict.csv')
# print(spamlist)
# print(hamlist)
# print(spamdict)
# print(hamdict)
amountOfHamSen= len(hamlist)
amountOfSpamSen = len(spamlist)
all_sen = amountOfHamSen + amountOfSpamSen
P_Ham = amountOfHamSen / all_sen
P_Spam = amountOfSpamSen / all_sen
print("P(ham) =  ", P_Ham, "\nP(spam) = ", P_Spam)
s = input()
l = s.split()
sumS = 0
sumH = 0
prH = 1
prS = 1
i = 0
for word in spamdict:
    sumS += spamdict[word]
for word in hamdict:
    sumH += hamdict[word]
print(sumS)
print(sumH)
for word in l:
    if word in spamdict:
        prS *= (spamdict[word]/sumS)
    else:
        if word in hamdict:
            i += 1
            prS *= ((hamdict[word]+1)/(sumH+i))
        else:
            i += 1
            prS *= (1/(sumH+i))
pSBTxt = P_Spam*prS
print(pSBTxt)
for word in l:
    if word in hamdict:
        prH *= (hamdict[word]/sumH)
    else:
        if word in spamdict:
            i += 1
            prH *= ((spamdict[word]+1)/(sumS+i))
        else:
            i += 1
            prH *= (1/(sumS+i))
pHBTxt = P_Ham*prH
print(pHBTxt)
print(pSBTxt / (pHBTxt + pSBTxt))
print(pHBTxt / (pHBTxt + pSBTxt))
if pSBTxt > pHBTxt:
    print("this is spam")
else:
    print("this is ham")

