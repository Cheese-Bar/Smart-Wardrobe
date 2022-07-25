import sys
import os

import tensorflow.keras as tensorflow
import tensorflow as tf
import numpy as np
import PIL
import PIL.ImageOps
from PIL import Image
from PIL.ImageQt import ImageQt
from mlxtend.data import loadlocal_mnist
import matplotlib
import matplotlib.pyplot as plt

from win32api import GetSystemMetrics
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QFileDialog, QLabel, QComboBox, QTextEdit
from PyQt5 import QtCore
from PyQt5.QtCore import QThread, pyqtSignal, QPoint
from PyQt5.QtGui import  QIcon, QCursor, QPixmap, QPainter, QBrush, QPen, QColor

matplotlib.use("TkAgg")
trainBusy = False
testBusy = False
imgFile = ""
imgPrediction = ""
epochsCount = 3
optimizer = "SGD"
lossFunction = "sparse_categorical_crossentropy"
accuracyData = []

mainWinWidth = GetSystemMetrics(0)
mainWinHeight = GetSystemMetrics(1)

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self._Width = 475
        self._Height = 425
        global mainWinWidth
        global mainWinHeight
        self._X = int((mainWinWidth/2) - (self._Width/2))
        self._Y = int((mainWinHeight/2) - (self._Height/2))
        self._trainThread = trainThread()
        self._testThread = testThread()
        self.initUI()
    
    def initUI(self):
        self.setGeometry(self._X, self._Y, self._Width, self._Height)
        self.oldPos = self.pos()
        self.setFixedSize(self._Width, self._Height)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setStyleSheet("QMainWindow{background-color: rgb(64, 64, 64); color: rgb(255, 255, 255);  border: 1px solid rgb(26, 26, 26);}")
        self.acceptDrops()

        self.title = QLabel(self)
        self.title.move(40, 3)
        self.title.setFixedWidth(200)
        self.title.setStyleSheet("QLabel {color: rgb(255, 255, 255); font-size: 9pt;}")
        self.title.setText("Smart Wardrobe")

        self.iconLabel = QLabel(self)
        self.displayIcon("app_icon.png")

        self.imgLabel = QLabel(self)

        x_pos = self._Width - 28
        y_pos = 8
        self.closeButton = QPushButton(self)
        self.closeButton.move(x_pos, y_pos)
        self.closeButton.resize(20, 20)
        self.closeButton.setStyleSheet("QPushButton {background-color: rgb(153, 0, 0); color: rgb(255, 255, 255); font-weight: bold;}")
        self.closeButton.setText("X")
        self.closeButton.clicked.connect(self.closeButtonClicked)

        x_pos -= 30
        self.minimizeButton = QPushButton(self)
        self.minimizeButton.move(x_pos, y_pos)
        self.minimizeButton.resize(20, 20)
        self.minimizeButton.setStyleSheet("QPushButton {background-color: rgb(0, 0, 51); color: rgb(255, 255, 255); font-weight: bold;}")
        self.minimizeButton.setText("_")
        self.minimizeButton.clicked.connect(self.minimizeButtonClicked)

        x_pos = 15
        y_pos = 50

        self.trainButton = QPushButton(self)
        self.trainButton.move(x_pos, y_pos)
        self.trainButton.resize(115, 30)
        self.trainButton.setStyleSheet("QPushButton {background-color: rgb(77, 0, 25); color: rgb(255, 255, 255);}")
        self.trainButton.setText("Train Model")
        self.trainButton.clicked.connect(self.trainButtonClicked)

        self.testButton = QPushButton(self)
        self.testButton.move(x_pos + 125, y_pos)
        self.testButton.resize(115, 30)
        self.testButton.setStyleSheet("QPushButton {background-color: rgb(77, 0, 25); color: rgb(255, 255, 255);}")
        self.testButton.setText("Test Model")
        self.testButton.clicked.connect(self.testButtonClicked)
        
        self._trainThread.trainDone.connect(self.trainComplete)
        self._testThread.testDone.connect(self.testComplete)

        y_pos += 40
        self.imgFileDialog = QPushButton(self)
        self.imgFileDialog.move(x_pos, y_pos)
        self.imgFileDialog.resize(30, 30)
        self.imgFileDialog.setStyleSheet("QPushButton {background-color: rgb(77, 0, 25); color: rgb(255, 255, 255);}")
        self.imgFileDialog.setIcon(QIcon("folder_icon.png"))
        self.imgFileDialog.setIconSize(QtCore.QSize(25, 25))
        self.imgFileDialog.clicked.connect(self.imgFileDialogClicked)

        self.imgFileComboBox = QComboBox(self)
        self.imgFileComboBox.move(x_pos + 40, y_pos + 2)
        self.imgFileComboBox.resize(200, 25)
        self.imgFileComboBox.setStyleSheet("QComboBox {background-color: rgb(30, 30, 30); color: rgb(255, 255, 255);}")
        self.imgFileComboBox.currentTextChanged.connect(self.imgFileChanged)

        y_pos +=30
        self.optimizerLabel = QLabel(self)
        self.optimizerLabel.move(x_pos, y_pos)
        self.optimizerLabel.setStyleSheet("QLabel {color: rgb(255, 255, 255);}")
        self.optimizerLabel.setText("Optimizer")

        y_pos += 27
        self.optimizerComboBox = QComboBox(self)
        self.optimizerComboBox.move(x_pos, y_pos)
        self.optimizerComboBox.resize(240, 25)
        self.optimizerComboBox.setStyleSheet("QComboBox {background-color: rgb(30, 30, 30); color: rgb(255, 255, 255);}")
        self.optimizerComboBox.addItems([
            "SGD",
            "RMSprop",
            "Adagrad",
            "Adadelta",
            "Adam",
            "Adamax",
            "Nadam"
        ])
        self.optimizerComboBox.setCurrentIndex(0)
        self.optimizerComboBox.currentIndexChanged.connect(self.optimzerChanged)

        y_pos +=25
        self.lossFunctionLabel = QLabel(self)
        self.lossFunctionLabel.move(x_pos, y_pos)
        self.lossFunctionLabel.setStyleSheet("QLabel {color: rgb(255, 255, 255);}")
        self.lossFunctionLabel.setText("Loss Function")

        y_pos += 27
        self.lossFunctionComboBox = QComboBox(self)
        self.lossFunctionComboBox.move(x_pos, y_pos)
        self.lossFunctionComboBox.resize(240, 25)
        self.lossFunctionComboBox.setStyleSheet("QComboBox {background-color: rgb(30, 30, 30); color: rgb(255, 255, 255);}")
        self.lossFunctionComboBox.addItems([
            "mean_squared_error",
            "mean_absolute_error",
            "mean_absolute_percentage_error",
            "mean_squared_logarithmic_error",
            "squared_hinge",
            "hinge",
            "categorical_hinge",
            "logcosh",
            "huber_loss",
            "categorical_crossentropy",
            "sparse_categorical_crossentropy",
            "binary_crossentropy",
            "kullback_leibler_divergence",
            "poisson",
            "cosine_proximity",
        ])
        self.lossFunctionComboBox.setCurrentIndex(10)
        self.lossFunctionComboBox.currentIndexChanged.connect(self.lossFunctionChanged)

        x_pos = 15
        y_pos = 240
        self.console = QTextEdit(self)
        self.console.move(x_pos, y_pos)
        self.console.resize(440, 170)
        self.console.setStyleSheet("QTextEdit {background-color: rgb(4, 4, 4); color: rgb(255, 255, 255); font: 8pt Courier;}")
        self.console.setReadOnly(True)
        self.console.setText("Smart Wardrobe (GUI) 1.0")

        self.show()
    
    def closeButtonClicked(self):
        self.close()
    
    def minimizeButtonClicked(self):
        self.showMinimized()

    def trainButtonClicked(self):
        global trainBusy
        global testBusy
        if trainBusy or testBusy:
            self.console.append("Please wait while the current process completes")
        else:
            self.console.append("Training model ...")
            self._trainThread.start()
    
    def trainComplete(self):
        global accuracyData
        plt.figure()
        plt.style.use("ggplot")
        plt.ylim(0, 1)
        x = ["epoch " + str(i + 1) for i in range(len(accuracyData))]
        x_pos = [i for i, _ in enumerate(x)]
        colorData = [((255 - (colorMappingFunction(accuracyData[i]) * 102))/255, (51 + (colorMappingFunction(accuracyData[i]) * 204))/255, (colorMappingFunction(accuracyData[i]) * 51)/255) for i in range(len(accuracyData))]
        plt.bar(x_pos, accuracyData, color = colorData)
        plt.xlabel("Epoch")
        plt.ylabel("Accuracy")
        plt.xticks(x_pos, x)
        plt.show()
        self.console.append("Training completed")
    
    def testButtonClicked(self):
        global trainBusy
        global testBusy
        global imgPrediction
        if trainBusy or testBusy:
            self.console.append("Please wait while the current process completes")
        elif self.imgFileComboBox.currentText() == "":
            self.console.append("Please select an image")
        else:
            self.console.append("Testing model ...")
            self._testThread.start()
    
    def testComplete(self):
        self.console.append("\nImage: " + str(self.imgFileComboBox.currentText()) + "\nObject: " + str(imgPrediction))
    
    def imgFileDialogClicked(self):
        fileName = QFileDialog.getOpenFileName(self, "Open Image", "img", "Image Files (*.png *.jpg *.bmp)")
        if fileName[0] != "":
            self.imgFileComboBox.addItem(fileName[0])
            self.imgFileComboBox.setCurrentIndex(self.imgFileComboBox.count() - 1)
    
    def imgFileChanged(self):
        global imgFile
        imgFile = self.imgFileComboBox.currentText()
        self.displayImage(imgFile)
    
    def optimzerChanged(self):
        global optimizer
        optimizer = self.optimizerComboBox.currentText()
    
    def lossFunctionChanged(self):
        global lossFunction
        lossFunction = self.lossFunctionComboBox.currentText()
    
    def displayIcon(self, filePath):
        self.iconLabel.setPixmap(QPixmap(filePath).scaled(34, 34, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation))
        self.iconLabel.resize(34, 34)
        self.iconLabel.move(5, 1)
    
    def displayImage(self, filePath):
        img = PIL.Image.open(filePath)
        imgWidth, imgHeight = img.size
        cropArea = (0, 0, imgWidth, imgHeight)
        if imgWidth > imgHeight:
            cropArea = ((imgWidth/2) - (imgHeight/2), 0, (imgWidth/2) + (imgHeight/2), imgHeight)
        elif imgWidth < imgHeight:
            cropArea = (0, (imgHeight/2) - (imgWidth/2), imgWidth, (imgHeight/2) + (imgWidth/2))
        img = img.crop(cropArea)
        img = img.resize((28, 28), Image.ANTIALIAS)

        img = ImageQt(img)
        self.imgLabel.setPixmap(QPixmap.fromImage(img).scaled(175, 175, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation))
        self.imgLabel.resize(175, 175)
        self.imgLabel.move(277, 47)
    
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()
    
    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        if QCursor().pos().x() < self.x() + self._Width - 60 and QCursor().pos().y() < self.y() + 30:
            self.move(self._X + delta.x(), self._Y + delta.y())
            self._X = self.x()
            self._Y = self.y()
            self.oldPos = event.globalPos()
    
    def paintEvent(self, event):
        self.painter = QPainter(self)
        
        tempColor = QColor(26, 26, 26)

        self.painter.setPen(QPen(tempColor, 8, QtCore.Qt.SolidLine))
        self.painter.setBrush(QBrush(tempColor, QtCore.Qt.SolidPattern))
        self.painter.drawRect(0, 0, self._Width, 30)

        self.painter.setPen(QPen(tempColor, 3, QtCore.Qt.DashLine))
        self.painter.setBrush(QBrush(tempColor, QtCore.Qt.NoBrush))
        self.painter.drawRoundedRect(275, 45, 179, 179, 5, 5)

        self.painter.end()
    
    def consoleWrite(self, text):
        self.console.append(text)

