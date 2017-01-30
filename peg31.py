# -*- coding: utf-8 -*-

import numpy as np
import random
#import itertools
import time
import copy



class Knapsack:
    def __init__(self):
        #---インスタンスは共通---#
        self.N=0
        self.weights=[]
        self.values=[]
        self.capacity=0
        self.num_of_nodes=0

    #--------branch and bound　で使う----------#
        self.results=[] #暫定解
        self.obj=0 #暫定解の目的関数値
    #--------1/2-近似解法　で使う----------#
        self.results_apx=[] 
        self.obj_apx=0 
        self.time=0
        
        
        
        #peg#
        self.results=[]
        self.unfixed=[] #未決定の番号を格納
        self.new_weights=[]
        self.new_values=[]
        self.new_ratios=[]
        self.new_capacity=0
        self.new_N=0
        self.new_results=[]

    def decide_num_of_item(self):
        
        while 1:
            self.N = int(input('# of items='))
            #self.N = 30
            if self.N <10:
                print('# of items >=10')
            else:
                break
    def fix_N(self):
        self.N=10000
        

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
            
    def pegging(self):
        print('釘付けリスト=[ ',end="")
        sum_w=0
        results1=[0]*self.N

        for i in range(self.N):
            if sum_w+ self.weights[i]<=self.capacity:
                results1[i]=1
                sum_w += self.weights[i]
            else:
               # rate=(self.capacity-sum_w)/float(self.weights[i])
                results1[i]=0


        greedy_obj=np.dot(np.array(results1),np.array(self.values))
        
        #固定されなかった番号を覚えておくリスト
        unfixed=[]
        
        for index in range(self.N):
            list=[0]*self.N
            sum_w=0
            if results1[index]==1:
                list[index]=0
            else :
                list[index]=1
            sum_w+= list[index]*self.weights[index]
            for i in range(self.N):
                if i == index:
                    continue
                else:
                    if sum_w+ self.weights[i]<=self.capacity:
                        list[i]=1
                        sum_w += self.weights[i]
                    else:
                        rate=(self.capacity-sum_w)/float(self.weights[i])
                        list[i]=rate
                        break
                

            if np.dot(np.array(list),np.array(self.values)) < greedy_obj:

                self.results[index]=results1[index]
                print(' %d'%(results1[index]),end="")
            else:
  
                unfixed.append(index)
                
                print(' *',end="")
        print(']')
        self.unfixed=unfixed
        print('# 未決定な変数/# 全変数 = %f' %(len(unfixed)/self.N))


    def change_problem(self): #釘付けされていない変数だけの問題を作成

        
        self.new_capacity=self.capacity-np.dot(np.array(self.results),np.array(self.weights))
        self.new_N=len(self.unfixed)
        
        for index in self.unfixed:
            self.new_weights.append(self.weights[index])
            self.new_values.append(self.values[index])
            self.new_ratios.append(self.values[index]/self.weights[index])
      


    def __judgeValue(self,fixed_list):
        self.num_of_nodes +=1
        
        evaluate_list =[] #採択したxの判定を格納
        evaluate_list.extend(fixed_list)
        weight_sum=0
        #固定リストの重さの合計を最初に計算
        for i in range(len(fixed_list)):
            weight_sum+= fixed_list[i]*self.new_weights[i]
        if len(fixed_list) == self.new_N: #全てのxが固定されている時
            if (weight_sum<=self.new_capacity) and (np.dot(np.array(fixed_list),np.array(self.new_values)) > self.obj):
                self.new_results=fixed_list #暫定解の更新
                self.obj=np.dot(np.array(fixed_list),np.array(self.new_values))
                return False
            else:
                return False #端まで来たので分岐終了 
        else:#固定されていないxがある時
        #そもそも受け取ったリストではすでに容量オーバーのとき
            if weight_sum > self.new_capacity:
                return False #この先に許容解なし、分岐終了
            elif weight_sum==self.new_capacity:#容量ぴったりの時
                #この先は全て０が許容解
                for i in range(len(fixed_list),self.new_N):
                    evaluate_list.append(0)
                if np.dot(np.array(evaluate_list),np.array(self.new_values))> self.obj :#この解が暫定解より良い時
                    self.new_results=evaluate_list #暫定解の更新
                    self.obj=np.dot(np.array(evaluate_list),np.array(self.new_values))
                    return False
                else: #暫定値を超えていない
                    return False #この先に許容解はないので終了
            else:
            #容量に余裕ありの時
            #緩和問題の解を用いて枝刈りをする
                for i in range(len(fixed_list),self.new_N):#greedyに採択を決定
                    if weight_sum+self.new_weights[i]<self.new_capacity: #１入れてもまだ容量に余裕ありの時
                        evaluate_list.append(1)
                        weight_sum+=self.new_weights[i]
                    else:
                        #0<X<=1になる時
                        rate=(self.new_capacity-weight_sum)/float(self.new_weights[i])
                        evaluate_list.append(rate)
                        weight_sum +=self.new_weights[i]*rate
                        for i in range(len(evaluate_list),self.new_N):#以降は全て０
                            evaluate_list.append(0)
                            
                        #最後に追加したアイテムがx=1となった時、evaluate_listは整数解なので暫定解より良いのかチェック
                        if rate==1:
                            if np.dot(np.array(evaluate_list),np.array(self.new_values))> self.obj :#この解が暫定解より良い時
                                self.new_results=evaluate_list #暫定解の更新
                                self.obj=np.dot(np.array(evaluate_list),np.array(self.new_values))
                                return False #分岐終了
                            else:#これ以上先に良い解なし
                                return False #分岐終了
                        else:#LPの解が非整数解
                            if np.dot(np.array(evaluate_list),np.array(self.new_values))> self.obj :#LPの解が暫定解より良い時
                                return True #分岐継続
                            else: #暫定解を超えていない
                                return False #この先を探す意味ないので終了
                

    def depthFirstSearch(self):
        if self.unfixed==[]:
            print ("---------貪欲法が最適解---------")
            print ('最適値=%d' %(np.dot(np.array(self.results),np.array(self.values))))
            print (self.results)
       #     print('探索ノード数=%d' %(self.num_of_nodes))
            end=time.time()
         #   print('実行時間=%f'%(end-start))
  
        else:  

            start=time.time()
            search_lists=[[0],[1]]
            while len(search_lists) !=0:
                print('探索中')
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
            print ("---------分枝限定法(縮小した問題)---------")
            print ('最適値=%d' %(self.obj))
            print (self.new_results)
            print('探索ノード数=%d' %(self.num_of_nodes))
            end=time.time()
            self.time=end-start
            print('実行時間=%f'%(end-start))

    def output(self): #元問題の解を出力:
        i=0
        for index in self.unfixed:
            self.results[index]=self.new_results[i]
            i+=1
        print('')
        print ("--------- 最終結果---------")
        print ('最適値=%d' %(np.dot(np.array(self.results),np.array(self.values))))
       # print (self.results)
        print('探索ノード数=%d' %(self.num_of_nodes))
 
        print('実行時間=%f'%(self.time))
          
    def depthFirstSearchAA(self):
        if self.unfixed==[]:
            print ("---------貪欲法が最適解---------")
            print ('最適値=%d' %(np.dot(np.array(self.results),np.array(self.values))))
            print (self.results)
       #     print('探索ノード数=%d' %(self.num_of_nodes))
            end=time.time()
         #   print('実行時間=%f'%(end-start))
  
        else:  

            start=time.time()
            search_lists=[[1],[0]]
            while len(search_lists) !=0:

                first_list = search_lists[0]
                search_lists.pop(0)
                if self.__judgeValue(first_list):
                    new_list_cp = copy.deepcopy(first_list)
                    new_list_cp.append(0)
                    search_lists.insert(0,new_list_cp)
                    new_list_cp=copy.deepcopy(first_list)
                    new_list_cp.append(1)
                    search_lists.insert(0,new_list_cp)
            print('')
            print ("---------分枝限定法(縮小した問題)---------")
            print ('最適値=%d' %(self.obj))
            print (self.new_results)
            print('探索ノード数=%d' %(self.num_of_nodes))
            end=time.time()
            self.time=end-start
            print('実行時間=%f'%(end-start))

        
       # print (np.dot(np.array(self.results_apx),np.array(self.weights)))
                
     
if __name__=="__main__":           
    bb = Knapsack()
    bb.fix_N()
    #bb.decide_num_of_item()
    bb.make_instance()
    bb.init_results() 
    bb.pegging()
    bb.change_problem()
    bb.depthFirstSearchAA()
    bb.output()
   # bb.improved_greedy()
    
