# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

from mpl_toolkits.mplot3d import Axes3D
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm
matplotlib.use('Qt5Agg')
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection

import RubikAbstraction, rubik, solver

class RubikCube:
    def __init__(self):
        self.faces = dict()
        self.faces['F']=['r', 'r', 'r', 'r']
        self.faces['B']=['o', 'o', 'o', 'o']
        self.faces['D']=['y', 'y', 'y', 'y']
        self.faces['U']=['w', 'w', 'w', 'w']
        self.faces['L']=['g', 'g', 'g', 'g']
        self.faces['R']=['b', 'b', 'b', 'b']

        self.face_color = dict()
        self.get_face_color()

        self.edges = dict()
        self.reset_edges()

    def draw(self, axes):
        all_faces = ['F', 'B', 'L', 'R', 'U', 'D']
        for af in all_faces:
            faces = Poly3DCollection(self.edges[af], linewidths=1, edgecolors='k')
            faces.set_facecolors(self.face_color[af])
            axes.add_collection3d(faces)
        axes.set_xlim(-1.5, 1.5)
        axes.set_ylim(-1.5, 1.5)
        axes.set_zlim(-1.5, 1.5)
        axes.set_aspect('equal')
        axes._axis3don = False

    def rotate(self, yaw, pitch, roll):
        self.reset_edges()
        Ryaw = np.array([[np.cos(yaw), -np.sin(yaw), 0],
                         [np.sin(yaw), np.cos(yaw), 0],
                         [0, 0, 1]])
        Rpitch = np.array([[np.cos(pitch), 0, np.sin(pitch)],
                           [0, 1, 0],
                           [-np.sin(pitch), 0, np.cos(pitch)]])
        Rroll = np.array([[1, 0, 0],
                          [0, np.cos(roll), -np.sin(roll)],
                          [0, np.sin(roll), np.cos(roll)]])
        for key in self.edges.keys():
            self.edges[key] = self.edges[key].dot(Ryaw).dot(Rpitch).dot(Rroll)

    def reset_edges(self):
        self.edges['F'] = np.array([[[2, 0, 2], [2, 1, 2], [2, 1, 1], [2, 0, 1]],
                           [[2, 1, 2], [2, 2, 2], [2, 2, 1], [2, 1, 1]],
                           [[2, 0, 1], [2, 1, 1], [2, 1, 0], [2, 0, 0]],
                           [[2, 1, 1], [2, 2, 1], [2, 2, 0], [2, 1, 0]]])-1
        self.edges['B'] = np.array([
                           [[0, 1, 2], [0, 2, 2], [0, 2, 1], [0, 1, 1]],
                           [[0, 0, 2], [0, 1, 2], [0, 1, 1], [0, 0, 1]],
                           [[0, 1, 1], [0, 2, 1], [0, 2, 0], [0, 1, 0]],
                           [[0, 0, 1], [0, 1, 1], [0, 1, 0], [0, 0, 0]],
                           ])-1
        self.edges['L'] = np.array([[[0, 0, 2], [1, 0, 2], [1, 0, 1], [0, 0, 1]],
                           [[1, 0, 2], [2, 0, 2], [2, 0, 1], [1, 0, 1]],
                           [[0, 0, 1], [1, 0, 1], [1, 0, 0], [0, 0, 0]],
                           [[1, 0, 1], [2, 0, 1], [2, 0, 0], [1, 0, 0]]])-1
        self.edges['R'] = np.array([
                           [[1, 2, 2], [2, 2, 2], [2, 2, 1], [1, 2, 1]],
                           [[0, 2, 2], [1, 2, 2], [1, 2, 1], [0, 2, 1]],
                           [[1, 2, 1], [2, 2, 1], [2, 2, 0], [1, 2, 0]],
                           [[0, 2, 1], [1, 2, 1], [1, 2, 0], [0, 2, 0]]])-1
        self.edges['U'] = np.array([
                           [[0, 1, 2], [1, 1, 2], [1, 0, 2], [0, 0, 2]],
                           [[0, 2, 2], [1, 2, 2], [1, 1, 2], [0, 1, 2]],
                           [[1, 1, 2], [2, 1, 2], [2, 0, 2], [1, 0, 2]],
                           [[1, 2, 2], [2, 2, 2], [2, 1, 2], [1, 1, 2]],
                           ])-1
        self.edges['D'] = np.array([[[1, 1, 0], [2, 1, 0], [2, 0, 0], [1, 0, 0]],
                           [[1, 2, 0], [2, 2, 0], [2, 1, 0], [1, 1, 0]],
                           [[0, 1, 0], [1, 1, 0], [1, 0, 0], [0, 0, 0]],
                           [[0, 2, 0], [1, 2, 0], [1, 1, 0], [0, 1, 0]]])-1

    def get_face_color(self):
        hex2rgb = dict()
        hex2rgb['r'] = (189/255, 45/255, 69/255)
        hex2rgb['g'] = (67/255, 151/255, 106/255)
        hex2rgb['b'] = (40/255, 107/255, 176/255)
        hex2rgb['o'] = (233/255, 150/255, 77/255)
        hex2rgb['w'] = (254/255, 254/255, 254/255)
        hex2rgb['y'] = (254/255, 239/255, 80/255)

        self.face_color['F'] = [hex2rgb[f]for f in self.faces['F']]
        self.face_color['B'] = [hex2rgb[f] for f in self.faces['B']]
        self.face_color['L'] = [hex2rgb[f] for f in self.faces['L']]
        self.face_color['R'] = [hex2rgb[f] for f in self.faces['R']]
        self.face_color['U'] = [hex2rgb[f] for f in self.faces['U']]
        self.face_color['D'] = [hex2rgb[f] for f in self.faces['D']]


