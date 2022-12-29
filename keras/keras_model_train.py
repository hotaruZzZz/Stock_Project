from keras.models import Sequential
from keras.layers import Convolution2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import BatchNormalization
from keras.layers import Input
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.efficientnet import EfficientNetB0

def keras_application_model(x_train , x_label , y_valid , y_label , n , epochs = 100 , batch_size = 32):
    inputs = Input(shape=(x_train.shape[1],x_train.shape[2],x_train.shape[3]))
    outputs = EfficientNetB0(include_top=False 
                             ,weights = None
                             , input_shape = (x_train.shape[1],x_train.shape[2],x_train.shape[3]))(inputs)

    mod = tf.keras.Model(inputs, outputs)
    mod.compile(
        optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"]
    )
    output = mod.fit( x_train
                    , x_label
                    ,epochs=epochs
                    ,validation_data = (y_valid, y_label)
                    ,batch_size = batch_size
                    ,verbose=2           )
    return mod , output

def keras_image_train(x_train , x_label , y_valid , y_label , n , epochs = 100 , batch_size = 32):
    model=Sequential()
    from keras.optimizers import Adam
    #卷積組合
    model.add(Convolution2D(100,(3,3),input_shape=(n,n,3),activation='relu'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(3,3)))

    #卷積組合
    model.add(Convolution2D(75,(2,2),activation='relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))
    #卷積組合
    model.add(Convolution2D(50,(2,2),activation='relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))
    #卷積組合
    model.add(Convolution2D(25,(2,2),activation='relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))

    #flatten
    model.add(Flatten())
    
    #FC
    model.add(Dense(units=100,activation='relu'))
    model.add(Dropout(0.3))
    
    model.add(Dense( units=len(x_label[0])
                    ,kernel_initializer='normal'
                    ,activation='softmax'   ))
    model.compile( optimizer = Adam(0.0001)
                  ,loss = 'categorical_crossentropy'
                  ,metrics = ['accuracy']   )
    output = model.fit( x_train
                       ,x_label
                       ,epochs=epochs
                       ,validation_data = (y_valid , y_label)
                       ,batch_size = batch_size
                       ,verbose=2           )
    #model.save("keras_images_train.h5")
    
    return model , output

def draw_loss_data(output , epoch):
    import matplotlib.pyplot as plt
    epochs_number = []
    for i in range(epoch):
        epochs_number.append(i)
    loss_data = output.history['loss']
    val_loss_data = output.history['val_loss']
    plt.plot(epochs_number, loss_data, "b--", label = 'train')
    plt.plot(epochs_number, val_loss_data, "r-", label = 'val')
    plt.legend(loc="best", fontsize=14)
    plt.title("loss", fontsize=18)
    plt.xticks(rotation=30)
    plt.show()
def draw_acc_data(output , epoch):
    import matplotlib.pyplot as plt
    epochs_number = []
    for i in range(epoch):
        epochs_number.append(i)
    accuracy_data = output.history['accuracy']
    val_accuracy_data = output.history['val_accuracy']
    plt.plot(epochs_number, accuracy_data, "b--", label = 'train')
    plt.plot(epochs_number, val_accuracy_data, "r-", label = 'val')
    plt.legend(loc="best", fontsize=14)
    plt.title("accuracy", fontsize=18)
    plt.xticks(rotation=30)
    plt.show()

def draw_confusion_matrix(true_label , pred_label):
    from sklearn.metrics import confusion_matrix
    import matplotlib.pyplot as plt
    label_classes = []
    alabel = 0
    for i in true_label:
        if i != alabel:
            label_classes.append(i)
            alabel = i
    mat_con = (confusion_matrix(true_label, pred_label , labels=label_classes))
    #print(mat_con)
    fig, px = plt.subplots(figsize=(5, 5))
    px.matshow(mat_con, cmap=plt.cm.YlOrRd, alpha=0.5)
    for m in range(mat_con.shape[0]):
        for n in range(mat_con.shape[1]):
            px.text(x=m,y=n,s=mat_con[m, n], va='center', ha='center', size='xx-large')
    
    # Sets the labels
    plt.xlabel('Predictions', fontsize=16)
    plt.ylabel('Actuals', fontsize=16)
    plt.title('Confusion Matrix', fontsize=15)
    plt.show()