import os
from PyQt5.QtWidgets import*
from PyQt5.QtCore import Qt # нужна константа Qt.KeepAspectRatio для изменения размеров с сохранением пропорций
from PyQt5.QtGui import QPixmap # оптимизированная для показа на экране картинка

from PIL import Image
from PIL.ImageQt import ImageQt # для перевода графики из Pillow в Qt  
from PIL import ImageFilter
from PIL.ImageFilter import *

app = QApplication([])
win = QWidget()        
win.resize(700, 500)  
win.setWindowTitle('Easy Editor')
label1 = QLabel("Картинка")
button1 = QPushButton("Папка")
listwidget= QListWidget()

button2= QPushButton("Лево")
button3 = QPushButton("Право")
button4= QPushButton("Зеркало")
button5 = QPushButton("Резкость")
button6 = QPushButton("Ч/Б")

row = QHBoxLayout()          # Основная строка 
col1 = QVBoxLayout()         # делится на два столбца
col2 = QVBoxLayout()
col1.addWidget(button1)      # в первом - кнопка выбора директории
col1.addWidget(listwidget)     # и список файлов
col2.addWidget(label1, 95) # вo втором - картинка
row_2 = QHBoxLayout()    # и строка кнопок
row_2.addWidget(button2)
row_2.addWidget(button3)
row_2.addWidget(button4)
row_2.addWidget(button5)
row_2.addWidget(button6)
col2.addLayout(row_2)

row.addLayout(col1, 20)
row.addLayout(col2, 80)
win.setLayout(row)

win.show()

workdir = ''

def filter(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def showFilenamesList():
    extensions = ['.jpg','.jpeg', '.png', '.gif', '.bmp']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir), extensions)

    listwidget.clear()
    for filename in filenames:
        listwidget.addItem(filename)

button1.clicked.connect(showFilenamesList)

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = "Modified/"

    def loadImage(self, filename):
        ''' при загрузке запоминаем путь и имя файла '''
        self.filename = filename
        fullname = os.path.join(workdir, filename)
        self.image = Image.open(fullname)

    def saveImage(self):
        ''' сохраняет копию файла в подпапке '''
        path = os.path.join(workdir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        fullname = os.path.join(path, self.filename)
        self.image.save(fullname)

    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_sharpen(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def showImage(self, path):
        label1.hide()
        pixmapimage = QPixmap(path)
        w, h = label1.width(), label1.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        label1.setPixmap(pixmapimage)
        label1.show()

def showChosenImage():
    if listwidget.currentRow() >= 0:
        filename = listwidget.currentItem().text()
        workimage.loadImage(filename)
        workimage.showImage(os.path.join(workdir, workimage.filename))

workimage = ImageProcessor() #текущая рабочая картинка для работы
listwidget.currentRowChanged.connect(showChosenImage)

button6.clicked.connect(workimage.do_bw)
button2.clicked.connect(workimage.do_left)
button3.clicked.connect(workimage.do_right)
button5.clicked.connect(workimage.do_sharpen)
button4.clicked.connect(workimage.do_flip)

app.exec()
