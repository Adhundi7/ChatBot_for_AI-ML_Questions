import os
import math
limit = 3

def ngrams(lines):
    global limit
    ngrams = []
    for i in range(1, limit+1):
        ndict = {}
        for line in lines:
            nline = ['<START>'] + line + ['<END>']
            for x in range(len(nline)-i +1) :
                key = '_'.join(nline[x:x+i])
                if key in ndict.keys():
                    ndict[key] += 1
                else:
                    ndict[key] = 1
        ngrams += [ndict]
    return ngrams

def cleanLines(lines):
    for i in range(len(lines)):
        lines[i] = lines[i].split()
        for x in range(len(lines[i])):
            lines[i][x] = lines[i][x].lower()
    return lines

class database:
    def __init__(self, folder):
        ngramsdict = {}
        path = './' +folder +'/'
        for fil in os.listdir(path):
            with open(path + fil) as f:
                lines = f.readlines()
            lines = cleanLines(lines)
            ngramsdict[(fil.split('.')[0])] = ngrams(lines)
        self.ngramdictionary = ngramsdict

    def ans_containing(self, token, i):
        n = 0
        for key in self.ngramdictionary:
            if token in self.ngramdictionary[key][i].keys():
                n += 1
        return n
    
    def score(self,uinput):
        scores = [] 
        uinput =[uinput.lower().split()]
        my_question = ngrams(uinput)
        total_ans = len(self.ngramdictionary)
        for key in self.ngramdictionary:
            cur_intent_dict = self.ngramdictionary[key]
            fscore = 0.0
            for i in range(3):
                cur_dict, ansdict = my_question[i], cur_intent_dict[i]
                totaltokens = sum([ansdict[key] for key in ansdict])
                current_rel = 0.0
                for j in cur_dict:
                    if j in ansdict.keys():
                        tf = cur_dict[j]*ansdict[j]/totaltokens
                        idf = math.log(total_ans/ self.ans_containing(j, i))
                        #print('word ', j, 'tf ', tf, 'idf ', idf)
                        current_rel += tf*idf
                fscore += (5**(i))*(current_rel)
            scores+= [(key,fscore)]
        return scores
    
    def matchintent(self, uinput):
        a = sorted(self.score(uinput), key=lambda tup: tup[1])
        return a[-1][0]