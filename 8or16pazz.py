# -*- coding: utf-8 -*-

import random
import numpy as np
import copy

#パズルをターミナルに表示
def showpazz(pazz):
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

#移動先入力
def get_input(pazz, player=0):
    surrender = 0
    #移動させる場所の添字
    beforeindex = 0
    #移動先の添字
    afterindex = 0
    #移動できる数字を入れる
    select_num = []
    #移動できる方向を入れる
    select_char = []
    #空白の位置を探して添字保存
    for i in range(size):
        if pazz[i] == 0:
            beforeindex = i
            break
    #移動できる組み合わせを探す
    #上に移動できる
    if beforeindex - col >= 0:
        select_num.append(pazz[beforeindex - col])
        select_char.append('w')
    #左に移動できる
    if beforeindex % col != 0:
        select_num.append(pazz[beforeindex - 1])
        select_char.append('a')
    #右に移動できる
    if beforeindex % col != col-1:
        select_num.append(pazz[beforeindex + 1])
        select_char.append('d')
    #下に移動できる
    if beforeindex + col < size:
        select_num.append(pazz[beforeindex + col])
        select_char.append('s')
    #プレイヤーの手動入力
    if not player:
        #入力
        while 1:
            player_input = input('Choose a character {} or Surrendrer [0] >>> '.format(select_char))
            #プレイヤーが降参
            if player_input == '0':
                surrender = 1
                return pazz, surrender
            #移動できる方向を入力
            elif player_input in select_char:
                player_input = select_num[select_char.index(player_input)]
                break
            #指定していない文字を入力
            else:
                print('Wrong input!')
    #バラす時に利用
    else:
        player_input = random.choice(select_num)
    #盤面更新
    #選んだ数値から移動先の添字を探す
    afterindex = pazz.index(player_input)
    pazz[beforeindex], pazz[afterindex] = pazz[afterindex], pazz[beforeindex]
    return pazz, surrender

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

#8パズルを遊ぶ
def playpazz(pazz):
    print('Let\'s play', size-1, 'Pazzle!')
    #盤面表示
    showpazz(pazz)
    #ターン数を数える
    turns = 0
    #リタイア判定
    surrender = 0
    #終了を知らせる
    end_flg = 0
    while 1:
        #ターンの経過
        turns += 1
        #プレイヤーに入力してもらいパズルを更新
        pazz, surrender = get_input(pazz, 0)
        #リタイアしていたらループ抜ける
        if surrender:
            break
        #ターン数表示
        print('\nNumber of turns :', turns)
        #盤面表示
        showpazz(pazz)
        #ゲームが終了したかを判別
        end_flg = judge(pazz)
        #終了していたらループ抜ける
        if end_flg:
            break
    if end_flg:
        print('CLEAR!!')
    else:
        print('Surrendered...')

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
    pazz, _ = get_input(pazz, 1)

#実行
playpazz(pazz)