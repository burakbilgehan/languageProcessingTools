from snowballstemmer import stemmer
import nltk
from nltk.tokenize import RegexpTokenizer
import sys, os
import codecs
#from num2words import num2words
from random import randint

myfiles = []
kokbul1 = stemmer('turkish')
kelimeler = []
tokenizer = RegexpTokenizer(r'\w+')
sesli = ["a", "e", "ı", "i", "o", "ö", "u", "ü", "â", "î", "û"]
sessiz = ["b", "c", "ç", "d", "f", "g", "ğ", "h", "j", "k", "l", "m", "n", "p", "r", "s", "ş", "t", "v", "y", "z"]
alphabet = list(set(sesli).union(sessiz))
#alphabet.sort()

#içinde bulunduğun klasördeki dosyaları myfiles globaline ekler
def path_bul():
    print('sys.argv[0] =', sys.argv[0])
    pathname = os.path.dirname(sys.argv[0])
    print('path =', pathname)
    print('full path =', os.path.abspath(pathname))
    full_path = os.path.abspath(pathname)
    for dirpath, dirnames, filenames in os.walk(full_path):
        for x in filenames:
            if (x[-1] == "t"):
                myfiles.append(x)

#verilen metitndeki kelimeleri global değişkene kaydeder
def add_kelime(my_file):
    print("current file is ", my_file)
    with open(my_file, 'r', encoding='utf-8') as dosya:
        metin = dosya.read()
        for i in nltk.word_tokenize(metin):
            mystr = i
            mystr1 = tokenizer.tokenize(mystr)
            if not (mystr1 == []):
                for x in range(0, len(mystr1)):
                    mystr1[x] = mystr1[x].lower()
            for x in mystr1:
                if x not in kelimeler:
                    kelimeler.append(x)

#global değişkendeki kelimeleri yazdırır
def create_words():
    for i in myfiles:
        add_kelime(i)
    kelimeler.sort()
    all_words = codecs.open("allwords.txt", "w", encoding='utf-8')
    for i in kelimeler:
        all_words.write(i + '\n')
    all_words.close()

#add_kelime'nin aynısı
def getWordsFromPlainText(pathToFile):
    with open(pathToFile, 'r', encoding='utf-8') as dosya:
        metin = dosya.read()
        for i in nltk.word_tokenize(metin):
            mystr = i
            mystr1 = tokenizer.tokenize(mystr)
            if not (mystr1 == []):
                for x in range(0, len(mystr1)):
                    mystr1[x] = mystr1[x].lower()
            for x in mystr1:
                if x not in kelimeler:
                    kelimeler.append(x)

#verilen kelimeyi hecelere böler
def hecele(mystr):
    mystr = mystr.rstrip()
    for x in mystr:
        if (x not in sesli) and (x not in sessiz):
            return None
    if mystr == "aort":
        return ["a", "ort"]
    elif len(mystr) == 2:
        return [mystr]
    elif len(mystr)>2:
        if len(mystr) == 3:
            if (mystr[0] in sessiz) and (mystr[1] in sessiz):
                return [mystr]
            elif (mystr[1] in sessiz) and (mystr[2] in sessiz):
                return [mystr]
            elif (mystr[0] in sesli) and (mystr[2] in sesli):
                return [mystr[0], mystr[1:]]
            elif (mystr[0] in sesli) and (mystr[1] in sesli):
                return [mystr[0], mystr[1:]]
            elif (mystr[1] in sesli) and (mystr[2] in sesli):
                return [mystr[:2], mystr[-1]]
            else:
                return [mystr]
        else:
            checkpts = []
            for i in range(0, len(mystr)-1):
                if (mystr[i] in sessiz) & (mystr[i+1] in sesli):
                    checkpts.append(i)
                elif ((mystr[i] in sesli) & (mystr[i+1] in sesli)):
                    checkpts.append(i+1)
            if len(checkpts) != 0:
                if (mystr[0] in sessiz) & (mystr[1] in sessiz):
                    checkpts[0] = 0
                if (checkpts[0] != 0):
                    checkpts = [0] + checkpts
            results = []
            if len(checkpts)!=0:
                for i in range(0, len(checkpts)-1):
                    results.append(mystr[checkpts[i]:checkpts[i+1]])
                results.append(mystr[checkpts[-1]:])
                return results
            else:
                return None
    else:
        return [mystr]


def findNonTurkish(mystr):
    try:
        hecele(mystr)
        return True
    except:
        return False

