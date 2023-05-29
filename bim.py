
import math
class bim:
    def __init__(self,term, term_detail,txt):
        self.docs = txt
        self.term = term
        self.term_detail = term_detail
        self.post = self.posting()
    
 

    
    
    def posting (self):
        '''
        Ntd: số tài liệu chứa term docs
        N: tổng số tài liệu
        p(tqi|r,q)=0.5
        p(td|-r,q)=Ntd/N
        wtd=log(0.5*N/Ntd)
        
        '''
        words = {}
        for i in self.term:
            words[i] = {
                "d" : 0.5,
                "-d": self.term[i]["So_luong_tai_lieu"] / len(self.docs),
                "w":  math.log(0.5*len(self.docs)/self.term[i]["So_luong_tai_lieu"],2)

            }
        
        self.post = words
        return words
    
    def posting_update(self, results, query):
        '''
       khi có bộ dữ liệu mẫu
       p(td|r,q) = (rtd+0.5)/(NR+1)
       p(td|-r,q) = (Ntd-rtd+0.5)/(N-NR+1)

       rtd: só tài liệu liên quan chứa term td
       Nr: số tài liệu liên quan 
       Ntd: số lần xuất hiện của term

        '''
        post = self.post
        Nr = len(results)
        for word in query:
            rtd = 0
            Ntd = 0
            if(word in self.term_detail): 
                for docs in results:
                    if docs in self.term_detail[word]: rtd+=1
                Ntd = self.term[word]["Tan_so"]
            else: post[word] = {}
    
            post[word]["d"] = (rtd+0.5)/ (len(results) + 1)
            post[word]["-d"] = (Ntd - rtd + 0.5 ) / (len(self.docs) - len(results) + 1)
            post[word]["w"] = math.log((rtd+0.5)* (len(self.docs) - len(results) + 1)) / ((len(results) + 1)*(Ntd - rtd + 0.5 ))



            







    
    def rel(self,words):
        '''
        len từ 0->1400 self.docs
        '''
        rel = {}
        for i in range(0,len(self.docs)) :
            score = 0
            for word in words:
                if word in self.docs[i]:
                    score += self.post[word]["w"]
            rel[i+1] = score
        return sorted(rel.items(),key=lambda x:x[1],reverse = True)
    

  


