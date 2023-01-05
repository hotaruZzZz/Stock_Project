import numpy as np
from keras.utils import np_utils
np.random.seed(10)
import matplotlib.pyplot as plt
import keras_model_train as KMT

tabel_confirm = []
def open_data(n_size , number = 11788*6):
    import re
    import cv2
    
    fp_image = open('augmented_images.txt','r')
    fp_classes = open('augmented_labels.txt','r')
    fp_number_data = open('augmented_datas.txt','r')
    image_name = []
    image_label = []
    image_data = []
    re_name = r'\S*'
    #re_image = r'\s\d.*'
    re_classe = r'\d*'
    #a = r'E:\school\大學\專題報告\2022_05_18_AI演講資料\studen_deep_learning\Program syntax\images'
    #b = r'E:\school\大學\專題報告\2022_05_18_AI演講資料\studen_deep_learning\Program syntax\new_images'
    for i , j in zip(fp_image , fp_classes):
        na_data = re.findall(re_name , i)
        image_name.append(na_data[2])
        classe_data = re.findall(re_classe , j)
        image_label.append(int(classe_data[2]))
        tabel_confirm.append(0)
    for i in fp_number_data:
        number_data = re.findall(re_classe , i)
        image_data.append(number_data[2])
    dataset_test = []
    dataset_valid = []
    dataset_train = []
    label_test = []
    label_valid = []
    label_train = []
    one_classe = 0
    vail = 0
    next_vail = 0
    next_a = 0
    for i in range(number):
        test = int(int(image_data[next_vail])/25*5)
        vail = int(image_data[next_vail]) - int(int(image_data[next_vail])/25*16)
        if one_classe != int(image_data[next_vail]):
            if next_a == 0:
                tabel_confirm[i] = 1
                next_img = cv2.imread("CUB_data/test/"+image_name[i])
                next_img = cv2.resize(next_img, (n_size , n_size))
                dataset_test.append(next_img)
                label_test.append(image_label[i])
            if next_a == 1:
                tabel_confirm[i] = 2
                next_img = cv2.imread("CUB_data/valid/images/"+image_name[i])
                next_img = cv2.resize(next_img, (n_size , n_size))
                dataset_valid.append(next_img)
                label_valid.append(image_label[i])
            if next_a == 2:
                tabel_confirm[i] = 3
                next_img = cv2.imread("CUB_data/train/images/"+image_name[i])
                next_img = cv2.resize(next_img, (n_size , n_size))
                dataset_train.append(next_img)
                label_train.append(image_label[i])
            one_classe += 1
            if one_classe == test:
                next_a += 1
            elif one_classe == vail:
                next_a += 1
        if one_classe == int(image_data[next_vail]):
            next_vail += 1
            next_a = 0
            one_classe = 0
    x_train = np.array(dataset_train , dtype = "float64")
    x_label = np.array(label_train , dtype = "int")
    y_valid = np.array(dataset_valid , dtype = "float64")
    y_label = np.array(label_valid , dtype = "int") 
    z_test = np.array(dataset_test , dtype = "float64")
    z_label = np.array(label_test , dtype = "int") 
    fp_image.close()
    fp_classes.close()
    fp_number_data.close()
    return x_train , x_label , y_valid , y_label , z_test , z_label

#11788*6
number = 11788*6
n_size = 150
epochs_int = 100
#建立訓練、驗證、測試三個分類的訓練圖檔和標籤
x_train , x_label , y_valid , y_label , z_test , z_label = open_data(n_size , number)
#print(x_train.shape)
#print(x_label.shape)
#需要把標籤做onthot編譯，例如:總共10個標籤，其中一個為5---->[0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
x_label_onehot = np_utils.to_categorical(x_label)
y_label_onehot = np_utils.to_categorical(y_label)
z_label_onehot = np_utils.to_categorical(z_label)
'''
model, output= KMT.keras_image_train( x_train
                                    , x_label_onehot
                                    , y_valid 
                                    , y_label_onehot 
                                    , n_size 
                                    , epochs = epochs_int 
                                    , batch_size = 100)
'''
model, output = KMT.keras_application_model( x_train
                                           , x_label_onehot
                                           , y_valid 
                                           , y_label_onehot 
                                           , n_size 
                                           , epochs = epochs_int 
                                           , batch_size = 100)

#評估準確率
fake_scores = model.evaluate(x_train , x_label_onehot)
print('\n假的準確率=' , fake_scores[1])
scores = model.evaluate(z_test, z_label_onehot)
print('\n準確率=',scores[1])

#繪圖loss, accuracy圖表
KMT.draw_loss_data(output,epochs_int)
KMT.draw_acc_data(output,epochs_int)

#測試回傳直
prediction = model.predict(z_test)
fake_prediction = model.predict(x_train)
fake_prediction_classes=np.argmax(fake_prediction, axis=1)
prediction_classes=np.argmax(prediction, axis=1)
print(fake_prediction_classes)
print(prediction_classes)
if number <= 10206:
    KMT.draw_confusion_matrix(z_label , prediction_classes)
    KMT.draw_confusion_matrix(x_label , fake_prediction_classes)
