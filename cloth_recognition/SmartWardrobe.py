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

#sys.stdout = open(os.devnull, "w")
while 1:
	#sys.stdout = sys.__stdout__
	command = input("\nEnter command> ")
	command_list = command.split()
	#sys.stdout = open(os.devnull, "w")
	if command_list[0] == "train":
		x_train, y_train = loadlocal_mnist(
		images_path = "E:/Programming/SmartWardrobe/train-images-idx3-ubyte",
		labels_path = "E:/Programming/SmartWardrobe/train-labels-idx1-ubyte")
		
		x_train = tf.keras.utils.normalize(x_train, axis = 1)
		
		model = tf.keras.models.Sequential()
		model.add(tf.keras.layers.Flatten())
		model.add(tf.keras.layers.Dense(784, activation=tf.nn.relu))
		model.add(tf.keras.layers.Dense(196, activation=tf.nn.relu))
		model.add(tf.keras.layers.Dense(10, activation=tf.nn.softmax))
		
		model.compile(optimizer = "sgd", loss = "sparse_categorical_crossentropy", metrics = ["accuracy"])
		model.fit(x_train, y_train, epochs = 3)
		
		model.save("smartwardrobe.model", save_format = "h5")
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
		
		imgArray = np.array(imgArray)
		new_model = tf.keras.models.load_model("smartwardrobe.model".encode("utf-8"))
		predictions = new_model.predict(imgArray)
		
		iter = 0
		#sys.stdout = sys.__stdout__
		while iter < cnt:
			print("\n" + str(iter + 1) + "). " + imgNames[iter] + " is an image of " + imageIndex(np.argmax(predictions[iter])))
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