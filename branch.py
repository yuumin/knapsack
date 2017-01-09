# -*- coding: utf-8 -*-

import numpy as np
import random
import itertools
import time
import copy

#def init_LPresults(LP_results,N): #使いたいけど使えてない
     #   for i in range(N):
      #      LP_results[i]=0

class Knapsack:
    def __init__(self):
        self.N=0
        self.weights=[]
        self.values=[]
        self.results=[] #暫定解
        self.obj=0 #暫定解の目的関数値
        self.weight_sum=0
        self.capacity=0
        self.flag=[]
        self.LP_results=[]

    def decide_num_of_item(self):
        while 1:
            self.N = int(raw_input('# of items='))
            if self.N <10:
                print('# of items >=10')
            else:
                break
    def fix_N(self):
        self.N=5
        

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
            self.LP_results.append(0)
    def __init_LPresults(self): #使いたいけど使えてない
        for i in range(self.N):
            self.LP_results[i]=0

   

            
    def __get_obj(self,results_list):
        obj =0
        for i in range(self.N):
            obj += self.values[i]*self.results_list[i]
        return obj
    
    def __get_weights(self,hoge_list):
        sum_of_W=0
        for i in range(len(hoge_list)):
            sum_of_W+= hoge_list[i]*self.weights[i]
        return sum_of_W


    def solve_LP(self,fixed_list):
        weight_sum=self.__get_weights(fixed_list)
      #  print weight_sum
        self.__init_LPresults()
      #  print self.LP_results
       # print self.capacity
        for i in range(len(fixed_list)): #固定する解を先に格納
            self.LP_results[i]=fixed_list[i]
        for i in range(len(fixed_list),self.N):
            #固定していない変数を入れるかはgreedyに決定
       #     print i 
            
            if weight_sum+self.weights[i]<=self.capacity:
                self.LP_results[i]=1
                weight_sum+=self.weights[i]
            else:
                rate=(self.capacity-weight_sum)/float(self.weights[i])
                weight_sum +=self.weights[i]*rate
                self.LP_results[i]=rate
             #   print rate
                break
        return self.LP_results


    def __solve_LP(self,fixed_list):
        weight_sum=self.__get_weights(fixed_list)
     #   print weight_sum
        self.__init_LPresults()#緩和問題の解は毎回初期化
      #  print self.LP_results
       # print self.capacity
        for i in range(len(fixed_list)): #固定する解を先に格納
            self.LP_results[i]=fixed_list[i]
        for i in range(len(fixed_list),self.N):
            #固定していない変数を入れるかはgreedyに決定
        #    print i 
            
            if weight_sum+self.weights[i]<=self.capacity:
                self.LP_results[i]=1
                weight_sum+=self.weights[i]
            else:
                rate=(self.capacity-self.weight_sum)/float(self.weights[i])
                weight_sum +=self.weights[i]*rate
                self.LP_results[i]=rate
         #       print rate
                break
      
            
        
    def __judge_int(self,list):
    #整数解かどうか判定
        for i in range(self.N):
            if list[i]!=int(list[i]):
                return False 
                break
        return True
    
    def __judge_weights(self,hoge_list):
        #渡されたlistの重さ合計値を算出し、容量オーバーなら0、容量ぴったりなら１、容量未満なら-1を返す
        sum_of_W=0
        for i in len(hoge_list):
            sum_of_W+= hoge_list[i]*self.weights[i]
        if sum_of_W > self.capacity:
            return 0
        elif sum_of_W == self.capacity:
            return 1
        else:
            return -1
    
            
            
    def print_results(self):
        obj_LP=np.array(self.values).dot(np.array(self.results))
        #self.print_instance()
        print("---results(relaxation)---")
#print "objectives_relaxation = %f" %(obj_relax)
      #  print "upperbound = %d" %(int()
      #  print "x=",
      # print(self.LP_results)
      #  print"weight_sum=",
       # print (self.weight_sum)
        #print self.capacity
#print 'time(relaxation)=%f' %(time_lp)


    def __judgeValue(self,fixed_list):
        #あるノードにおける変数x=1を入れた時に分岐継続できるかを判定、また、より良い解を見つけたら暫定解を更新
       # new_list=fixed_list.append(1)#末尾に１を追加
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
                        
        #=============#
       
               

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
        print ("-----深さ優先探索-----")
        print (self.obj)
        print (self.results)
        print (np.dot(np.array(self.results),np.array(self.weights)))
  
    
    
    def depthFirstSearchB(self): #深さ優先探索
        search_lists = [[0], [1]] # 要素 [0]、[1]は先に入れておく
        while len(search_lists) != 0: # search_listsが空になるまで続ける
            first_list = search_lists[0] # Stachで考える、上から１つ取得
            search_lists.pop(0) # 取得した要素は削除
            if self.__judgeValue(first_list): # 探索が継続かどうか
                new_list_cp = copy.deepcopy(first_list) # 次要素に「1」を追加するために深いコピー
                new_list_cp.append(1) # 1を末尾に追加
                search_lists.insert(0, new_list_cp) # 新たな要素を search_listsの先頭に格納
                new_list_cp = copy.deepcopy(first_list) # 次要素に「0」を追加するために深いコピー
                new_list_cp.append(0) # 0を末尾に追加
                search_lists.insert(0, new_list_cp) # 新たな要素を　search_listsの先頭に格納

        print("-----深さ優先探索-----")
        for index in range(self.N):
            print( ": " + str(self.results[index]))
        print("ans: " + str(self.obj))
    
    def breadthFirstSearch(self): #幅優先探索
        search_lists = [[0], [1]] # 要素 [0]、[1]は先に入れておく
        while len(search_lists) != 0: # search_listsが空になるまで続ける
            first_list = search_lists[0] # Queueで考える、上から１つ取得
            search_lists.pop(0) # 取得した要素は削除
            if self.__judgeValue(first_list): # 探索が継続かどうか
                new_list_cp = copy.deepcopy(first_list) # 次要素に「1」を追加するために深いコピー
                new_list_cp.append(0) # 0を末尾に追加
                search_lists.append(new_list_cp) # 新たな要素を search_listsの末尾に格納
                new_list_cp = copy.deepcopy(first_list) # 次要素に「0」を追加するために深いコピー
                new_list_cp.append(1) # 1を末尾に追加
                search_lists.append(new_list_cp) # 新たな要素を　search_listsの末尾に格納

        print("-----幅優先探索-----")
        print (self.obj)
        print (self.results)
  
        
if __name__=="__main__":           
    bb = Knapsack()
    bb.fix_N()
    #bb.decide_num_of_item()
    #bb.random_generator()
    bb.make_instance()
    
   # bb.capacity_generator()
    bb.init_results()
  #  bb.init_LPresults()
    #bb.solve_LP([0,0])
    #bb.solve_LP([0,1,0])
    #bb.print_results()
    bb.depthFirstSearch()
    bb.breadthFirstSearch()
    
    
        
          
    
 #10def judge_Value(self,fixed_list):"
    

