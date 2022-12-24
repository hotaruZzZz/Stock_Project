import cv2 
import numpy as np
from PIL import Image

#---------------------------------------------------------------------------------
#這個程式是把原來檔案改成想要size的程式，是提取並創新一個檔案，所以不用當心原檔案消失
#---------------------------------------------------------------------------------

#size_change(原檔案位子, 想要改成的大小 , 新的檔案位子)
def size_change(img , img_size , new_img):
    img_a = Image.open(img)
    w = img_a.width       #圖片的宽
    h = img_a.height      #圖片的高
    
    if(w > h) :
        w2 = img_size;h2 = (w2/w) * h
    else :
        h2 = img_size;w2 = (h2/h) * w
    img_data = cv2.imread(img)# 讀取圖片
    # 修改大小
    img = cv2.resize(img_data, (int(w2), int(h2)))  # 將大小修改成w2*h2
    
    # 儲存圖片
    cv2.imwrite(new_img, img)
#需要在這個檔案平行的位子有一個images.txt，這個在原本CUB裡面有一個
import re
fp_image = open('images.txt','r')
image_name = []
re_image = r'\s\d.*'
#---------------------------------------------------------------------------------
#這邊注意a是你原本圖片檔案位子，b是你想要新圖片的位子，可以一樣，但我選擇新增一個資料夾
#---------------------------------------------------------------------------------
a = r'E:\school\大學\專題報告\2022_05_18_AI演講資料\studen_deep_learning\Program syntax\images'
b = r'E:\school\大學\專題報告\2022_05_18_AI演講資料\studen_deep_learning\Program syntax\new_images'
#讀取images.txt裡面的文次，並且提取後段名稱位子
for i in fp_image:
    image_str = re.findall(re_image , i)
    image_name.append(image_str[0][1:])
#將一一讀取檔案
dataset_images = []
#這邊後面新圖片位子，我選擇原檔名是因為對我來說後續需要抓全部檔案可以直接使用前面的方法，如果改成自己可能需要自己另外創建總檔案名
for i in range(11788):
    dataset_images.append(cv2.imread("images/"+image_name[i]))
    size_change("images/"+image_name[i] , 150 , "new_image/"+image_name[i])