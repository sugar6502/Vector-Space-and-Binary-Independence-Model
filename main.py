from math import log, sqrt
import re
import numpy as np
import glob
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from bim import bim
from evaluation import EvaluationMetrics



numbers = re.compile(r'(\d+)')

def numericalSort(value):
    '''
    đọc theo số thứ tự file txt
    '''
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

def loc_chu_so(url):
    '''
    xóa các số trong văn bản
    '''
    txt = []
    for i in sorted(glob.glob(url),key=numericalSort):  #lọc chữ số
        with open(i) as f:
            lines = f.readlines()
            if len(lines) == 0: lines = " "
            char_str = ['' .join((z for z in lines[0] if not z.isdigit())).lower()]
            txt.extend(char_str)
    return txt

def tien_xu_ly(i):
    '''
    Xóa các stopwords, đưa về từ gốc, tách từ
    '''
    tokenizer = RegexpTokenizer(r'\w+')
    lemmatizer=WordNetLemmatizer()
    stop = set(stopwords.words("english"))

    temp = tokenizer.tokenize(i)
    output = [w for w in temp if not w in stop]
    #temp_stem=[stemmer.stem(word) for word in output]
    temp_stem=[lemmatizer.lemmatize(word) for word in output]
    final = [word for word in temp_stem if wordnet.synsets(word)]
    final_final = [word for word in final if not len(word)<3]
    #final_final = [word for word in temp_stem if not len(word)<3]
    return final_final

def make_docs(txt):
    docs = []
    for i in txt:
        docs.append(tien_xu_ly(i))
    return docs


def make_term(txt_term):

    '''
    tạo thành các term có dạng là một dict, từ -> số lượng tài liệu chứa nó, tần số lặp từ đó trong tất cả tài liệu. Vd:
    'deepest' : {So_luong_tai_lieu: 1,
                 Tan_so: 2
                }
    '''
    words = {}
    for i in txt_term:
        final_final=tien_xu_ly(i)
        for word in final_final:
            if word not in words: 
                words[word] = {
                "So_luong_tai_lieu" : [txt_term.index(i)+1], 
                "Tan_so" : 1
                }

            else:
                words[word]["Tan_so"]+=1
                current_index = txt_term.index(i)+1
                if current_index not in words[word]["So_luong_tai_lieu"]: 
                    words[word]["So_luong_tai_lieu"].append(current_index)
    for i in words:
        words[i]["So_luong_tai_lieu"] = len(words[i]["So_luong_tai_lieu"])
    return words

def make_detail_term(txt_term):
    '''
    Chi tiết về term đó, từ -> số Id docs: số lần lặp trong doc đó. Vd
    conceived: {
                1016: 1
                1268: 1
    }
    
    '''
    words = {}
    for i in txt_term:
        final_final=tien_xu_ly(i)
        current_index = txt_term.index(i)+1
        for word in final_final:
            if word not in words:
                words[word] = {}

            if current_index not in words[word]:
                words[word][current_index] = 1
            else:
                words[word][current_index] +=1

    return words         






##################### Main


txt = loc_chu_so('./Cranfield/*')



term = make_term(txt)
detail_term = make_detail_term(txt)
xs = bim(term,detail_term,make_docs(txt))

####Query
with open("query.txt") as f:
    lines = f.readlines()
    query_full = []
    for i in lines:
        query_full.append('' .join((z for z in i if not z.isdigit())).lower())
#query1 = tien_xu_ly(query_full[0])



####lấy file results
result = []
for i in sorted(glob.glob('./RES/*'),key=numericalSort):  #lọc chữ số
    temp = []
    with open(i) as f:
        lines = []
        read = f.readlines()
        for i in read:
            lines.append(i.split(" ")[-1].split("\t")[0])
        temp.extend(lines)
    result.append(temp)




#xs.posting_update(result[0], query1)
#rank_query1 = xs.rel(query1)


##eva


#####
# for i in query_full:
#     query = tien_xu_ly(i)
#     xs.posting_update(result[query_full.index(i)], query)


score = []
for i in query_full:
    query = tien_xu_ly(i)
    rank_query = xs.rel(query)
    score.append(EvaluationMetrics(rank_query,result[query_full.index(i)]).cal_precision())


# query1 = tien_xu_ly(query_full[2])
# rank_query1 = xs.rel(query1)


#eva = EvaluationMetrics(rank_query1,result[2])
#print(score)
print(np.mean(score))
