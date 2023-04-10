import math
import re
import sys
import time
from collections import Counter
import nltk
import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPalette, QBrush
from PyQt5.QtWidgets import QMainWindow, QPushButton, QFileDialog,
QLineEdit, QPlainTextEdit, QLabel
from nltk import sent_tokenize, word_tokenize, PorterStemmer
from nltk.corpus import wordnet, stopwords
from nltk.stem import WordNetLemmatizer
Plagiarism detection in text documents
from nltk.tag import pos_tag
from nltk.tokenize import PunktSentenceTokenizer
nltk.download(’stopwords’)
class MainWindow(QMainWindow):
def __init__(self):
QMainWindow.__init__(self)
self.font = QtGui.QFont("Times", 12)
self.font2 = QtGui.QFont("Times", 20, QtGui.QFont.Bold)
icon = QtGui.QIcon()
icon.addPixmap(QtGui.QPixmap("icon.png"),
QtGui.QIcon.Normal, QtGui.QIcon.Off)
self.setWindowIcon(icon)
self.setWindowTitle("Document Plagarism Checker")
self.setFixedSize(900, 600)
oImage = QImage("plag.png")
sImage = oImage.scaled(QSize(900, 600))
palette = QPalette()
palette.setBrush(10, QBrush(sImage))
self.setPalette(palette)
self.startButton = QPushButton(’Check Matching’, self)
self.startButton.clicked.connect(self.startService)
self.startButton.setCursor(QtGui.QCursor
(QtCore.Qt.PointingHandCursor))
self.startButton.move(180, 250)
self.startButton.resize(150, 30)
self.sample1_in = QLineEdit(self)
Plagiarism detection in text documents
self.sample1_in.move(20, 70)
self.sample1_in.resize(400, 30)
self.sample2_in = QLineEdit(self)
self.sample2_in.move(20, 150)
self.sample2_in.resize(400, 30)
self.sample1_in.setDisabled(True)
self.sample2_in.setDisabled(True)
self.stopButton = QPushButton(’Reset’, self)
self.stopButton.clicked.connect(self.reset)
self.stopButton.setCursor(QtGui.QCursor
(QtCore.Qt.PointingHandCursor))
self.stopButton.move(700, 20)
self.stopButton.resize(150, 30)
self.chooseButton1 = QPushButton(’Choose File 1’, self)
self.chooseButton1.clicked.connect
(self.OpenFileNamesDialog1)
self.chooseButton1.resize(100, 32)
self.chooseButton1.move(450, 69)
self.chooseButton2 = QPushButton(’Choose File 2’, self)
self.chooseButton2.clicked.connect
(self.OpenFileNamesDialog2)
self.chooseButton2.resize(100, 32)
self.chooseButton2.move(450, 150)
def startService(self):
input_text = open(self.sample1_in.text(), ’r’)
input_text1 = open(self.sample2_in.text(), ’r’)
Plagiarism detection in text documents
text = input_text.read()
text1 = input_text1.read()
input_text.close()
input_text1.close()
self.sentences = sent_tokenize(text)
self.sentences1 = sent_tokenize(text1)
self.N = len(self.sentences)
self.N1 = len(self.sentences1)
self.ps = PorterStemmer()
self.lemmatizer = WordNetLemmatizer()
self.stop_words = stopwords.words(’english’)
self.special = [’.’, ’,’, ’\’’, ’"’, ’-’, ’/’, ’*’, ’+’,
’=’, ’!’, ’@’, ’$’, ’%’, ’^’, ’&’, ’‘‘’, ’\’\’’, ’We’,
’The’, ’This’]
mat = self.f_s_to_s(self.sentences1)
print (mat)
length = len(mat)-2
point1= sum(mat)
percent = point1*100
percent_round = round(percent,2)
percent_text = str(percent_round)+" %"
print (point1)
self.result = QLabel(self)
Plagiarism detection in text documents
self.result.setText(’score’)
self.result.resize(100, 30)
self.result.move(380, 250)
self.result.setFont(self.font2)
self.result.show()
self.sample3_in = QLineEdit(self)
self.sample3_in.move(350, 300)
self.sample3_in.resize(120, 30)
self.sample3_in.setText(percent_text)
self.sample3_in.setFont(self.font)
self.sample3_in.show()
def get_cosine(self,vec1, vec2):
intersection = set(vec1) & set(vec2.keys())
numerator = sum([vec1[x] * vec2[x] for x in intersection])
sum1 = sum([vec1[x]**2 for x in vec1.keys()])
sum2 = sum([vec2[x]**2 for x in vec2.keys()])
denominator = math.sqrt(sum1) * math.sqrt(sum2)
if not denominator:
return 0.0
else:
return numerator / denominator
def text_to_vector(self,text):
words = word_tokenize(text)
vec=[]
for word in words:
if(word not in self.stop_words):
Plagiarism detection in text documents
if(word not in self.special):
w=self.normalise(word);
vec.append(w);
#print Counter(vec)
return Counter(vec)
def docu_to_vector(self,sent):
vec=[]
for text in sent:
words = word_tokenize(text)
for word in words:
if(word not in self.stop_words):
if(word not in special):
w=normalise(word);
vec.append(w);
#print Counter(vec)
return Counter(vec)
def f_s_to_s(self,sent):
length = self.N+1
cosine_mat=np.zeros(length)
row=0
for text in self.sentences:
maxi=0
vector1 = self.text_to_vector(text)
for text1 in sent:
vector2 = self.text_to_vector(text1)
cosine = self.get_cosine(vector1, vector2)
for text2 in sent:
Plagiarism detection in text documents
vector3 = self.text_to_vector(text2)
cosine = self.get_cosine(vector1, vector3)
for text3 in sent:
vector4 = self.text_to_vector(text3)
cosine = self.get_cosine(vector1, vector4)
for text4 in sent:
vector5 = self.text_to_vector(text4)
cosine = self.get_cosine(vector1, vector5)
for text5 in sent:
vector6 = self.text_to_vector(text5)
cosine = self.get_cosine(vector1, vector6)
for text6 in sent:
vector7 = self.text_to_vector(text6)
cosine = self.get_cosine(vector1, vector7)
for text7 in sent:
vector8 = self.text_to_vector(text7)
cosine = self.get_cosine(vector1, vector8)
for text8 in sent:
vector9 = self.text_to_vector(text4)
cosine = self.get_cosine(vector1, vector9)
for text9 in sent:
vector10 = self.text_to_vector(text9)
cosine = self.get_cosine(vector1, vector10)
Plagiarism detection in text documents
if(maxi<cosine):
maxi=cosine
cosine_mat[row]=maxi
row+=1
return cosine_mat
def normalise(self,word):
word = word.lower()
word = self.ps.stem(word)
return word
def reset(self):
self.sample1_in.setText("")
self.sample2_in.setText("")
self.sample3_in.setText("")
self.sample3_in.hide()
self.result.hide()
def OpenFileNamesDialog1(self):
options = QFileDialog.Options()
options |= QFileDialog.DontUseNativeDialog
fileName, _ = QFileDialog.getOpenFileName(self, "Select
File","","Text Files (*.txt)", options=options)
if fileName:
self.sample1_in.setText(fileName)
Plagiarism detection in text documents
def OpenFileNamesDialog2(self):
options = QFileDialog.Options()
options |= QFileDialog.DontUseNativeDialog
fileName, _ = QFileDialog.getOpenFileName(self, "Select
File", " ","Text Files (*.txt)", options=options)
if fileName:
self.sample2_in.setText(fileName)
if __name__ == "__main__":
app = QtWidgets.QApplication(sys.argv)
mainWin = MainWindow()
mainWin.show()
sys.exit(app.exec_()
