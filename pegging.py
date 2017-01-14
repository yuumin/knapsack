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
        self.num_of_nodes=0
        
    #--------1/2-近似解法　で使う----------#
        self.results_apx=[] 
        self.obj_apx=0 
        self.results_greedy=[]
        self.obj_greedy=0

    #--------pegging_testで使う---------#
        self.suvive=0
        self.dead=0#釘付けされた変数のカウント
        self.pegging_list=[]
        self.som_is_undecided=0#全部固定されたら１にする
                    
    def fix_N(self):
        self.N=500
        self.suvive=self.N
        

    def decide_num_of_item(self):
        
        while 1:
            self.N = int(input('# of items='))
            self.suvive=self.N
            #self.N = 30
            if self.N <10:
                print('# of items >=10')
            else:
                break

    def make_instance(self): #インスタンスを降順にして表示
        weights=[np.random.randint(1, 1000) for i in range(self.N)]
        values=[np.random.randint(1, 1000) for i in range(self.N)]
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
            
            
    def pegging_test(self):#
        #固定する解は0,1を入力し、それ以外は-1を格納
        #for peg_index in range(self.N):
        while len(self.pegging_list)!=self.N:
            list=[]
            list.extend(self.pegging_list)
            peg_index=len(self.pegging_list)
            
            for i in range(len(list),self.N):
                list.append(-1)
            #greedyの解とは裏側の変数を入力し固定
            if self.results_greedy[peg_index]==1:
                list[peg_index]=0
                val_greedy=1
            else:
                list[peg_index]=1
                val_greedy=0
            #固定して緩和問題を解く
            weight_sum=0
            for i in range(len(list),self.N):#greedyに採択を決定
                    if list[i]==-1:
                        if weight_sum+self.weights[i]<self.capacity: #１入れてもまだ容量に余裕ありの時
                            list[i]=1
                            weight_sum+=self.weights[i]
                        else:
                            #0=<X<=1になる時
                            rate=(self.capacity-weight_sum)/float(self.weights[i])
                            list[i]=rate
                            weight_sum +=self.weights[i]*rate
            #もし暫定解よりも悪い解だったら、その解は最適解にはなりえないのでgreedｙで得られた解に釘付けする
            if np.dot(np.array(list),np.array(self.values)) < self.obj_greedy :
                self.suvive += -1
                self.pegging_list.append(val_greedy)
                self.dead +=1
            else:#固定できなかったら-1入れておく
                self.pegging_list.append(-1)
             #   self.some_is_undecided=1  #釘付けテストで生き残った変数があるよ、という目印          
       
        print ('釘付けリスト＝')
        print (self.pegging_list)
        print('# of 生き残った変数=',end="")
        print(self.suvive)
        
            
            
            
    

    def __judgeValue(self,fixed_list):
        self.num_of_nodes +=1
        print('fixed_list=',end="")
        print (fixed_list)
        
       # evaluate_list =[] #採択したxの判定を格納
       # evaluate_list.extend(fixed_list)
        weight_sum=0
        #固定リストの重さの合計を最初に計算
        for i in range(len(fixed_list)):
            if fixed_list[i]!=-1:#固定解の重さの和を算出
                weight_sum+= fixed_list[i]*self.weights[i]
        if self.suvive== 0: #全てのxが固定されている時
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
                for i in range(self.N):
                    if fixed_list[i]==-1 :#まだ決まっていない解について
                        fixed_list[i]=0
                if np.dot(np.array(fixed_list),np.array(self.values))> self.obj :#この解が暫定解より良い時
                    self.results=fixed_list #暫定解の更新
                    self.obj=np.dot(np.array(fixed_list),np.array(self.values))
                    return False
                else: #暫定値を超えていない
                    return False #この先に許容解はないので終了
            else:
            #容量に余裕ありの時
            #緩和問題の解を用いて枝刈りをする
                for i in range(self.N):#greedyに採択を決定
                    if fixed_list[i]==-1:#まだ決まっていない解について
                        if weight_sum+self.weights[i]<self.capacity: #１入れてもまだ容量に余裕ありの時
                            fixed_list[i]=1
                            weight_sum+=self.weights[i]
                        else:
                        #0<X<=1になる時
                            rate=(self.capacity-weight_sum)/float(self.weights[i])
                            fixed_list[i]=(rate)
                            weight_sum +=self.weights[i]*rate
                            for j in range(i,self.N):#以降は決まってないものは全て０
                                if fixed_list[j]==-1:
                                    fixed_list[j]=0
                            
                        #最後に追加したアイテムがx=1となった時、fixed_listは整数解なので暫定解より良いのかチェック
                            if rate==1:
                                if np.dot(np.array(fixed_list),np.array(self.values))> self.obj :#この解が暫定解より良い時
                                    self.results=fixed_list #暫定解の更新
                                    self.obj=np.dot(np.array(fixed_list),np.array(self.values))
                                    return False #分岐終了
                                else:#これ以上先に良い解なし
                                    return False #分岐終了
                            else:#LPの解が非整数解
                                if np.dot(np.array(fixed_list),np.array(self.values))> self.obj :#LPの解が暫定解より良い時
                                    return True #分岐継続
                                else: #暫定解を超えていない
                                    return False #この先を探す意味ないので終了
                

    def depthFirstSearch(self):
        search_lists=[[0],[1]]
        count=0
        
        while len(search_lists) !=0:
            count+=1
            first_list = search_lists[0]#search_list(複数)の配列から最初の配列を調べる
            search_lists.pop(0)#調べたものは削除
            print ('search_list=',end="")
            print (search_lists)
            print('first_list=',end="")
            print (first_list)
            if self.__judgeValue(first_list):
                new_list_cp = copy.deepcopy(first_list)
                print ('new_list_cp=',end="")
                print(new_list_cp)
                new_list_cp.append(1)#末尾に１を追加してsearch_listに追加する
                print ('new_list_cp.append(1)=',end="")
                print(new_list_cp)
                search_lists.insert(0,new_list_cp)#末尾に0を追加してsearch_listに追加する
                new_list_cp=copy.deepcopy(first_list)
                new_list_cp.append(0)
                search_lists.insert(0,new_list_cp)
                print ('**search_list=',end="")
                print(search_lists)
            else:
                print('false', end="")#探索不可能な配列の場合はsaech_listには何も追加しない
                print (first_list)
                
                
        print('')
        print ("---------分枝限定法---------")
        print ('最適値=%d' %(self.obj))
        print (self.results)
        print('探索ノード数=%d' %(self.num_of_nodes))
        #  print (np.dot(np.array(self.results),np.array(self.weights)))
        
        
                       

    def depthFirstSearchAA(self):#１から優先に探索
        print(self.dead)
        print(self.suvive)
        if self.N==self.dead :#全部釘付けされている時、それが最適解
            self.results=self.pegging_list
            self.obj=np.dot(np.array(self.pegging_list),np.array(self.values))
        else:#釘付けリストを使って、初期サーチリストを作成
            search_lists=[]
            new_list_cp = copy.deepcopy(self.pegging_list)
            for index in range(self.N):
                if self.pegging_list[index]==-1:
 
                    new_list_cp[index]=1
                    search_lists.insert(0,new_list_cp)
                    new_list_cp=copy.deepcopy(self.pegging_list)
                    new_list_cp[index]=0
                    search_lists.insert(0,new_list_cp)
                    print('最初のリスト＝')
                    print (search_lists)
            
       
                    count=0
                    self.num_of_nodes=0#初期化
                    while len(search_lists) !=0:
                        count+=1
                        first_list = search_lists[0]#search_list(複数)の配列から最初の配列を調べる
                        search_lists.pop(0)#調べたものは削除
           # print ('search_list=',end="")
            #print (search_lists)
            #print('first_list=',end="")
            #print (first_list)
                    if self.__judgeValue(first_list):
                        new_list_cp = copy.deepcopy(self.first_list)
                        for index in range(self.N):
                            if first_list[index]==-1:
 
                                new_list_cp[index]=1
                                search_lists.insert(0,new_list_cp)
                                new_list_cp=copy.deepcopy(self.pegging_list)
                                new_list_cp[index]=0
                                search_lists.insert(0,new_list_cp)
                                new_list_cp = copy.deepcopy(first_list)
             #   print ('new_list_cp=',end="")
              #  print(new_list_cp)
                       # new_list_cp.append(1)#末尾に１を追加してsearch_listに追加する
               # print ('new_list_cp.append(1)=',end="")
               # print(new_list_cp)
                       # search_lists.insert(0,new_list_cp)#末尾に0を追加してsearch_listに追加する
                        #new_list_cp=copy.deepcopy(first_list)
                        #new_list_cp.append(0)
                        #search_lists.insert(0,new_list_cp)
               # print ('**search_list=',end="")
                #print(search_lists)
                    else:
                    #print('false', end="")#探索不可能な配列の場合はsaech_listには何も追加しない
                #print (first_list)
                        m=0
 
          
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
        self.results_greedy.extend(results1)
        self.obj_greedy=np.dot(np.array(self.results_greedy),np.array(self.values)) 

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
        self.obj=self.obj_apx
        self.results=self.results_apx
        
      
    def print_result(self):
                       
        print('')
        print ("---------分枝限定法---------")
        print ('最適値=%d' %(self.obj))
        print (self.results)
        print('探索ノード数=%d' %(self.num_of_nodes))
        
        
        print ('--------1/2-近似解法--------')
        print ('目的関数値＝%d' %(self.obj_apx) )
        print ('近似比=%f' %(self.obj_apx/self.obj))
        print (self.results_apx)
        print (self.results_greedy)
        print (np.dot(np.array(self.results_apx),np.array(self.weights)))        
        
       # print (np.dot(np.array(self.results_apx),np.array(self.weights)))
                
     
if __name__=="__main__":           
    bb = Knapsack()
    bb.fix_N()
    #bb.decide_num_of_item()
    bb.make_instance()
    bb.init_results() 
   # bb.depthFirstSearch()
    
    bb.improved_greedy()
    bb.pegging_test()
  #  bb.depthFirstSearch()
    bb.depthFirstSearchAA()
    bb.print_result()
    
    
