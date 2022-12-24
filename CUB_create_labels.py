import re
import numpy as np
from PIL import Image
box_list = []
classes_list = []
image_list = []
classes_name =[]
image_data = []
image_name = []
tabel_confirm = []

#---------------------------------------------------------------------------------
#這個程式是創建label的程式，是直接指明地點，所以直接指到目標就ok了
#如果擔心的話可以在下面改自己知道的位子，再移動
#裡面的程式是覆蓋以前的檔案並且寫入資料，所以不用因為要改數據就刪掉建立好的檔案
#---------------------------------------------------------------------------------

def total_data_see(tabel_confirm , image_data):
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
    return total_data

#這邊是改變bounding_box的地方。
def creat_bounding_box(box_list , image_name , i):
    test_list = ['0' , '0' , '0' , '0']
    a = [0,0]
    #下面的a是圖片縮放轉移後的位子，'new_images/'<----只要改這個
    A = Image.open('new_image/'+image_name)
    a[0] = A.width
    a[1] = A.height
    #下面的b是元圖片位子，'images/'<----只要改這個
    #這邊提取舊資料是因為比例是按照原檔案縮的，所以需要依據原檔案數據
    b = [0,0]
    B = Image.open('images/'+image_name)
    b[0] = B.width
    b[1] = B.height
    #print(i ,a[0] , a[1])
    number_str = r'\d*\.\d*'
    size_img = 150
    number_box = re.findall(number_str , box_list)
    #print("number:",number_box[0] , number_box[1] , number_box[2] , number_box[3])
    #bounding_box第一個數字是x的起點，第二個是y的起點，第三個是x軸長度，第四個是y軸長度
    if b[0] >= b[1]:
        si = b[0]
    else:
        si = b[1]
    if float(number_box[0]) != 0:
        xmin = size_img/si * float(number_box[0])
    else:
        xmin = float(number_box[0])
    if float(number_box[1]) != 0:
        ymin = size_img/si * float(number_box[1])
    else:
        ymin = float(number_box[1])
    
    w = size_img/si * float(number_box[2])
    h = size_img/si * float(number_box[3])
    w_img = a[0]
    h_img = a[1]
    #下面四行是改變公式，總共有(xmin , ymin , w , h , w_img . h_img)
    xcenter = (xmin + w/2) / w_img
    ycenter = (ymin + h/2) / h_img
    w = w / w_img
    h = h / h_img
    #-------------------------------------------------------------
    if xcenter > 1:
        xcenter = 1
    if ycenter > 1:
        ycenter = 1
    if w > 1:
        w = 1
    if h > 1:
        h = 1
    test_list[0] = str(round(xcenter , 6))
    test_list[1] = str(round(ycenter , 6))
    test_list[2] = str(round(w , 6))
    test_list[3] = str(round(h , 6))
    #下面是debug用的不用管他
    '''
    for i in test_list:
        print(i)
        if float(i) > 1:
            print(1/0)
    '''
    #上面四個是最後要存入label的數據，如果需要直接在python裡面觀看的話，可以直接使用下面print
    #print("test:",test_list[0], test_list[1], test_list[2], test_list[3])
    return test_list

