import shutil
import re
import numpy as np
import Data_Normalization as DN
#---------------------------------------------------------------------------------
#這個程式是用來把檔案，分類計算移動test,valid,train三個資料夾
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------
#這邊要特別注意，這個是"移動"檔案，所以原本的地方會沒有東西，所以請確認完位子後再執行
#如果因為中間出現error或著失敗導致原本檔不完全，要直接刪掉原檔案全部，再從cub裡面複製檔案
#所以下面a的地方請用複製完檔案的位子，不要直接使用cub裡面的檔案
#這邊也推薦在執行這個檔案前先執行Data_Normalization.py，裡面的新檔案位子是直接一個新位子，後續只要檔案不完全的時候，直接執行前面講的檔案就OK了
#---------------------------------------------------------------------------------
fp_image = open('images.txt','r')
fp_data = open('image_data.txt','r')
image_name = []
image_data = []
tabel_confirm = []
re_image = r'\s\d.*'
#a要改成想要抓取圖片的位子
a = r'E:\school\大學\專題報告\2022_05_18_AI演講資料\studen_deep_learning\Program syntax\new_image'
#下面三個是分別是放到各個名稱地方，位子也需要改成自己的位子
#會使用r''格式是因為可以直接複製檔案路徑
destination_test = r'E:\school\大學\專題報告\2022_05_18_AI演講資料\studen_deep_learning\Program syntax\CUB_data\data_move_test\1'
destination_valid = r'E:\school\大學\專題報告\2022_05_18_AI演講資料\studen_deep_learning\Program syntax\CUB_data\data_move_test\2'
destination_train = r'E:\school\大學\專題報告\2022_05_18_AI演講資料\studen_deep_learning\Program syntax\CUB_data\data_move_test\3'
total = 1
for i in fp_image:
    image_str = re.findall(re_image , i)
    image_name.append(image_str[0][1:])
    tabel_confirm.append(0)
for i in fp_data:
    classe = r'\d*'
    number_data = re.findall(classe , i)
    image_data.append(number_data[4])
one_classe = 0
vail = 0
next_vail = 0
next_a = 0
for i in range(11788):
    #下面兩個改變計算方式可以改變比例
    #下面test計算方式，例如:想要分a:b:c的比例------>某一類總數/(a+b+c)*c
    test = int(int(image_data[next_vail])/25*5)
    #下面vail計算方式，例如:想要分a:b:c的比例------>(某一類總數) - (某一類總數/(a+b+c)*a)
    vail = int(image_data[next_vail]) - int(int(image_data[next_vail])/25*16)
    #上面全部都要在int()裡面計算，因為要整數，另外image_data[]需要是因為原本是'str'
    if one_classe != int(image_data[next_vail]):
        if next_a == 0:
            shutil.move(f"{a}/{image_name[i]}", destination_test)
            tabel_confirm[i] = 1
        if next_a == 1:
            shutil.move(f"{a}/{image_name[i]}", destination_valid)
            tabel_confirm[i] = 2
        if next_a == 2:
            shutil.move(f"{a}/{image_name[i]}", destination_train)
            tabel_confirm[i] = 3
        one_classe += 1
        if one_classe == test:
            next_a += 1
        elif one_classe == vail:
            next_a += 1
    if one_classe == int(image_data[next_vail]):
        next_vail += 1
        next_a = 0
        one_classe = 0
'''
#計算整理資料個別數量
total_data = np.zeros((200,3))
tests = 0
vails = 0
trains = 0
one_classe = 0
n = 0
next_vail = 0
for i in range(11788):
    if one_classe != int(image_data[next_vail]):
        if tabel_confirm[i] == 1:
            tests += 1
            one_classe += 1
        if tabel_confirm[i] == 2:
            vails += 1
            one_classe += 1
        if tabel_confirm[i] == 3:
            trains += 1
            one_classe += 1
    if one_classe == int(image_data[n]):
        total_data[n][0] = tests
        total_data[n][1] = vails
        total_data[n][2] = trains
        tests = 0
        vails = 0
        trains = 0
        one_classe = 0
        n += 1
'''
fp_image.close()
fp_data.close()