class my3DCanvas(FigureCanvas):
    '''Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.).'''

    def __init__(self, cube, parent=None, width=5, height=3):
        self.figure = Figure(figsize=(width, height), dpi=100)
        self.axes = self.figure.gca(projection='3d')

        cube.draw(self.axes)

        FigureCanvas.__init__(self, self.figure)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def updateMpl(self, cube):
        self.axes.cla()
        cube.draw(self.axes)
        self.draw()

class my2DCanvas(FigureCanvas):
    '''Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.).'''

    def __init__(self, solution=[], parent=None, width=5, height=3):
        self.figure = Figure(figsize=(width, height), dpi=100)
        self.axes = self.figure.gca()

        self.draw_solution(solution)

        FigureCanvas.__init__(self, self.figure)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def updateMpl(self, solution):
        self.axes.cla()
        self.draw_solution(solution)
        self.draw()

    def draw_solution(self, solution):
        im = np.ones([200, 1680, 4])
        imlib = [plt.imread('F.png'),
                 plt.imread('Fi.png'),
                 plt.imread('L.png'),
                 plt.imread('Li.png'),
                 plt.imread('U.png'),
                 plt.imread('Ui.png')]
        for i, s in enumerate(solution):
            im[:, i*120:(i+1)*120, :] = imlib[s]
        # im = np.concatenate([im[:, :840, :], im[:, 840:, :]], axis=0)
        self.axes.imshow(im)
        self.axes.set_axis_off()

    def textOutput(self, txt):
        self.axes.cla()
        self.axes.text(-1, 0.5, txt, fontsize=20)
        self.axes.set_axis_off()
        self.draw()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.cube = RubikCube()
        self.solution = []

        MainWindow.setObjectName('MainWindow')
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet('background-color: rgb(245, 245, 245);')
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName('centralwidget')
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(30, 60, 371, 241))
        font = QtGui.QFont()
        font.setFamily('Apple SD Gothic Neo')
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setStyleSheet('background-color: rgb(238, 236, 234);\n'
'border-radius: 10px;')
        self.groupBox.setFlat(True)
        self.groupBox.setCheckable(False)
        self.groupBox.setObjectName('groupBox')
        self.tabWidget = QtWidgets.QTabWidget(self.groupBox)
        self.tabWidget.setGeometry(QtCore.QRect(10, 30, 351, 161))
        self.tabWidget.setStyleSheet('margin: 6px;\n'
'border-color: #0c457e;\n'
'outline-style: outset;\n'
'border-radius: 5px;\n'
'border-width: 1px;')
        self.tabWidget.setObjectName('tabWidget')
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName('tab')
        self.comboBox = QtWidgets.QComboBox(self.tab)
        self.comboBox.addItems(['  WHITE', '  YELLOW', '  GREEN', '  RED',
        '  ORANGE', '  BLUE'])
        self.comboBox.setGeometry(QtCore.QRect(40, 20, 111, 26))
        self.comboBox.currentIndexChanged.connect(self.changeColor)
        self.comboBox.setStyleSheet('margin: 3px;\n'
'border-color: #0c457e;\n'
'border-style: outset;\n'
'border-radius: 5px;\n'
'border-width: 1px;\n'
'color: black;\n'
'background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(245, 245, 245), stop: 1 rgb(245, 245, 245));')
        self.comboBox.setObjectName('comboBox')
        self.comboBox_2 = QtWidgets.QComboBox(self.tab)
        self.comboBox_2.addItems(['  WHITE', '  YELLOW', '  GREEN', '  RED',
        '  ORANGE', '  BLUE'])
        self.comboBox_2.setGeometry(QtCore.QRect(190, 20, 111, 26))
        self.comboBox_2.currentIndexChanged.connect(self.changeColor)
        self.comboBox_2.setStyleSheet('margin: 3px;\n'
'border-color: #0c457e;\n'
'border-style: outset;\n'
'border-radius: 5px;\n'
'border-width: 1px;\n'
'color: black;\n'
'background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(245, 245, 245), stop: 1 rgb(245, 245, 245));')
        self.comboBox_2.setObjectName('comboBox_2')
        self.comboBox_3 = QtWidgets.QComboBox(self.tab)
        self.comboBox_3.addItems(['  WHITE', '  YELLOW', '  GREEN', '  RED',
        '  ORANGE', '  BLUE'])
        self.comboBox_3.setGeometry(QtCore.QRect(40, 70, 111, 26))
        self.comboBox_3.currentIndexChanged.connect(self.changeColor)
        self.comboBox_3.setStyleSheet('margin: 3px;\n'
'border-color: #0c457e;\n'
'border-style: outset;\n'
'border-radius: 5px;\n'
'border-width: 1px;\n'
'color: black;\n'
'background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(245, 245, 245), stop: 1 rgb(245, 245, 245));')
        self.comboBox_3.setObjectName('comboBox_3')
        self.comboBox_4 = QtWidgets.QComboBox(self.tab)
        self.comboBox_4.addItems(['  WHITE', '  YELLOW', '  GREEN', '  RED',
        '  ORANGE', '  BLUE'])
        self.comboBox_4.setGeometry(QtCore.QRect(190, 70, 111, 26))
        self.comboBox_4.currentIndexChanged.connect(self.changeColor)
        self.comboBox_4.setStyleSheet('margin: 3px;\n'
'border-color: #0c457e;\n'
'border-style: outset;\n'
'border-radius: 5px;\n'
'border-width: 1px;\n'
'color: black;\n'
'background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(245, 245, 245), stop: 1 rgb(245, 245, 245));')
        self.comboBox_4.setObjectName('comboBox_4')
        self.tabWidget.addTab(self.tab, '')
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName('tab_2')
        self.comboBox_8 = QtWidgets.QComboBox(self.tab_2)
        self.comboBox_8.addItems(['  WHITE', '  YELLOW', '  GREEN', '  RED',
        '  ORANGE', '  BLUE'])
        self.comboBox_8.setGeometry(QtCore.QRect(40, 70, 111, 26))
        self.comboBox_8.currentIndexChanged.connect(self.changeColor)
        self.comboBox_8.setStyleSheet('margin: 3px;\n'
'border-color: #0c457e;\n'
'border-style: outset;\n'
'border-radius: 5px;\n'
'border-width: 1px;\n'
'color: black;\n'
'background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(245, 245, 245), stop: 1 rgb(245, 245, 245));')
        self.comboBox_8.setObjectName('comboBox_8')
        self.comboBox_6 = QtWidgets.QComboBox(self.tab_2)
        self.comboBox_6.addItems(['  WHITE', '  YELLOW', '  GREEN', '  RED',
        '  ORANGE', '  BLUE'])
        self.comboBox_6.setGeometry(QtCore.QRect(190, 70, 111, 26))
        self.comboBox_6.currentIndexChanged.connect(self.changeColor)
        self.comboBox_6.setStyleSheet('margin: 3px;\n'
'border-color: #0c457e;\n'
'border-style: outset;\n'
'border-radius: 5px;\n'
'border-width: 1px;\n'
'color: black;\n'
'background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(245, 245, 245), stop: 1 rgb(245, 245, 245));')
        self.comboBox_6.setObjectName('comboBox_6')
        self.comboBox_5 = QtWidgets.QComboBox(self.tab_2)
        self.comboBox_5.addItems(['  WHITE', '  YELLOW', '  GREEN', '  RED',
        '  ORANGE', '  BLUE'])
        self.comboBox_5.setGeometry(QtCore.QRect(190, 20, 111, 26))
        self.comboBox_5.currentIndexChanged.connect(self.changeColor)
        self.comboBox_5.setStyleSheet('margin: 3px;\n'
'border-color: #0c457e;\n'
'border-style: outset;\n'
'border-radius: 5px;\n'
'border-width: 1px;\n'
'color: black;\n'
'background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(245, 245, 245), stop: 1 rgb(245, 245, 245));')
        self.comboBox_5.setObjectName('comboBox_5')
        self.comboBox_7 = QtWidgets.QComboBox(self.tab_2)
        self.comboBox_7.addItems(['  WHITE', '  YELLOW', '  GREEN', '  RED',
        '  ORANGE', '  BLUE'])
        self.comboBox_7.setGeometry(QtCore.QRect(40, 20, 111, 26))
        self.comboBox_7.currentIndexChanged.connect(self.changeColor)
        self.comboBox_7.setStyleSheet('margin: 3px;\n'
'border-color: #0c457e;\n'
'border-style: outset;\n'
'border-radius: 5px;\n'
'border-width: 1px;\n'
'color: black;\n'
'background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(245, 245, 245), stop: 1 rgb(245, 245, 245));')
        self.comboBox_7.setObjectName('comboBox_7')
        self.tabWidget.addTab(self.tab_2, '')
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName('tab_3')
        self.comboBox_12 = QtWidgets.QComboBox(self.tab_3)
        self.comboBox_12.addItems(['  WHITE', '  YELLOW', '  GREEN', '  RED',
        '  ORANGE', '  BLUE'])
        self.comboBox_12.setGeometry(QtCore.QRect(40, 70, 111, 26))
        self.comboBox_12.currentIndexChanged.connect(self.changeColor)
        self.comboBox_12.setStyleSheet('margin: 3px;\n'
'border-color: #0c457e;\n'
'border-style: outset;\n'
'border-radius: 5px;\n'
'border-width: 1px;\n'
'color: black;\n'
'background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(245, 245, 245), stop: 1 rgb(245, 245, 245));')
        self.comboBox_12.setObjectName('comboBox_12')
        self.comboBox_10 = QtWidgets.QComboBox(self.tab_3)
        self.comboBox_10.addItems(['  WHITE', '  YELLOW', '  GREEN', '  RED',
        '  ORANGE', '  BLUE'])
        self.comboBox_10.setGeometry(QtCore.QRect(190, 70, 111, 26))
        self.comboBox_10.currentIndexChanged.connect(self.changeColor)
        self.comboBox_10.setStyleSheet('margin: 3px;\n'
'border-color: #0c457e;\n'
'border-style: outset;\n'
'border-radius: 5px;\n'
'border-width: 1px;\n'
'color: black;\n'
'background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(245, 245, 245), stop: 1 rgb(245, 245, 245));')
        self.comboBox_10.setObjectName('comboBox_10')
        self.comboBox_11 = QtWidgets.QComboBox(self.tab_3)
        self.comboBox_11.addItems(['  WHITE', '  YELLOW', '  GREEN', '  RED',
        '  ORANGE', '  BLUE'])
        self.comboBox_11.setGeometry(QtCore.QRect(40, 20, 111, 26))
        self.comboBox_11.currentIndexChanged.connect(self.changeColor)
        self.comboBox_11.setStyleSheet('margin: 3px;\n'
'border-color: #0c457e;\n'
'border-style: outset;\n'
'border-radius: 5px;\n'
'border-width: 1px;\n'
'color: black;\n'
'background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(245, 245, 245), stop: 1 rgb(245, 245, 245));')
        self.comboBox_11.setObjectName('comboBox_11')
        self.comboBox_9 = QtWidgets.QComboBox(self.tab_3)
        self.comboBox_9.addItems(['  WHITE', '  YELLOW', '  GREEN', '  RED',
        '  ORANGE', '  BLUE'])
        self.comboBox_9.setGeometry(QtCore.QRect(190, 20, 111, 26))
        self.comboBox_9.currentIndexChanged.connect(self.changeColor)
        self.comboBox_9.setStyleSheet('margin: 3px;\n'
'border-color: #0c457e;\n'
'border-style: outset;\n'
'border-radius: 5px;\n'
'border-width: 1px;\n'
'color: black;\n'
'background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(245, 245, 245), stop: 1 rgb(245, 245, 245));')
        self.comboBox_9.setObjectName('comboBox_9')
        self.tabWidget.addTab(self.tab_3, '')
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName('tab_4')
        self.comboBox_16 = QtWidgets.QComboBox(self.tab_4)
        self.comboBox_16.addItems(['  WHITE', '  YELLOW', '  GREEN', '  RED',
        '  ORANGE', '  BLUE'])
        self.comboBox_16.setGeometry(QtCore.QRect(40, 70, 111, 26))
        self.comboBox_16.currentIndexChanged.connect(self.changeColor)
        self.comboBox_16.setStyleSheet('margin: 3px;\n'
'border-color: #0c457e;\n'
'border-style: outset;\n'
'border-radius: 5px;\n'
'border-width: 1px;\n'
'color: black;\n'
'background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(245, 245, 245), stop: 1 rgb(245, 245, 245));')
        self.comboBox_16.setObjectName('comboBox_16')
        self.comboBox_13 = QtWidgets.QComboBox(self.tab_4)
        self.comboBox_13.addItems(['  WHITE', '  YELLOW', '  GREEN', '  RED',
        '  ORANGE', '  BLUE'])
        self.comboBox_13.setGeometry(QtCore.QRect(190, 20, 111, 26))
        self.comboBox_13.currentIndexChanged.connect(self.changeColor)
        self.comboBox_13.setStyleSheet('margin: 3px;\n'
'border-color: #0c457e;\n'
'border-style: outset;\n'
'border-radius: 5px;\n'
'border-width: 1px;\n'
'color: black;\n'
'background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(245, 245, 245), stop: 1 rgb(245, 245, 245));')
        self.comboBox_13.setObjectName('comboBox_13')
        self.comboBox_14 = QtWidgets.QComboBox(self.tab_4)
        self.comboBox_14.addItems(['  WHITE', '  YELLOW', '  GREEN', '  RED',
        '  ORANGE', '  BLUE'])
        self.comboBox_14.setGeometry(QtCore.QRect(190, 70, 111, 26))
        self.comboBox_14.currentIndexChanged.connect(self.changeColor)
        self.comboBox_14.setStyleSheet('margin: 3px;\n'
'border-color: #0c457e;\n'
'border-style: outset;\n'
'border-radius: 5px;\n'
'border-width: 1px;\n'
'color: black;\n'
'background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(245, 245, 245), stop: 1 rgb(245, 245, 245));')
        self.comboBox_14.setObjectName('comboBox_14')
        self.comboBox_15 = QtWidgets.QComboBox(self.tab_4)
        self.comboBox_15.addItems(['  WHITE', '  YELLOW', '  GREEN', '  RED',
        '  ORANGE', '  BLUE'])
        self.comboBox_15.setGeometry(QtCore.QRect(40, 20, 111, 26))
        self.comboBox_15.currentIndexChanged.connect(self.changeColor)
        self.comboBox_15.setStyleSheet('margin: 3px;\n'
'border-color: #0c457e;\n'
'border-style: outset;\n'
'border-radius: 5px;\n'
'border-width: 1px;\n'
'color: black;\n'
'background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(245, 245, 245), stop: 1 rgb(245, 245, 245));')
        self.comboBox_15.setObjectName('comboBox_15')
        self.tabWidget.addTab(self.tab_4, '')
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName('tab_5')
        self.comboBox_20 = QtWidgets.QComboBox(self.tab_5)
        self.comboBox_20.addItems(['  WHITE', '  YELLOW', '  GREEN', '  RED',
        '  ORANGE', '  BLUE'])
        self.comboBox_20.setGeometry(QtCore.QRect(40, 70, 111, 26))
        self.comboBox_20.currentIndexChanged.connect(self.changeColor)
        self.comboBox_20.setStyleSheet('margin: 3px;\n'
'border-color: #0c457e;\n'
'border-style: outset;\n'
'border-radius: 5px;\n'
'border-width: 1px;\n'
'color: black;\n'
'background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(245, 245, 245), stop: 1 rgb(245, 245, 245));')
        self.comboBox_20.setObjectName('comboBox_20')
        self.comboBox_17 = QtWidgets.QComboBox(self.tab_5)
        self.comboBox_17.addItems(['  WHITE', '  YELLOW', '  GREEN', '  RED',
        '  ORANGE', '  BLUE'])
        self.comboBox_17.setGeometry(QtCore.QRect(190, 20, 111, 26))
        self.comboBox_17.currentIndexChanged.connect(self.changeColor)
        self.comboBox_17.setStyleSheet('margin: 3px;\n'
'border-color: #0c457e;\n'
'border-style: outset;\n'
'border-radius: 5px;\n'
'border-width: 1px;\n'
'color: black;\n'
'background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(245, 245, 245), stop: 1 rgb(245, 245, 245));')
        self.comboBox_17.setObjectName('comboBox_17')
        self.comboBox_19 = QtWidgets.QComboBox(self.tab_5)
        self.comboBox_19.addItems(['  WHITE', '  YELLOW', '  GREEN', '  RED',
        '  ORANGE', '  BLUE'])
        self.comboBox_19.setGeometry(QtCore.QRect(40, 20, 111, 26))
        self.comboBox_19.currentIndexChanged.connect(self.changeColor)
        self.comboBox_19.setStyleSheet('margin: 3px;\n'
'border-color: #0c457e;\n'
'border-style: outset;\n'
'border-radius: 5px;\n'
'border-width: 1px;\n'
'color: black;\n'
'background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(245, 245, 245), stop: 1 rgb(245, 245, 245));')
        self.comboBox_19.setObjectName('comboBox_19')
        self.comboBox_18 = QtWidgets.QComboBox(self.tab_5)
        self.comboBox_18.addItems(['  WHITE', '  YELLOW', '  GREEN', '  RED',
        '  ORANGE', '  BLUE'])
        self.comboBox_18.setGeometry(QtCore.QRect(190, 70, 111, 26))
        self.comboBox_18.currentIndexChanged.connect(self.changeColor)
        self.comboBox_18.setStyleSheet('margin: 3px;\n'
'border-color: #0c457e;\n'
'border-style: outset;\n'
'border-radius: 5px;\n'
'border-width: 1px;\n'
'color: black;\n'
'background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(245, 245, 245), stop: 1 rgb(245, 245, 245));')
        self.comboBox_18.setObjectName('comboBox_18')
        self.tabWidget.addTab(self.tab_5, '')
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName('tab_6')
        self.comboBox_24 = QtWidgets.QComboBox(self.tab_6)
        self.comboBox_24.addItems(['  WHITE', '  YELLOW', '  GREEN', '  RED',
        '  ORANGE', '  BLUE'])
        self.comboBox_24.setGeometry(QtCore.QRect(40, 70, 111, 26))
        self.comboBox_24.currentIndexChanged.connect(self.changeColor)
        self.comboBox_24.setStyleSheet('margin: 3px;\n'
'border-color: #0c457e;\n'
'border-style: outset;\n'
'border-radius: 5px;\n'
'border-width: 1px;\n'
'color: black;\n'
'background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(245, 245, 245), stop: 1 rgb(245, 245, 245));')
        self.comboBox_24.setObjectName('comboBox_24')
        self.comboBox_22 = QtWidgets.QComboBox(self.tab_6)
        self.comboBox_22.addItems(['  WHITE', '  YELLOW', '  GREEN', '  RED',
        '  ORANGE', '  BLUE'])
        self.comboBox_22.setGeometry(QtCore.QRect(190, 70, 111, 26))
        self.comboBox_22.currentIndexChanged.connect(self.changeColor)
        self.comboBox_22.setStyleSheet('margin: 3px;\n'
'border-color: #0c457e;\n'
'border-style: outset;\n'
'border-radius: 5px;\n'
'border-width: 1px;\n'
'color: black;\n'
'background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(245, 245, 245), stop: 1 rgb(245, 245, 245));')
        self.comboBox_22.setObjectName('comboBox_22')
        self.comboBox_21 = QtWidgets.QComboBox(self.tab_6)
        self.comboBox_21.addItems(['  WHITE', '  YELLOW', '  GREEN', '  RED',
        '  ORANGE', '  BLUE'])
        self.comboBox_21.setGeometry(QtCore.QRect(190, 20, 111, 26))
        self.comboBox_21.currentIndexChanged.connect(self.changeColor)
        self.comboBox_21.setStyleSheet('margin: 3px;\n'
'border-color: #0c457e;\n'
'border-style: outset;\n'
'border-radius: 5px;\n'
'border-width: 1px;\n'
'color: black;\n'
'background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(245, 245, 245), stop: 1 rgb(245, 245, 245));')
        self.comboBox_21.setObjectName('comboBox_21')
        self.comboBox_23 = QtWidgets.QComboBox(self.tab_6)
        self.comboBox_23.addItems(['  WHITE', '  YELLOW', '  GREEN', '  RED',
        '  ORANGE', '  BLUE'])
        self.comboBox_23.setGeometry(QtCore.QRect(40, 20, 111, 26))
        self.comboBox_23.currentIndexChanged.connect(self.changeColor)
        self.comboBox_23.setStyleSheet('margin: 3px;\n'
'border-color: #0c457e;\n'
'border-style: outset;\n'
'border-radius: 5px;\n'
'border-width: 1px;\n'
'color: black;\n'
'background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(245, 245, 245), stop: 1 rgb(245, 245, 245));')
        self.comboBox_23.setObjectName('comboBox_23')
        self.tabWidget.addTab(self.tab_6, '')
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(240, 200, 113, 32))
        self.pushButton.clicked.connect(self.solve)
        self.pushButton.setStyleSheet('margin: 6px;\n'
'border-color: #0c457e;\n'
'border-style: outset;\n'
'border-radius: 5px;\n'
'border-width: 1px;\n'
'color: black;\n'
'background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(245, 245, 245), stop: 1 rgb(245, 245, 245));')
        self.pushButton.setObjectName('pushButton')
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_2.setGeometry(QtCore.QRect(130, 200, 113, 32))
        self.pushButton_2.setStyleSheet('margin: 6px;\n'
'border-color: #0c457e;\n'
'border-style: outset;\n'
'border-radius: 5px;\n'
'border-width: 1px;\n'
'color: black;\n'
'background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(245, 245, 245), stop: 1 rgb(245, 245, 245));')
        self.pushButton_2.setFlat(False)
        self.pushButton_2.setObjectName('pushButton_2')
        self.pushButton_2.clicked.connect(self.resetColor)
        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox, text='Random')
        self.pushButton_3.setGeometry(QtCore.QRect(20, 200, 113, 32))
        self.pushButton_3.setStyleSheet('margin: 6px;\n'
'border-color: #0c457e;\n'
'border-style: outset;\n'
'border-radius: 5px;\n'
'border-width: 1px;\n'
'color: black;\n'
'background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(245, 245, 245), stop: 1 rgb(245, 245, 245));')
        self.pushButton_3.setFlat(False)
        self.pushButton_3.setObjectName('pushButton_3')
        self.pushButton_3.clicked.connect(self.randomFace)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(420, 60, 351, 241))
        font = QtGui.QFont()
        font.setFamily('Apple SD Gothic Neo')
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setStyleSheet('background-color: rgb(220, 226, 228);\n'
'border-radius: 10px;')
        self.groupBox_2.setFlat(True)
        self.groupBox_2.setObjectName('groupBox_2')
        self.frame = QtWidgets.QFrame(self.groupBox_2)
        self.frame.setGeometry(QtCore.QRect(40, 30, 275, 181))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName('frame')
        self.myMplCanvas = my3DCanvas(self.cube, self.frame, width=3, height=2)
        self.horizontalSlider = QtWidgets.QSlider(self.groupBox_2)
        self.horizontalSlider.setGeometry(QtCore.QRect(40, 220, 275, 22))
        self.horizontalSlider.setRange(0, np.pi*20)
        self.horizontalSlider.setValue(0)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setInvertedAppearance(False)
        self.horizontalSlider.setInvertedControls(False)
        self.horizontalSlider.setObjectName('horizontalSlider')
        self.verticalSlider = QtWidgets.QSlider(self.groupBox_2)
        self.verticalSlider.setGeometry(QtCore.QRect(320, 30, 22, 201))
        self.verticalSlider.setRange(0, np.pi*20)
        self.verticalSlider.setValue(0)
        self.verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider.setObjectName('verticalSlider')
        self.horizontalSlider.valueChanged.connect(self.rotateCube)
        self.verticalSlider.valueChanged.connect(self.rotateCube)
        self.verticalSlider_2 = QtWidgets.QSlider(self.groupBox_2)
        self.verticalSlider_2.setGeometry(QtCore.QRect(15, 30, 22, 201))
        self.verticalSlider_2.setRange(0, np.pi*20)
        self.verticalSlider_2.setValue(0)
        self.verticalSlider_2.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_2.setObjectName('verticalSlider')
        self.verticalSlider_2.valueChanged.connect(self.rotateCube)
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(30, 310, 741, 251))
        font = QtGui.QFont()
        font.setFamily('Apple SD Gothic Neo')
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setStyleSheet('background-color: rgb(225, 229, 233);\n'
'border-radius: 10px;')
        self.groupBox_3.setFlat(True)
        self.groupBox_3.setObjectName('groupBox_3')
        self.scrollArea = QtWidgets.QScrollArea(self.groupBox_3)
        self.scrollArea.setGeometry(QtCore.QRect(10, 30, 721, 211))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName('scrollArea')
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 721, 211))
        self.scrollAreaWidgetContents.setObjectName('scrollAreaWidgetContents')
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.my2DCanvas = my2DCanvas(
            parent=self.scrollAreaWidgetContents,
            width=7.5,
            height=1.5)
        self.pushButton_4 = QtWidgets.QPushButton(self.scrollAreaWidgetContents, text='Next Step')
        self.pushButton_4.setGeometry(QtCore.QRect(600, 160, 113, 32))
        self.pushButton_4.clicked.connect(self.solve_step)
        self.pushButton_4.setStyleSheet('margin: 6px;\n'
'border-color: #0c457e;\n'
'border-style: outset;\n'
'border-radius: 5px;\n'
'border-width: 1px;\n'
'color: black;\n'
'background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(245, 245, 245), stop: 1 rgb(245, 245, 245));')
        self.pushButton_4.setObjectName('pushButton_4')
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(240, 15, 281, 41))
        font = QtGui.QFont()
        font.setFamily('Apple SD Gothic Neo')
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setAutoFillBackground(False)
        self.label.setStyleSheet('color: rgb(76, 76, 76);')
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName('label')
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName('statusbar')
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.resetColor()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate('MainWindow', 'MainWindow'))
        self.groupBox.setTitle(_translate('MainWindow', 'Configuration'))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate('MainWindow', 'Front'))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate('MainWindow', 'Up'))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate('MainWindow', 'Down'))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate('MainWindow', 'Left'))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate('MainWindow', 'Right'))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), _translate('MainWindow', 'Back'))
        self.tabWidget.currentChanged.connect(self.changeFace)
        self.pushButton.setText(_translate('MainWindow', 'Solve'))
        self.pushButton_2.setText(_translate('MainWindow', 'Reset'))
        self.groupBox_2.setTitle(_translate('MainWindow', 'Visualization'))
        self.groupBox_3.setTitle(_translate('MainWindow', 'Solution'))
        self.label.setText(_translate('MainWindow', 'Rubic\'s Cube Solver'))

    def rotateCube(self):
        yaw = self.horizontalSlider.value()/10
        pitch = self.verticalSlider.value()/10
        roll = self.verticalSlider_2.value()/10
        self.cube.rotate(yaw, pitch, roll)
        self.myMplCanvas.updateMpl(self.cube)

    def changeColor(self):
        name2color = dict()
        name2color['  WHITE'] = 'w'
        name2color['  YELLOW'] = 'y'
        name2color['  GREEN'] = 'g'
        name2color['  RED'] = 'r'
        name2color['  ORANGE'] = 'o'
        name2color['  BLUE'] = 'b'
        self.cube.faces['F'] = [name2color[self.comboBox.currentText()],
                                name2color[self.comboBox_2.currentText()],
                                name2color[self.comboBox_3.currentText()],
                                name2color[self.comboBox_4.currentText()]]
        self.cube.faces['B'] = [name2color[self.comboBox_23.currentText()],
                                name2color[self.comboBox_21.currentText()],
                                name2color[self.comboBox_24.currentText()],
                                name2color[self.comboBox_22.currentText()]]
        self.cube.faces['L'] = [name2color[self.comboBox_15.currentText()],
                                name2color[self.comboBox_13.currentText()],
                                name2color[self.comboBox_16.currentText()],
                                name2color[self.comboBox_14.currentText()]]
        self.cube.faces['R'] = [name2color[self.comboBox_19.currentText()],
                                name2color[self.comboBox_17.currentText()],
                                name2color[self.comboBox_20.currentText()],
                                name2color[self.comboBox_18.currentText()]]
        self.cube.faces['U'] = [name2color[self.comboBox_8.currentText()],
                                name2color[self.comboBox_7.currentText()],
                                name2color[self.comboBox_6.currentText()],
                                name2color[self.comboBox_5.currentText()]]
        self.cube.faces['D'] = [name2color[self.comboBox_9.currentText()],
                                name2color[self.comboBox_10.currentText()],
                                name2color[self.comboBox_11.currentText()],
                                name2color[self.comboBox_12.currentText()]]

        self.cube.get_face_color()
        self.myMplCanvas.updateMpl(self.cube)

    def changeFace(self):
        index = self.tabWidget.currentIndex()
        if index == 0:
            yaw = np.pi/2
            pitch = 0
            roll = 0
        elif index == 1:
            yaw = 0
            pitch = 0
            roll = 3/2*np.pi
        elif index == 2:
            yaw = 0
            pitch = 0
            roll = np.pi/2
        elif index == 3:
            yaw = 0
            pitch = 0
            roll = 0
        elif index == 4:
            yaw = np.pi
            pitch = 0
            roll = 0
        elif index == 5:
            yaw = np.pi/2*3
            pitch = 0
            roll = 0
        self.setRot(yaw, pitch, roll)

    def setRot(self, yaw, pitch, roll):
        self.horizontalSlider.setValue(yaw*10)
        self.verticalSlider.setValue(pitch*10)
        self.verticalSlider_2.setValue(roll*10)
        self.cube.rotate(yaw, pitch, roll)
        self.myMplCanvas.updateMpl(self.cube)

    def resetColor(self):
        self.comboBox.setCurrentIndex(3)
        self.comboBox_2.setCurrentIndex(3)
        self.comboBox_3.setCurrentIndex(3)
        self.comboBox_4.setCurrentIndex(3)
        self.comboBox_5.setCurrentIndex(0)
        self.comboBox_6.setCurrentIndex(0)
        self.comboBox_7.setCurrentIndex(0)
        self.comboBox_8.setCurrentIndex(0)
        self.comboBox_9.setCurrentIndex(1)
        self.comboBox_10.setCurrentIndex(1)
        self.comboBox_11.setCurrentIndex(1)
        self.comboBox_12.setCurrentIndex(1)
        self.comboBox_13.setCurrentIndex(2)
        self.comboBox_14.setCurrentIndex(2)
        self.comboBox_15.setCurrentIndex(2)
        self.comboBox_16.setCurrentIndex(2)
        self.comboBox_17.setCurrentIndex(5)
        self.comboBox_18.setCurrentIndex(5)
        self.comboBox_19.setCurrentIndex(5)
        self.comboBox_20.setCurrentIndex(5)
        self.comboBox_21.setCurrentIndex(4)
        self.comboBox_22.setCurrentIndex(4)
        self.comboBox_23.setCurrentIndex(4)
        self.comboBox_24.setCurrentIndex(4)

        self.cube.faces = RubikAbstraction.list_to_faces(rubik.I)

        # self.cube.faces['F'] = ['r', 'r', 'r', 'g']
        # self.cube.faces['B'] = ['g', 'o', 'o', 'o']
        # self.cube.faces['L'] = ['w', 'g', 'w', 'y']
        # self.cube.faces['R'] = ['b', 'y', 'r', 'b']
        # self.cube.faces['U'] = ['b', 'o', 'w', 'w']
        # self.cube.faces['D'] = ['b', 'y', 'g', 'y']

        yaw = np.pi/2
        pitch = 0
        roll = 0
        self.setRot(yaw, pitch, roll)

        self.cube.get_face_color()
        self.myMplCanvas.updateMpl(self.cube)
        self.tabWidget.setCurrentIndex(0)

    def solve(self):
        try:
            start = RubikAbstraction.faces_to_list(self.cube.faces)
            moves = solver.shortest_path(start, rubik.I)
            if moves is None:
                self.my2DCanvas.textOutput('No Solution found in 14 steps.')
                return None
            self.solution = perm2sol(moves)
            self.solution_step=0
            self.my2DCanvas.updateMpl(self.solution)
        except:
            self.my2DCanvas.textOutput('Error found in color input.')

    def randomFace(self):
        num_steps = np.random.randint(low=1, high=15)
        operations = np.random.randint(low=0, high=6, size=num_steps)
        print(operations)
        start = rubik.I
        for o in operations:
            start = rubik.perm_apply(rubik.quarter_twists[o], start)
        self.cube.faces = RubikAbstraction.list_to_faces(start)
        self.cube.get_face_color()
        self.myMplCanvas.updateMpl(self.cube)

    def solve_step(self):
        if self.solution_step < len(self.solution):
            start = RubikAbstraction.faces_to_list(self.cube.faces)
            middle = rubik.perm_apply(rubik.quarter_twists[self.solution[self.solution_step]], start)
            self.solution_step += 1
            self.cube.faces = RubikAbstraction.list_to_faces(middle)
            self.cube.get_face_color()
            self.myMplCanvas.updateMpl(self.cube)

def perm2sol(moves):
    solution = []
    for move in moves:
        if move == rubik.F:
            solution.append(0)
        elif move == rubik.Fi:
            solution.append(1)
        elif move == rubik.L:
            solution.append(2)
        elif move == rubik.Li:
            solution.append(3)
        elif move == rubik.U:
            solution.append(4)
        elif move == rubik.Ui:
            solution.append(5)
    return solution
