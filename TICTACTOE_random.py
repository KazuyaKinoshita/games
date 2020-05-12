# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from IPython.display import clear_output
import random
import time
import numpy as np
import math

#プレイヤー入力
def get_player_input(play_area, first_inputter):
    """
    プレイヤーから入力を受け付ける関数

    ゲームの状況を表すリストを受け取り、
    プレイヤーの入力で更新したリストと入力を返す
    """
    #入力可能エリアの更新
    chooseable_are = [str(area) for area in play_area if type(area) is int]
    #入力させる
    while(True):
        player_input = input('Choose a number!>>>')
        #置ける場所を入力した
        if player_input in chooseable_are:
            player_input = int(player_input)
            break
        #置けない場所を入力した
        else:
            print('Wrong input!\nChoose a number from　{}'.format(chooseable_are))
    
    #プレイエリアの更新
    #プレイヤーが先手なら○で
    if first_inputter == 1:
        play_area[play_area.index(player_input)] = '○'
    #プレイヤーが後手なら×で入力を行う
    elif first_inputter == 2:
        play_area[play_area.index(player_input)] = '×'

    return play_area, player_input

#AIの入力
def get_ai_input(play_area, first_inputter, q_table=None, epsilon=None):
    """
    AIの入力を受け付ける関数

    ゲームの状況を表すリストとAIのモードおよびその他のオプションを受け取り、
    AIの入力で更新したリストと入力を返す
    """
    #入力可能エリアの更新
    chooseable_are = [str(area) for area in play_area if type(area) is int]
    #置く場所をランダムに決定
    ai_input = int(random.choice(chooseable_are))
    #プレイヤーが先手なら×で
    if first_inputter == 1:
        play_area[play_area.index(ai_input)] = '×'
    #プレイヤーが後手なら○で入力を行う
    elif first_inputter == 2:
        play_area[play_area.index(ai_input)] = '○'

    return play_area, ai_input

#ゲーム画面をターミナルに表示
def show_play_term(play_area, inputter=0, inputted=0):
    """
    TIC TAC TOEの画面をターミナルに表示する関数

    表示すべきリスト（1~9の数値、○、×から成る）と
    直前の入力者および入力を受け取り、表示する
    """
    #マーカを設定
    markers = [str(marker) for marker in play_area]

    #ゲーム開始
    if inputter == 0:
        title = 'Play the TIC TAC TOE!!'
    #ゲーム途中
    else:
        title = '{} chose {}!!'.format(inputter, inputted)
    
    #画面表示
    print(title)
    for i in range(9):
        #「end=""」にすることで改行させない
        print(markers[i], end="")
        if(i % 3) == 2:
            print("")
        else:
            print(" | ", end="")
    print()

#ゲーム終了の判定
def judge(play_area, inputter):
    """
    ゲーム終了および勝者を判定する

    ゲームの状況を表すリストと直前の入力者を受け取り、
    ゲームが終了していれば勝者と終了判定を返す
    """
    end_flg = 0
    winner = 'DRAW'
    #三つ並ぶ条件を羅列
    first_list = [0, 3, 6, 0, 1, 2,  0, 2]
    second_list = [1, 4, 7, 3, 4, 5, 4, 4]
    third_list = [2, 5, 8, 6, 7, 8, 8, 6]
    for first, second, third in zip(first_list, second_list, third_list):
        #三つ並んだら
        if play_area[first] == play_area[second] and play_area[first] == play_area[third]:
            winner = inputter
            end_flg = 1
            break
    #入力可能エリアの更新
    chooseable_are = [str(area) for area in play_area if type(area) is int]
    #入力可能エリアが無くなったら
    if len(chooseable_are) == 0:
        end_flg = 1
    
    return winner, end_flg

#お試し対戦
def player_vs_randomAI(first_inputter):
    """
    プレイヤーとAI（ランダム）のゲームを実行する関数

    先手（１：プレイヤー、２：AI）を受け取り、ゲームが終了するまで実行する
    """
    inputter1 = 'YOU'
    inputter2 = 'AI'

    #プレイエリアの表示
    play_area = list(range(1, 10))
    show_play_term(play_area)
    #どちらのターンなのかを判別
    inputter_count = first_inputter
    #終了を知らせる
    end_flg = 0
    while True:
        #プレイヤーターン
        if (inputter_count % 2) == 1:
            print('Your turn!')
            #プレイヤーの入力で更新したリストと入力を得る
            play_area, play_input = get_player_input(play_area, first_inputter)
            #プレイエリアをターミナルに表示
            show_play_term(play_area, inputter1, play_input)
            #ゲームが終了したかを判別
            winner, end_flg = judge(play_area, inputter1)
            if end_flg:
                break
        #AIのターン
        elif (inputter_count % 2) == 0:
            print("AI's turn!\n.\n.\n.")
            play_area, ai_input = get_ai_input(play_area, first_inputter)
            #sleep関数で処理を一時停止する
            time.sleep(3)
            #プレイエリアをターミナルに表示
            show_play_term(play_area, inputter2, ai_input)
            #ゲームが終了したかを判別
            winner, end_flg = judge(play_area, inputter2)
            #ゲームが終了していたらループを抜ける
            if end_flg:
                break
        inputter_count += 1
    if winner == 'DRAW':
        print(winner + "!!")
    else:
        print('{} win!!'.format(winner))

#ランダムAIとゲーム開始
#引数１：プレイヤー先手
#引数２：プレイヤー後手
turn = random.randint(0,1)%2 + 1
player_vs_randomAI(turn)