#hecelenemeyen (türkçe olmayan) kelimeleri atar
def checkNonTurkish(inputf, outputf):
    words = []
    with open(inputf, 'r', encoding='utf-8') as dosya:
        metin = dosya.readlines()
        for x in metin:
            if hecele(x)!=None:
                words.append(x)
    correctWords = codecs.open(outputf, "w", encoding='utf-8')
    for i in words:
        correctWords.write(i)
    correctWords.close()

#zargan sözlükteli tüm türkçe kelimeleri alır
def takeWordsZargan(inf, ouf):
    words = []
    with open(inf, 'r', encoding='utf-8') as dosya:
        metin = dosya.readlines()
        print("there are ", len(metin), " words")
        cnt = 0
        for x in metin:
            if cnt%1000 == 0:
                print(cnt)
            cnt = cnt + 1
            x = x.split()
            mystr1 = tokenizer.tokenize(x[0])
            if not (mystr1 == []):
                for y in range(0, len(mystr1)):
                    mystr1[y] = mystr1[y].lower()
                    words.append(mystr1[y])
    correctWords = codecs.open(ouf, "w", encoding='utf-8')
    words.sort()
    for i in words:
        correctWords.write(i + '\n')
    correctWords.close()

def takeWords(inf, ouf):
    sentences = []
    with open(inf, 'r', encoding='utf-8') as dosya:
        metin = dosya.readlines()
        print("there are ", len(metin), " lines")
        cnt = 0
        for x in metin:
            if cnt%1000 == 0:
                print(cnt)
            cnt = cnt + 1
            x = x.split()
            mystr1 = tokenizer.tokenize(x)
            if not (mystr1 == []):
                for y in range(0, len(mystr1)):
                    mystr1[y] = mystr1[y].lower()
                    #sentences.append(mystr1[y])
    #correctWords = codecs.open(ouf, "w", encoding='utf-8')
    #words.sort()
    """
    for i in words:
        correctWords.write(i + '\n')
    correctWords.close()
    """

#kopya kelimeleri çıkartır
def removeDuplicates(inf, ouf):
    words = []
    words.append(" ")
    with open(inf, 'r', encoding='utf-8') as dosya:
        metin = dosya.readlines()
        print("there are ", len(metin), " words")
        cnt = 0
        for x in metin:
            x = x.rstrip()
            if cnt % 1000 == 0:
                print(cnt)
            cnt = cnt + 1
            if x != words[-1]:
                words.append(x)
    correctWords = codecs.open(ouf, "w", encoding='utf-8')
    words.sort()
    for i in words:
        correctWords.write(i + '\n')
    correctWords.close()

#verilen dosya listesindeki dosyaları tek dosyada birleştirip kopyaları atar
def mergeFiles(mylist, newFile):
    words = []
    for x in mylist:
        with open(x, 'r', encoding='utf-8') as dosya:
            metin = dosya.readlines()
            for y in metin:
                y = y.rstrip()
                words.append(y)
    words.sort()
    finalwords = []
    for x in range(1, len(words)):
        if words[x] != words[x-1]:
            finalwords.append(words[x])
    myfile = codecs.open(newFile, "w", encoding='utf-8')
    for x in finalwords:
        myfile.write(x + '\n')
    myfile.close()

#verilen dosyadaki metni hecelere bölüp içindeki tüm heceleri ouf ile belirtilen adrese yazar
def heceYarat(inf, ouf):
    heceler = []
    with open(inf, 'r', encoding='utf-8') as dosya:
        metin = dosya.readlines()
        cnt = 0
        for y in metin:
            if cnt%10000 == 0:
                print(cnt)
            cnt = cnt+1
            y = y.rstrip()

            try:
                hece = hecele(y)
                for x in hece:
                    if x not in heceler:
                        heceler.append(x)
            except:
                continue
    heceler.sort()
    myfile = codecs.open(ouf, "w", encoding='utf-8')
    for x in heceler:
        myfile.write(x + '\n')
    myfile.close()

# verilen metni 5-60 kelimelik cümlelere bölerek satırlara yazar
def metinBol(myfile):
    senSize = 0
    newArr = []
    newSen = ""
    for x in myfile:
        tokens = nltk.tokenize.sent_tokenize(x)
        #print(tokens, " \nlength:", len(tokens))
        for x in tokens:
            words = x.split()
            #print(len(words))
            if senSize+len(words)<60:
                senSize = senSize+len(words)
                newSen = newSen + " " + x
            if senSize>randint(5, 50):
                newArr.append(newSen)
                senSize = 0
                newSen = ""
    # print(len(newArr))
    # for x in newArr:
    #     print(x + "\n")
    return newArr

