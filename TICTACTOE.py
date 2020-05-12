# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from IPython.display import clear_output
import random
import time
from time import sleep
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
    
    if first_inputter == 1:
        play_area[play_area.index(player_input)] = '○'
    elif first_inputter == 2:
        play_area[play_area.index(player_input)] = '×'

    return play_area, player_input

#AIの入力
def get_ai_input(play_area, first_inputter, mode=0, q_table=None, epsilon=None):
    """
    AIの入力を受け付ける関数

    ゲームの状況を表すリストとAIのモードおよびその他のオプションを受け取り、
    AIの入力で更新したリストと入力を返す
    """
    #入力可能エリアの更新
    chooseable_are = [str(area) for area in play_area if type(area) is int]
    #モードの変更
    #ランダムに手を打つモード
    if mode == 0:
        ai_input = int(random.choice(chooseable_are))
    #Q学習するモード
    elif mode == 1:
        ai_input = get_ql_action(play_area, chooseable_are, q_table, epsilon)
    if first_inputter == 1:
        play_area[play_area.index(ai_input)] = '×'
    elif first_inputter == 2:
        play_area[play_area.index(ai_input)] = '○'

    return play_area, ai_input

#ゲーム画面の表示
def show_play(play_area, inputter=0, inputted=0):
    """
    TIC TAC TOEの画面を表示する関数

    表示すべきリスト（1~9の数値、○、×から成る）と
    直前の入力者および入力を受け取り、表示する
    """
    #出力のリセット
    clear_output()
    plt.figure(figsize=(6, 6))
    plt.plot()
    #目盛りの設定
    plt.xticks([0, 5, 10, 15])
    plt.yticks([0, 5, 10, 15])
    #目盛りの下軸ラベルを消す
    plt.tick_params(labelbottom='off', bottom='off')
    #目盛りの左軸ラベルを消す
    plt.tick_params(labelleft='off', left='off')
    #表示範囲
    plt.xlim(0, 15)
    plt.ylim(0, 15)
    #表示場所
    x_pos = [2.5, 7.5, 12.5]
    y_pos = [2.5, 7.5, 12.5]

    #マーカを設定
    markers = ['$' + str(marker) + '$' for marker in play_area]

    marker_count = 0
    #reversed:後ろから見る
    for y in reversed(y_pos):
        for x in x_pos:
            if markers[marker_count] == '$○$':
                color = 'r'
            elif markers[marker_count] == '$×$':
                color = 'k'
            else:
                color = 'b'
            #プロット
            plt.plot(x, y, marker=markers[marker_count], markersize=30, color=color)
            marker_count += 1
    #ゲーム開始
    if inputter == 0:
        title = 'Play the TIC TAC TOE!!'
    #ゲーム途中
    else:
        title = '{} chose {}!!'.format(inputter, inputted)
    #表示
    plt.title(title)
    plt.show()

#ゲーム終了の判定
def judge(play_area, inputter):
    """
    ゲーム終了および勝者を判定する

    ゲームの状況を表すリストと直前の入力者を受け取り、
    ゲームが終了していれば勝者と終了判定を返す
    """
    end_flg = 0
    winner = 'NOBODY'
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

#Qテーブル作成
def make_q_table():
    """
    Qテーブルを作成する関数
    """
    n_columns = 9
    n_rows = 3**9

    return np.zeros((n_rows, n_columns))

#Qテーブルの更新
def q_learning(play_area, ai_input, reward, play_area_next, q_table, end_flg):
    """
    Qテーブルを更新する関数

    ゲームの状況を表すリスト・AIの行動・報酬
    １手番後のゲームの状況を表すリスト・Qテーブル・勝利フラグ
    を受け取り、更新したQテーブルを返す
    """
    #行番号取得
    row_index = find_q_row(play_area)
    row_index_next = find_q_row(play_area_next)
    column_index = ai_input - 1
    #勝利した or 敗北した場合
    if end_flg == 1:
        q_table[row_index, column_index] = q_table[row_index, column_index] + eta * (reward - q_table[row_index, column_index])
    #まだ続いている場合以外
    else:
        q_table[row_index, column_index] = q_table[row_index, column_index] + eta * (reward + gamma * np.nanmax(q_table[row_index_next,:]) - q_table[row_index, column_index])
    return q_table

