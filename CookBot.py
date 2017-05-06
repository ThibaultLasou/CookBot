import enum
import treetaggerwrapper

verbManger = ["manger", "affamer"]
exprManger = [("avoir", "faim", "dalle")]
knownIngredients = ["pomme", "pâte", "orange"]
numbers = {}


class Request:
    def __init__(self):
        self.nom = ""
        self.foodType = ""
        self.availableIngredients = []
        self.culture = ""
        self.nbEaters = 0
        self.prepTime = 0
        self.cookTime = 0
        self.isSet  = {"foodType" : False, "culture" : False, "nbEaters" : False, "availableIngredients" : False}
        self.Results = []

    def fillRequest(self, tagW):
        for i in range(0,len(tagW)):
            w = tagW[i]
            if w.posTag == "NOM":
                if i>0 and tagW[i-1].posTag == "NUM":
                   for kI in knownIngredients:
                       if w.lemma == kI:
                           self.availableIngredients.append((int(tagW[i-1].word), w.lemma))
                           break;

    def printRequest(self):
        print(self.availableIngredients)
        
def eatingIntention(tagW):
    for w in taggedWords:
        if w.posTag[0:3] == "VER":
            for verb in verbManger:
                if w.lemma == verb:
                    return True
    return False
                
class TreeTaggerWord:
    def __init__(self, triplet):
        self.word, self.posTag, self.lemma = triplet

def formatTTG(output):
    words=[]
    for w in output:
        words.append(TreeTaggerWord(w.split("\t")))
    return words

def postTreatment(TW):
    for w in TW:
        if w.posTag == "NUM" and w.lemma != "@card@":
            try:
                w.word = numbers[w.word]
            except:
                ans = input("Je ne comprends pas bien ce nombre : " + w.word + ". Pourriez-vous l'écrire en chiffres ?\n")
                taggedAns = formatTTG(tagger.TagText(ans))
                for wAns in taggedAns:
                    if wAns.posTag == "NUM" and wAns.lemma == "@card@":
                        numbers[w.word] = int(wAns.word)
                        w.word = numbers[w.word]
    return TW
    
tagger = treetaggerwrapper.TreeTagger(TAGLANG='fr', TAGDIR='./Ressources', TAGINENC='utf-8', TAGOUTENC='utf-8')
demande = input("Bonjour ! Que puis-je pour vous aujourd'hui ?\n")
taggedWords = formatTTG(tagger.TagText(demande))
taggedWords = postTreatment(taggedWords)

if(eatingIntention(taggedWords)):
    r = Request()
    r.fillRequest(taggedWords)
    r.printRequest()