def metinBol2(myfile):
    newArr = []
    for x in myfile:
        tokens = nltk.tokenize.sent_tokenize(x)
        #print(tokens, " \nlength:", len(tokens))
        for x in tokens:
            newArr.append(x)
    # print(len(newArr))
    # for x in newArr:
    #     print(x + "\n")
    return newArr

#verilen dosyayı okuyup return eder
def metinOku(mypath):
    metin = []
    with open(mypath, 'r', encoding='utf-8') as dosya:
        tmp = dosya.readlines()
        for y in tmp:
            metin.append(y.rstrip())
    return metin

# verilen değişkeni (myfile), verilen adrese (mypath) yazar
def metinYaz(mypath, myfile):
    newfile = codecs.open(mypath, "w", encoding='utf-8')
    for x in myfile:
        newfile.write(x + '\n')
    newfile.close()

def sadelestir(metin):
    newfile = codecs.open("metinler_sade.txt", "w", encoding='utf-8')
    for x in metin:
        x = x.lower()
        tmp = []
        for y in tokenizer.tokenize(x):
            try:
                tmp.append(num2words(int(y), lang='tr'))
            except:
                tmp.append(y)
        for x in tmp:
            print(x)
            try:
                for y in hecele(x):
                    newfile.write(y)
                    newfile.write(" ")
            except:
                print("xxxxxxxxxxx")
        newfile.write("\n")
        

def acousticParser(inp):
    cnt = 1
    cumleler = []
    current = ""
    for x in inp:
        try:
            if int(x) == cnt:
                print("true")
                cnt = cnt + 1
                cumleler.append(current)
                current = ""
        except:
            current = current + x + " "
    return cumleler
#def sayiYazi(myNumber):

def acousticYap(metin, args):
    fileids = codecs.open("turkce_train.fileids", "w", encoding='utf-8')
    trans = codecs.open("turkce_train.transcription", "w", encoding='utf-8')
    for y in args:
        cnt = 1
        for x in metin:
            x = x.rstrip()
            tra = "<s> " + x + " </s> (" +  str(cnt) + ")"
            filei = y + "/" + str(cnt)
            trans.write(tra + "\n")
            fileids.write(filei + "\n")
            cnt = cnt + 1
    fileids.close()
    trans.close()

def dictYap(metin):
    nMetin = codecs.open("turkce.dic", "w", encoding='utf-8')
    for x in metin:
        cnt = 0
        x = x.rstrip()
        tmp = x + " "
        for y in x:
            if cnt == 0:
                if y != "ğ":
                    tmp = tmp + y + " "
            else:
                if y != "ğ":
                    tmp = tmp + y + " "
                else:
                    tmp = tmp + x[cnt-1] + " "
            cnt = cnt + 1
        nMetin.write(tmp + "\n")
    nMetin.close()

def findWordsConsisting(myfile, myarr):
    diff = list(set(alphabet) - set(myarr))
    print(diff)
    ret = []
    for x in myfile:
        flag = 0
        for y in x:
            if y in diff:
                flag = 1
        if flag == 0:
            ret.append(x)
    return ret


# path_bul()
# create_words()
# print(findNonTurkish("burakkkkk"))
# checkNonTurkish("allwords.txt", "correctwords.txt")
# print(hecele("khlj"))
# takeWordsZargan("zargan.txt", "zarganwords.txt")
# removeDuplicates("zarganwords.txt", "zarganNoDup.txt")
# mergeFiles(["correctwords.txt", "zarganNoDup.txt"], "mergedWords.txt")
# heceYarat("mergedWords.txt", "heceler.txt")
# print(num2words(2001942, lang='tr'))

#path_bul()
#newfile = codecs.open("cumleler2", "w", encoding='utf-8')
#for x in myfiles:
#    if x[-1] == "t":
#        metin = metinOku(x)
#        nMetin = metinBol2(metin)
#        for y in nMetin:
#            newfile.write(y.lower() + "\n")
#        print("finished writing ", x)
#newfile.close()

#metin = metinOku("cumleler2")
#sadelestir(metin)

#metin = metinOku("turkce.dict")
#dictYap(metin)
#nMetin = acousticParser(metin)
#sadelestir(nMetin)
metin = metinOku("mergedWords.txt")
#acousticYap(metin, ["burak", "mehmet", "omer"])
print(alphabet)
ret = findWordsConsisting(metin, ["a", "e", "l", "k"])
print(ret)