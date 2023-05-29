import numpy as np





class EvaluationMetrics:
    def __init__(self,ranks, results ):
        self.precision = 0
        self.ranks = ranks
        self.results = results

    def cal_precision(self):
        '''
        hàm tính precision không nội suy
        sử dụng phương pháp cắt n=5,10 với trọng số tương đương nhau = 1/2
        
        '''
        pre = []
        count = 0
        for i in self.ranks[0:10]:
            #print(i)
            if str(i[0]) in self.results:
                count+=1
                
                
            if self.ranks.index(i) == 4: pre.append(count/5)
        
        pre.append(count/10)
        return np.mean(pre)





        


