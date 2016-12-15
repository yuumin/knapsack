# -*- coding: utf-8 -*-

import numpy as np
import random
import itertools
import time

#アイテム数の決定
while 1:
   N = int(raw_input('# of items='))
   if N <10:
       print('# of items >=10')
   else:
       break
       

#重さの配列を生成(ランダム正整数)
weights=[np.random.randint(1, 1000) for i in range(N)]
#価値の配列を生成
values=[np.random.randint(1, 1000) for i in range(N)]
#結果の{0,1}ベクトル,初期値は0
results_greedy = np.zeros(N)
results_exact = np.zeros(N)
results_relax = np.zeros(N)
#capacity=max(重さ)＊items数/6
capacity = max(weights)*N/6

#評価値の配列
ratios = [float(values[i])/weights[i] for i in range(N)]

for i in range(N):
    print 'item[%d]:value=%d, weight=%d, ratio=%f' % (i,values[i],weights[i],ratios[i])
print 'capacity=%d' %(capacity)

#---------------全列挙---------------#

t0 = time.clock()#実行時間を計測
time.sleep(3)
opt_exact=0

binary = [0,1]
    # デカルト積
    # 繰り返しを許す: 1,1 がある
    # 順序が違えば別と見なす: 0,1 と 1,0 は別
for element in itertools.product(binary, repeat=N):
	solutions=np.array(element)
	obj = np.array(values).dot(solutions)#目的関数値
	if opt_exact <= obj and np.array(weights).dot(solutions) <= capacity:
		results_exact=solutions
		opt_exact=np.array(values).dot(results_exact)

weight_sum2=np.array(weights).dot(results_exact)
t1 = time.clock()#終了時間の取得
dt=t1-t0
#time=str(time)
print("---results(exact)---")
print "optimum = %d" %(opt_exact)
#print "x=",
#print(results_exact)
#print"weight_sum=",
#print (weight_sum2)
print 'time(exact)=%f' %(dt)


#-------------greedy-------------#
#実行時間を計測
t2 = time.clock()
time.sleep(3)
weight_sum = 0
copy_ratios=ratios #判定用に使う

k=1
while k<=N:#評価値の高い順に追加できるか判定
    indexMAX=max(xrange(N), key=lambda i: copy_ratios[i]) #評価値最大のindexの取得
    if weight_sum + weights[indexMAX]<= capacity:
        weight_sum += weights[indexMAX]
        results_greedy[indexMAX] = 1 #容量制限を満たしていたら採択
    copy_ratios[indexMAX] += -10000 #一度チェックしたアイテムは排除
    k+=1

obj_greedy=np.array(values).dot(np.array(results_greedy))#目的関数値
t3 = time.clock()#終了時間の取得
time_greedy=t3-t2

print("---results(greedy)---")
print "objective_greedy= %d" %(obj_greedy)
#print "x=",
#print(results_greedy)
#print"weight_sum=",
#print (weight_sum)
print 'time(greedy)=%f' %(time_greedy)

#---------------relaxation--------------#
t4 = time.clock()
time.sleep(3)
weight_sum3= 0

#評価値の高い順に追加できるか判定

copy_ratios2= [float(values[i])/weights[i] for i in range(N)]#判定用に使う
#print copy_ratios2
#print ratios
k=1
while k<=N:#N回チェックすれば良い
    indexMAX=max(xrange(N), key=lambda j: copy_ratios2[j]) #評価値最大のindexの取得
    #print copy_ratios2
    if weight_sum3 + weights[indexMAX]<= capacity:
        results_relax[indexMAX] = 1 #容量制限を満たしていたら全部入れる
        weight_sum3 += weights[indexMAX]
        copy_ratios2[indexMAX] += -10000 #一度チェックしたアイテムは排除
    else:
        rate=(capacity-weight_sum3)/float(weights[indexMAX])
        results_relax[indexMAX] =rate #可能な限りできるだけ入れる
        weight_sum3 += weights[indexMAX]*rate
        break
    k+=1

obj_relax=np.array(values).dot(np.array(results_relax))#目的関数値
t5 = time.clock()#終了時間の取得
time_lp=t5-t4

print("---results(relaxation)---")
#print "objectives_relaxation = %f" %(obj_relax)
print "upperbound = %d" %(int(obj_relax))
#print "x=",
#print(results_relax)
#print"weight_sum=",
#print (weight_sum3)
print 'time(relaxation)=%f' %(time_lp)
