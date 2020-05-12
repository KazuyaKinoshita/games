# -*- coding: utf-8 -*-

import random
import numpy as np
from queue import Queue
import copy
import time

#パズルをターミナルに表示
def showpazz(pazz, elapsed_time):
    print('\ntime :', elapsed_time)
    num = [int(n) for n in pazz]
    if size == 16:
        print('-----', end="")
    print("----------------")
    for i in range(size):
        if i % col == 0:
            print('| ', end="")
        if num[i] < 10:
            print(' ', end="")
        if num[i] == 0:
            print('  | ', end="")
        else:
            print(num[i], "| ", end="")
        if i % col == col-1:
            if size == 16:
                print("\n---------------------")
            else:
                print("\n----------------")

#空白の位置の添字と移動できる組み合わせを探す
def find_in_sel(pazz):
    select_num = []
    #空白の位置を探して添字保存
    index = pazz.index(0)
    #移動できる組み合わせを探す
    #上に移動できる
    if index - col >= 0:
        select_num.append(index - col)
    #左に移動できる
    if index % col != 0:
        select_num.append(index - 1)
    #右に移動できる
    if index % col != col-1:
        select_num.append(index + 1)
    #下に移動できる
    if index + col < size:
        select_num.append(index + col)
    return index, select_num

#パズルをランダムに入れ替える
def random_change(pazz):
    #移動させる場所の添字と移動できる数字を入れる
    beforeindex, select_num = find_in_sel(pazz)
    #移動先の添字
    afterindex = random.choice(select_num)
    #盤面更新
    pazz[beforeindex], pazz[afterindex] = pazz[afterindex], pazz[beforeindex]
    return pazz

#パズルを受け取り、移動させた後のパズルを返す
def change_pazz(pazz):
    index, select_num = find_in_sel(pazz)
    moves = []
    for i in range(len(select_num)):
        tmp = copy.copy(pazz)
        tmp[index], tmp[select_num[i]] = tmp[select_num[i]], tmp[index]
        moves.append(tmp)
    return moves

#幅優先探索
def breadth_sreach(pazz):
    frontier = pazz
    search_q = Queue()
    search_q.put(pazz)
    while 1:
        current = search_q.get()
        # print('current:', current)
        #移動結果のリスト
        moves = change_pazz(current)
        # print('moves:', moves)
        #子ノードについてみる
        for n in moves:
            #終了判定
            if judge(n):
                return n
            #未訪問
            if n not in frontier:
                #訪問記録
                frontier.append(n)
                search_q.put(n)
    return pazz

#評価
# def eva_pazz(pazz):

#A*アルゴ
#f(n) = g(n) + h(n)
#h'(n) < h(n)で、h'(n):ヒューリスティック関数
def A_star(pazz):
    Calculate = []
    Close = []
    Calculate.append(pazz)
    while len(Calculate):
        #格納されているノードのうち、最小のf'(n)を持つnを取り出す
        if judge(n):
            return n
        else:
            Close.append(n)
        #nに隣接しているすべてのノードmに対して
        #f''(m) = g(n)(←f(n)-h(n)) + cost(n,m)
        if m not in Calculate and m not in Close:
            #f'(m)=f''(m)
            Calculate.append(m)
            # m.parent = n
        elif m in Calculate:
            #if f''(m) < f(m):
            #  f(m) = f''(m)
            #  m.parent = n
        elif m in Close:
            #if f''(m) < f(m):
            #  f(m) = f''(m)
            #  Calculate.append(m)
            #  m.parent = n

#ゲームの終了判定
def judge(pazz):
    end_flg = 0
    #終了する場合の配列
    ans = [int(i) for i in range(1,size)]
    ans.append(0)
    #終了していたら
    if np.allclose(pazz, ans):
        end_flg = 1
    return end_flg

#パズルサイズ入力
while 1:
    try:
        size = int(input('Pazzle size : '))
        if size == 9 or size == 16:
            break
        else:
            print('Wrong input!')
    except ValueError:
        print('You should input a number!')
if size == 9:
    col = 3
else:
    col = 4

#初期状態
pazz = [int(i) for i in range(1,size)]
pazz.append(0)
#パズルをぐちゃぐちゃにする
for i in range(5000):
    pazz = random_change(pazz)

#実行
t1 = 0
showpazz(pazz, t1)
t1 = time.time()
# pazz = breadth_sreach(pazz)
# pazz = A_star(pazz)
t2 = time.time()
showpazz(pazz, t2-t1)