def open_data(box_list , classes_list , image_list , tabel_confirm , classes_name , image_data , image_name):
    fp_box = open('bounding_boxes.txt' , 'r')
    fp_classes = open('image_class_labels.txt','r')
    fp_image = open('images.txt','r')
    fp_classes_name = open('classes.txt' , 'r')
    fp_data = open('image_data.txt' , 'r')
    box = r'\s+.*'
    classe = r'\d*'
    na = r'\/.*\.'
    cla_na = r'\d{3}\..*'
    im_na = r'\s\d.*'
    c = 0
    for i , j , k in zip(fp_box , fp_classes , fp_image):
        box_data = re.findall(box, i)
        box_list.append(box_data[0])
        classe_data = re.findall(classe , j)
        classes_list.append(classe_data[2])
        na_data = re.findall(na , k)
        image_list.append(na_data[0][1:len(na_data[0])-1])
        image_str = re.findall(im_na , k)
        image_name.append(image_str[0][1:])
        tabel_confirm.append(0)
    #下面寫入classes全部，並且讀取資料，所以open()裡面的問子要自己改
    #'CUB_data/train/labels/'<---只要改這個，後面的classes.txt不用改，他會因為沒有自動創建
    with open('CUB_data/train/labels/classes.txt' , 'w' , encoding='utf-8') as f:
        for i , j in zip(fp_classes_name , fp_data):
            name_clas = re.findall(cla_na , i)
            classes_name.append(name_clas[0])
            f.write(str(c)+'\n')
            #f.write(name_clas[0])
            number_data = re.findall(classe , j)
            image_data.append(number_data[4])
            c += 1
    fp_box.close()
    fp_classes.close()
    fp_image.close()
    fp_classes_name.close()
    fp_data.close()

def read_write_data(classes_name , classes_list , box_list , image_data , tabel_confirm , image_list , image_name):
    one_classe = 0
    vail = 0
    next_vail = 0
    next_a = 0
    
    for i in range(11788):
        classes_Correction = int(classes_list[i]) - 1
        box_number_list = creat_bounding_box(box_list[i], image_name[i] , i)
        data = (
            str(classes_Correction)
            + ' ' + box_number_list[0] 
            + ' ' + box_number_list[1] 
            + ' ' + box_number_list[2] 
            + ' ' + box_number_list[3]
            )
        test = int(int(image_data[next_vail])/25*5)
        vail = int(image_data[next_vail]) - int(int(image_data[next_vail])/25*16)
        if one_classe != int(image_data[next_vail]):
            if next_a == 0:
                tabel_confirm[i] = 1
                #下面open()要改成自己的位子，'CUB_data/test/'<---只要改這個
                #改成要放test的地方
                with open('CUB_data/test/'+image_list[i]+'.txt', 'w' , encoding='utf-8') as f:
                    f.write(data)
            if next_a == 1:
                tabel_confirm[i] = 2
                #下面open()要改成自己的位子，'CUB_data/valid/labels/'<---只要改這個
                #改成要放valid的地方
                with open('CUB_data/valid/labels/'+image_list[i]+'.txt', 'w' , encoding='utf-8') as f:
                    f.write(data)
            if next_a == 2:
                tabel_confirm[i] = 3
                #下面open()要改成自己的位子，'CUB_data/train/labels/'<---只要改這個
                #改成要放train的地方
                with open('CUB_data/train/labels/'+image_list[i]+'.txt', 'w' , encoding='utf-8') as f:
                    f.write(data)
            one_classe += 1
            if one_classe == test:
                next_a += 1
            elif one_classe == vail:
                next_a += 1
        if one_classe == int(image_data[next_vail]):
            next_vail += 1
            next_a = 0
            one_classe = 0
#開啟檔案，需要bounding_boxes.txt、image_class_labels.txt、images.txt、classes.txt、image_data.txt
#這邊image_data.txt這邊是我自己做的，所以我會放到github
open_data(box_list , classes_list , image_list , tabel_confirm , classes_name , image_data , image_name)
#裡面全部open()的位子都需要注意，要改成自己想要擺放的位子，最後都是建立在這個檔案平行下
read_write_data(classes_name, classes_list, box_list, image_data, tabel_confirm, image_list, image_name)
#主要是在spyder裡面觀看提取情況，可以不執行
#see_data = total_data_see(tabel_confirm , image_data)
'''
a = 0
b = 0
c = 0
for i in range(200):
    a += see_data[i][0]
    b += see_data[i][1]
    c += see_data[i][2]
'''
#上面a,b,c是我當初計算test,valid,train各個總數用的，如果要只用需要使用total_data_see函示