#Qテーブルの行インデックスを返す
def find_q_row(play_area):
    """
    参照時の状況（state）が参照すべき行番号を計算する関数

    ゲームの状況を表すリストを受け取り、行番号を返す
    """
    row_index = 0
    for index in range(len(play_area)):
        if play_area[index] == '○':
            coef = 1
        elif play_area[index] == '×':
            coef = 2
        else:
            coef = 0
        row_index += (3 ** index) * coef
    return row_index

#行動選択
#ε-greedy法（？）を用いる
def get_ql_action(play_area, chooseable_are, q_table, epsilon):
    """
    AIの行動を決定する関数

    ゲームの状況を表すリスト・選択可能エリア・Qテーブル・イプシロンを受け取り、
    行動を返す
    """
    #epsilonの確率でランダムな選択をする
    if np.random.rand() < epsilon:
        ai_input = int(random.choice(chooseable_are))
    #Qテーブルに従い行動を選択する
    else:
        row_index = find_q_row(play_area)
        first_choise_flg = 1
        for choise in chooseable_are:
            if first_choise_flg == 1:
                ai_input = int(choise)
                first_choise_flg = 0
            else:
                if q_table[row_index, ai_input-1] < q_table[row_index, int(choise)-1]:
                    ai_input = int(choise)
    return ai_input

#ランダムvsQ学習
def randomAI_vs_QLAI(first_inputter, q_table, epsilon=0):
    """
    AI（ランダム）とAI（Q学習）のゲームを実行する関数

    先手（１：AI(ランダム)、２：AI(Q学習)）とQテーブルを受け取り、
    ゲームが終了するまで実行する
    """
    inputter1 = 'Random AI'
    inputter2 = 'QL AI'

    #Q学習待避用
    ql_input_list = []
    play_area_list = []

    play_area = list(range(1, 10))
    #show_play(play_area)
    inputter_count = first_inputter
    end_flg = 0
    ql_flg = 0
    reward = 0
    while True:
        #Q学習待避用
        play_area_tmp = play_area.copy()
        play_area_list.append(play_area_tmp)
        #Q学習実行フラグ
        ql_flg = 0
        #AI(Q学習)の手番
        if (inputter_count % 2) == 0:
            #QL AI入力
            play_area, ql_ai_input = get_ai_input(play_area, first_inputter, mode=1, q_table=q_table, epsilon=epsilon)
            winner, end_flg = judge(play_area, inputter2)
            #Q学習待避用
            ql_input_list.append(ql_ai_input)
            #勝利した場合
            if winner == inputter2:
                reward = 1
                ql_flg = 1
            play_area_before = play_area_list[-1]
            ql_ai_input_before = ql_input_list[-1]
        #AI(ランダム)の手番
        elif (inputter_count % 2) == 1:
            play_area, random_ai_input = get_ai_input(play_area, first_inputter+1, mode=1)
            winner, end_flg = judge(play_area, inputter1)
            #AI(ランダム)が先手の場合の初手以外は学習
            if inputter_count != 1:
                ql_flg = 1
        #Q学習実行
        if ql_flg == 1:
            ql_ai_input_before = ql_input_list[-1]
            q_table = q_learning(play_area_before, ql_ai_input_before, reward, play_area, q_table, end_flg)
        if end_flg:
            break
        inputter_count += 1
    print('{} win!!'.format(winner))
    return winner, q_table

#Qテーブル作成およびパラメータの設定
q_table = make_q_table()
#学習率
eta = 0.1
#時間割引率
gamma = 0.9
#ε-greedy法の初期値
initial_epsilon = 0.5

#ランダム vs QL(学習)
#試行回数設定
episode = 5000
winner_list = []
start = time.time()
for i in range(episode):
    epsilon = initial_epsilon * (episode-i) / episode
    winner, _ = randomAI_vs_QLAI(1, q_table, epsilon)
    winner_list.append(winner)
elapsed_time = time.time() - start
print('elapsed_time:{0}'.format(elapsed_time) + '[sec]')

#結果の出力
print('勝ち回数')
print('Random AI:{}'.format(winner_list.count('Random AI')))
print('QL AL    :{}'.format(winner_list.count('QL AI')))
print('NOBODY   :{}'.format(winner_list.count('NOBODY')))
print('QLの勝率  :{}'.format(winner_list.count('QL AI') / len(winner_list)))