class trainThread(QThread):
    trainDone = pyqtSignal(int)

    def __init__(self):
        super().__init__()
    
    def run(self):
        global trainBusy
        trainBusy = True
        trainData()
        trainBusy = False
        self.trainDone.emit(int)

class testThread(QThread):
    testDone = pyqtSignal(int)

    def __init__(self):
        super().__init__()
    
    def run(self):
        global testBusy
        global imgPrediction
        testBusy = True
        imgPrediction = testData()
        testBusy = False
        self.testDone.emit(int)

def imgIndex(n):
	if n == 0:
		return "T-Shirt/Top"
	elif n == 1:
		return "Trousers"
	elif n == 2:
		return "Pullover"
	elif n == 3:
		return "Dress"
	elif n == 4:
		return "Coat"
	elif n == 5:
		return "Sandals"
	elif n == 6:
		return "Shirt"
	elif n == 7:
		return "Sneakers"
	elif n == 8:
		return "Bar"
	elif n == 9:
		return "Ankle Boots"
	else:
		return "Unknown"

def trainData():
    global epochsCount
    global optimizer
    global lossFunction
    global accuracyData

    #sys.stdout = open(os.devnull, 'w')

    myWin.consoleWrite("Loading training data ...")
    x_train, y_train = loadlocal_mnist(images_path = "train-images-idx3-ubyte", labels_path = "train-labels-idx1-ubyte")
    x_train = tf.keras.utils.normalize(x_train, axis = 1)

    myWin.consoleWrite("Adding neural network layers ...")
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(784, activation = tf.nn.relu))
    model.add(tf.keras.layers.Dense(196, activation = tf.nn.relu))
    model.add(tf.keras.layers.Dense(10, activation = tf.nn.softmax))

    myWin.consoleWrite("Optimizer = " + str(optimizer))
    myWin.consoleWrite("Loss Function = " + str(lossFunction))
    model.compile(optimizer = optimizer, loss = lossFunction, metrics = ["acc", "mse"])
    
    myWin.consoleWrite("Fitting model ...")
    history = model.fit(x_train, y_train, epochs = epochsCount)
    accuracyData = history.history["acc"]
    for metric in model.metrics_names:
        metricList = history.history[metric]
        myWin.consoleWrite(metric + " = " + str(round(metricList[len(metricList) - 1], 4)))

    model.save("smartwardrobe.model")

    #sys.stdout = sys.__stdout__

def testData():
    img = PIL.Image.open(imgFile).convert('L')

    imgWidth, imgHeight = img.size
    cropArea = (0, 0, imgWidth, imgHeight)
    if imgWidth > imgHeight:
        cropArea = ((imgWidth/2) - (imgHeight/2), 0, (imgWidth/2) + (imgHeight/2), imgHeight)
    elif imgWidth < imgHeight:
        cropArea = (0, (imgHeight/2) - (imgWidth/2), imgWidth, (imgHeight/2) + (imgWidth/2))
    img = img.crop(cropArea)

    img = img.resize((28, 28), Image.ANTIALIAS)
    img = PIL.ImageOps.invert(img)
    img = np.array(img).flatten()
    imgArray = np.array([img])

    sys.stdout = open(os.devnull, 'w')

    new_model = tf.keras.models.load_model("smartwardrobe.model")
    predictions = new_model.predict(imgArray)

    sys.stdout = sys.__stdout__

    return imgIndex(np.argmax(predictions[0]))

def colorMappingFunction(x):
    return 0.5 * ((np.sign(x - 0.5) * (abs(x - 0.5) ** 0.2)) + 1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = Window()
    sys.exit(app.exec_())