# -*- coding: utf-8 -*-

import numpy as np
import random
#import itertools
#import time
import copy



class Knapsack:
    def __init__(self):
        #---インスタンスは共通---#
        self.N=0
        self.weights=[]
        self.values=[]
        self.capacity=0

    #--------branch and bound　で使う----------#
        self.results=[] #暫定解
        self.obj=0 #暫定解の目的関数値
    #--------1/2-近似解法　で使う----------#
        self.results_apx=[] 
        self.obj_apx=0 
        

    def decide_num_of_item(self):
        
        while 1:
            self.N = int(input('# of items='))
            #self.N = 30
            if self.N <10:
                print('# of items >=10')
            else:
                break
    def fix_N(self):
        self.N=4
        

    def make_instance(self): #インスタンスを降順にして表示
        weights=[np.random.randint(1, 60) for i in range(self.N)]
        values=[np.random.randint(1, 60) for i in range(self.N)]
        self.ratios= [float(values[i])/weights[i] for i in range(self.N)]
        for i in np.argsort(self.ratios)[::-1]:
            self.values.append(values[i])
            self.weights.append(weights[i])
        self.ratios.sort(reverse=True)
        self.capacity=max(self.weights)*self.N/6
        for i in range(self.N):
            print ('item[%d]:value=%d, weight=%d, ratio=%f' % (i,self.values[i],self.weights[i],self.ratios[i]))
        print ('capacity=%d' % (self.capacity))


    def init_results(self):
        for i in range(self.N):
            self.results.append(0)
            
    

    def __judgeValue(self,fixed_list):
        evaluate_list =[] #採択したxの判定を格納
        evaluate_list.extend(fixed_list)
        weight_sum=0
        #固定リストの重さの合計を最初に計算
        for i in range(len(fixed_list)):
            weight_sum+= fixed_list[i]*self.weights[i]
        if len(fixed_list) == self.N: #全てのxが固定されている時
            if (weight_sum<=self.capacity) and (np.dot(np.array(fixed_list),np.array(self.values)) > self.obj):
                self.results=fixed_list #暫定解の更新
                self.obj=np.dot(np.array(fixed_list),np.array(self.values))
                return False
            else:
                return False #端まで来たので分岐終了 
        else:#固定されていないxがある時
        #そもそも受け取ったリストではすでに容量オーバーのとき
            if weight_sum > self.capacity:
                return False #この先に許容解なし、分岐終了
            elif weight_sum==self.capacity:#容量ぴったりの時
                #この先は全て０が許容解
                for i in range(len(fixed_list),self.N):
                    evaluate_list.append(0)
                if np.dot(np.array(evaluate_list),np.array(self.values))> self.obj :#この解が暫定解より良い時
                    self.results=evaluate_list #暫定解の更新
                    self.obj=np.dot(np.array(evaluate_list),np.array(self.values))
                    return False
                else: #暫定値を超えていない
                    return False #この先に許容解はないので終了
            else:
            #容量に余裕ありの時
            #緩和問題の解を用いて枝刈りをする
                for i in range(len(fixed_list),self.N):#greedyに採択を決定
                    if weight_sum+self.weights[i]<self.capacity: #１入れてもまだ容量に余裕ありの時
                        evaluate_list.append(1)
                        weight_sum+=self.weights[i]
                    else:
                        #0<X<=1になる時
                        rate=(self.capacity-weight_sum)/float(self.weights[i])
                        evaluate_list.append(rate)
                        weight_sum +=self.weights[i]*rate
                        for i in range(len(evaluate_list),self.N):#以降は全て０
                            evaluate_list.append(0)
                            
                        #最後に追加したアイテムがx=1となった時、evaluate_listは整数解なので暫定解より良いのかチェック
                        if rate==1:
                            if np.dot(np.array(evaluate_list),np.array(self.values))> self.obj :#この解が暫定解より良い時
                                self.results=evaluate_list #暫定解の更新
                                self.obj=np.dot(np.array(evaluate_list),np.array(self.values))
                                return False #分岐終了
                            else:#これ以上先に良い解なし
                                return False #分岐終了
                        else:#LPの解が非整数解
                            if np.dot(np.array(evaluate_list),np.array(self.values))> self.obj :#LPの解が暫定解より良い時
                                return True #分岐継続
                            else: #暫定解を超えていない
                                return False #この先を探す意味ないので終了
                

    def depthFirstSearch(self):
        search_lists=[[0],[1]]
        while len(search_lists) !=0:
            first_list = search_lists[0]
            search_lists.pop(0)
            if self.__judgeValue(first_list):
                new_list_cp = copy.deepcopy(first_list)
                new_list_cp.append(1)
                search_lists.insert(0,new_list_cp)
                new_list_cp=copy.deepcopy(first_list)
                new_list_cp.append(0)
                search_lists.insert(0,new_list_cp)
        print('')
        print ("---------分枝限定法---------")
        print ('最適値=%d' %(self.obj))
        print (self.results)
      #  print (np.dot(np.array(self.results),np.array(self.weights)))
        
          
    #--------近似解法-------#
    def improved_greedy(self):
        #step1: greedy法
        sum_w=0
        sum_w2=0
        results1=[]

        for i in range(self.N):
            if sum_w+ self.weights[i]<=self.capacity:
                results1.append(1)
                sum_w += self.weights[i]
            else:
                results1.append(0)

        #step2: step1で0になったアイテムの中でもっとも効率の良いものを１に固定して貪欲法を実行
        results2=[]
        for i in range(self.N):
            if results1[i]==0:
                results2.append(1)
                sum_w2=self.weights[i]
                for j in range(i+1,self.N):
                    results2.append(0)
                break
            else:
                results2.append(0)

        for i in range(self.N):
            if results2[i]==0:
                if sum_w2+self.weights[i]<=self.capacity:
                    results2[i]=1
                    sum_w2 += self.weights[i]
                else:
                    results2[i]=0

        #print (results2)
        #よかった方を出力
        if np.dot(np.array(results1),np.array(self.values))>np.dot(np.array(results2),np.array(self.values)):
            self.results_apx.extend(results1)
        else:#step2の方がよかったら
            self.results_apx.extend(results2)
            
        self.obj_apx=np.dot(np.array(self.results_apx),np.array(self.values))
        
        print ('--------1/2-近似解法--------')
        print ('目的関数値＝%d' %(self.obj_apx) )
        print ('近似比=%f' %(self.obj_apx/self.obj))
        print (self.results_apx)
        
       # print (np.dot(np.array(self.results_apx),np.array(self.weights)))
                
     
if __name__=="__main__":           
    bb = Knapsack()
    #bb.fix_N()
    bb.decide_num_of_item()
    bb.make_instance()
    bb.init_results() 
    bb.depthFirstSearch()
    bb.improved_greedy()
    
