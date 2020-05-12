# -*- coding: utf-8 -*-

import random
import matplotlib.pyplot as plt
import numpy as np

#パズルをmatplotlibで表示
def drawpazz(pazz):
    # clear_output()
    plt.figure(figsize=(6, 6))    
    plt.plot()
    plt.tick_params(labelbottom=False, labelleft=False)
    plt.tick_params(bottom=False, left=False)
    plt.xlim(0, 15)
    plt.ylim(0, 15)
    x_pos = [2.5, 7.5, 12.5]
    y_pos = [2.5, 7.5, 12.5]
    markers = ['$' + str(marker) + '$' for marker in pazz]
    marker_count = 0
    for y in reversed(y_pos):
        for x in x_pos:
            plt.plot(x, y, marker=markers[marker_count], markersize=30, color='b')
            marker_count += 1
    plt.title('Start 8×8 Pazzle')
    plt.show()

#パズルをターミナルに表示
def showpazz(pazz):
    num = [str(n) for n in pazz]
    print("-------------")
    for i in range(9):
        if i % 3 == 0:
            print('| ', end="")
        if num[i] == '0':
            print('  | ',end="")
        else:
            print(num[i],"| " ,end="")
        if i % 3 == 2:
            print("\n-------------")

#移動先入力
def get_input(pazz, player=0):
    surrender = 0
    #移動させる場所のインデックス
    beforeindex = 0
    #移動先のインデックス
    afterindex = 0
    #移動できる組み合わせ
    choose_num = [[pazz[1],pazz[3]], [pazz[0],pazz[2],pazz[4]], [pazz[1],pazz[5]], [pazz[0],pazz[4],pazz[6]], [pazz[1],pazz[3],pazz[5],pazz[7]], [pazz[2],pazz[4],pazz[8]], [pazz[3],pazz[7]], [pazz[4],pazz[6],pazz[8]], [pazz[5],pazz[7]]]
    #移動できる数字を探す
    select_num = []
    for i in range(9):
        if pazz[i] == 0:
            beforeindex = i
            select_num = choose_num[i]
            break
    #プレイヤーの手動入力
    if not player:
        #入力
        while 1:
            try:
                player_input = int(input('Choose a number {} or Surrendrer [9] >>> '.format(select_num)))
                #プレイヤーが降参
                if player_input == 9:
                    surrender = 1
                    break
                #移動できる数字を入力
                elif player_input in select_num:
                    break
                #移動できない数字を入力
                else:
                    print('Wrong input!')
            #数字以外を入力
            except ValueError:
                    print('You should input a number!')
    #自動入力
    else:
        player_input = random.choice(select_num)
    #盤面更新
    for i in range(9):
        if player_input == pazz[i]:
            afterindex = i
            break
    pazz[beforeindex], pazz[afterindex] = pazz[afterindex], pazz[beforeindex]
    return pazz, surrender

#ゲームの終了判定
def judge(pazz):
    end_flg = 0
    #終了する場合の配列
    ans = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    #終了していたら
    if np.allclose(pazz, ans):
        end_flg = 1
    return end_flg

#8パズルを遊ぶ
def playpazz(pazz):
    print('Let\'s play 8Pazzle!')
    #drawpazz(pazz)
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

#初期状態
pazz = [1, 2, 3, 4, 5, 6, 7, 8, 0]
#パズルをぐちゃぐちゃにする
for i in range(5000):
    pazz, _ = get_input(pazz, 1)

#実行
playpazz(pazz)
