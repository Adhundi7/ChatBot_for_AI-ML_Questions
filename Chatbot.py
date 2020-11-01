from Bot_2.generatengrams import *

def ngrams_matcher(inp, topic):
     my_que_data = database('Bot_2/ques/' + topic)
     my_ans_data = database('Bot_2/ans/' + topic)
     sc_que = my_que_data.score(inp)
     sc_ans = my_ans_data.score(inp)
     scq = sorted(sc_que, key=lambda tup: tup[0])
     sca = sorted(sc_ans, key=lambda tup: tup[0])

     tot_score = [(sca[i][0] , (7*scq[i][1])+(3*sca[i][1])) for i in range(len(scq))]

     best_q = sorted(tot_score, key=lambda tup: tup[1])
     best_ans = best_q[-1][0]
     return best_q, best_ans

