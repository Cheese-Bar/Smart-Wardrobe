import os
import sys
import tensorflow.keras as tensorflow
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import PIL
import PIL.ImageOps
from PIL import Image
from mlxtend.data import loadlocal_mnist
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout
from tensorflow.keras.utils import multi_gpu_model


def imageIndex(n):
	if n == 0:
		return "a T-SHIRT/TOP"
	elif n == 1:
		return "TROUSERS"
	elif n == 2:
		return "a PULLOVER"
	elif n == 3:
		return "a DRESS"
	elif n == 4:
		return "a COAT"
	elif n == 5:
		return "SANDALS"
	elif n == 6:
		return "a SHIRT"
	elif n == 7:
		return "SNEAKERS"
	elif n == 8:
		return "a BAG"
	elif n == 9:
		return "ANKLE BOOTS"
	else:
		return "an unknown object"

def newindex(n):
	if n == 0:
		return "a T-SHIRT/TOP"
	elif n == 1:
		return "shirt"
	elif n == 3:
		return "a PULLOVER"
	elif n == 4:
		return "a COAT"
	else:
		return "Unknown"

os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

#sys.stdout = open(os.devnull, "w")
while 1:
	#sys.stdout = sys.__stdout__
	command = input("\nEnter command> ")
	command_list = command.split()
	#sys.stdout = open(os.devnull, "w")
	if command_list[0] == "train":
		x_train, y_train = loadlocal_mnist(
		images_path = "train-images-idx3-ubyte",
		labels_path = "train-labels-idx1-ubyte")

		# new add
		X = []
		Y = []
		for i in range(len(x_train)):
			if y_train[i] ==0:
				X.append(x_train[i])
				Y.append(0)#duanxiu
			elif y_train[i]==2:
				X.append(x_train[i])
				Y.append(3)#maoyi
			elif y_train[i]==4:
				X.append(x_train[i])
				Y.append(4)#dayi
			elif y_train[i]==6:
				X.append(x_train[i])
				Y.append(1)#changxiu
		x_train=np.array(X)
		y_train=np.array(Y)
		
		x_train = tf.keras.utils.normalize(x_train, axis = 1)
		x_train=x_train.reshape(len(x_train),28,28,1)
		
		model = tf.keras.models.Sequential()
		# model = Sequential()
		model.add(Conv2D(32, (5,5),activation='relu',input_shape=(28,28,1)))
		model.add(Conv2D(64, (5,5),activation='relu'))
		#model.add(Convolution2D(128, (3,3),activation='relu'))
		model.add(MaxPooling2D(2,2))
		model.add(Dropout(0.5))
		#model.add(Convolution2D(64, (3,3),activation='relu'))
		#model.add(Convolution2D(32, (3,3),activation='relu'))
		model.add(Conv2D(32,(5,5),activation='relu'))
		#model.add(MaxPooling2D(2,2))
		model.add(Conv2D(8,(5,5),activation='relu'))
		model.add(Flatten())
		model.add(Dense(10,activation='softmax'))

		# model.add(Conv2D(32, (3, 3), padding='same', activation='relu', input_shape=(28, 28, 1)))
		# model.add(MaxPooling2D((2, 2)))
		# model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
		# model.add(MaxPooling2D((2, 2)))
		# model.add(Conv2D(128, (3, 3), padding='same', activation='relu'))
		# model.add(MaxPooling2D((2, 2)))
		# model.add(Conv2D(128, (3, 3), padding='same', activation='relu'))
		# model.add(MaxPooling2D((2, 2)))
		# model.add(Flatten())
		# model.add(Dropout(0.5))
		# model.add(Dense(512, activation='relu'))
		# model.add(Dense(10, activation='sigmoid'))
		
		# gpu设定
		# model = multi_gpu_model(model, 1)

		# model.compile(optimizer = "sgd", loss = "sparse_categorical_crossentropy", metrics = ["accuracy"])
		model.compile(optimizer = "adam", loss = "sparse_categorical_crossentropy", metrics = ["accuracy"])
		model.fit(x_train, y_train, epochs = 60)
		
		model.save("smartwardrobe2.model", save_format = "h5")
	elif command_list[0] == "test":
		cnt = 0
		imgArray = []
		imgNames = []
		# for filename in os.listdir("E:/Programming/SmartWardrobe/img"):
		for filename in os.listdir(os.getcwd()+"/img"):
			if filename.endswith(".jpg"):
				img = PIL.Image.open("img/" + filename).convert("L")
				img = img.resize((28, 28), Image.ANTIALIAS)
				img = PIL.ImageOps.invert(img)
				img = np.array(img)
				img = img.flatten()
				imgArray.append(img)
				imgNames.append(filename)
				cnt+=1
		
		imgArray = np.array(imgArray).reshape(cnt,28,28,1)
		new_model = tf.keras.models.load_model("smartwardrobe2.model".encode("utf-8"))
		predictions = new_model.predict(imgArray)
		
		iter = 0
		#sys.stdout = sys.__stdout__
		while iter < cnt:
			print("\n" + str(iter + 1) + "). " + imgNames[iter] + " is an image of " + newindex(np.argmax(predictions[iter])))
			iter+=1
		#sys.stdout = open(os.devnull, "w")
	elif command_list[0] == "display":
		#sys.stdout = sys.__stdout__
		if len(command_list) < 2:
			print("type:    display [FILE NAME]")
		else:
			im = Image.open("img/" + command_list[1])
			im.show()
		#sys.stdout = open(os.devnull, "w")
	elif command_list[0] == "exit":
		exit()
	else:
		#sys.stdout = sys.__stdout__
		print("\nCOMMANDS")
		print("\ttrain\t\t\ttrain dataset")
		print("\ttest\t\t\tpredict images in img folder")
		print("\tdisplay [FILE NAME]\tdisplay image file")
		#sys.stdout = open(os.devnull, "w")