# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from ayuda import resource_path

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Loged")
        MainWindow.resize(320, 462)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.main = QtWidgets.QFrame(self.centralwidget)
        self.main.setGeometry(QtCore.QRect(0, 0, 320, 462))
        self.main.setMinimumSize(QtCore.QSize(320, 462))
        self.main.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.main.setFrameShadow(QtWidgets.QFrame.Raised)
        self.main.setObjectName("main")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.main)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.header = QtWidgets.QFrame(self.main)
        self.header.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.header.setFrameShadow(QtWidgets.QFrame.Raised)
        self.header.setObjectName("header")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.header)
        self.horizontalLayout_2.setContentsMargins(0, 5, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame = QtWidgets.QFrame(self.header)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_4.addWidget(self.frame_3)
        self.boton_minimizar = QtWidgets.QPushButton(self.frame)
        self.boton_minimizar.setMaximumSize(QtCore.QSize(40, 16777215))
        self.boton_minimizar.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(resource_path("res/icons/light/arrows-diagonal-minimize.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.boton_minimizar.setIcon(icon)
        self.boton_minimizar.setIconSize(QtCore.QSize(20, 20))
        self.boton_minimizar.setObjectName("boton_minimizar")
        self.horizontalLayout_4.addWidget(self.boton_minimizar)
        self.boton_cerrar = QtWidgets.QPushButton(self.frame)
        self.boton_cerrar.setMaximumSize(QtCore.QSize(40, 16777215))
        self.boton_cerrar.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(resource_path("res/icons/light/x.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.boton_cerrar.setIcon(icon1)
        self.boton_cerrar.setIconSize(QtCore.QSize(20, 20))
        self.boton_cerrar.setObjectName("boton_cerrar")
        self.horizontalLayout_4.addWidget(self.boton_cerrar)
        self.horizontalLayout_2.addWidget(self.frame)
        self.verticalLayout.addWidget(self.header)
        self.content = QtWidgets.QFrame(self.main)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.content.sizePolicy().hasHeightForWidth())
        self.content.setSizePolicy(sizePolicy)
        self.content.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.content.setFrameShadow(QtWidgets.QFrame.Raised)
        self.content.setObjectName("content")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.content)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.header_c = QtWidgets.QFrame(self.content)
        self.header_c.setMaximumSize(QtCore.QSize(16777215, 55))
        self.header_c.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.header_c.setFrameShadow(QtWidgets.QFrame.Raised)
        self.header_c.setObjectName("header_c")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.header_c)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_wifi = QtWidgets.QLabel(self.header_c)
        self.label_wifi.setMinimumSize(QtCore.QSize(35, 35))
        self.label_wifi.setMaximumSize(QtCore.QSize(35, 35))
        self.label_wifi.setText("")
        self.label_wifi.setPixmap(QtGui.QPixmap(resource_path("res/icons/light/wifi.svg")))
        self.label_wifi.setObjectName("label_wifi")
        self.horizontalLayout.addWidget(self.label_wifi)
        self.label = QtWidgets.QLabel(self.header_c)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.verticalLayout_3.addWidget(self.header_c)
        self.cont_c = QtWidgets.QFrame(self.content)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cont_c.sizePolicy().hasHeightForWidth())
        self.cont_c.setSizePolicy(sizePolicy)
        self.cont_c.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.cont_c.setFrameShadow(QtWidgets.QFrame.Raised)
        self.cont_c.setObjectName("cont_c")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.cont_c)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.tiempo_consumido_frame = QtWidgets.QFrame(self.cont_c)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tiempo_consumido_frame.sizePolicy().hasHeightForWidth())
        self.tiempo_consumido_frame.setSizePolicy(sizePolicy)
        self.tiempo_consumido_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tiempo_consumido_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.tiempo_consumido_frame.setObjectName("tiempo_consumido_frame")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.tiempo_consumido_frame)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.relleno_2 = QtWidgets.QFrame(self.tiempo_consumido_frame)
        self.relleno_2.setMinimumSize(QtCore.QSize(20, 0))
        self.relleno_2.setMaximumSize(QtCore.QSize(50, 16777215))
        self.relleno_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.relleno_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.relleno_2.setObjectName("relleno_2")
        self.horizontalLayout_3.addWidget(self.relleno_2)
        self.label_tc = QtWidgets.QLabel(self.tiempo_consumido_frame)
        self.label_tc.setMinimumSize(QtCore.QSize(35, 35))
        self.label_tc.setMaximumSize(QtCore.QSize(35, 35))
        self.label_tc.setText("")
        self.label_tc.setPixmap(QtGui.QPixmap(resource_path("res/icons/light/clock-play.svg")))
        self.label_tc.setObjectName("label_tc")
        self.horizontalLayout_3.addWidget(self.label_tc)
        self.tiempo_consumido = QtWidgets.QLabel(self.tiempo_consumido_frame)
        self.tiempo_consumido.setMinimumSize(QtCore.QSize(49, 40))
        self.tiempo_consumido.setMaximumSize(QtCore.QSize(110, 40))
        self.tiempo_consumido.setObjectName("tiempo_consumido")
        self.horizontalLayout_3.addWidget(self.tiempo_consumido)
        self.relleno = QtWidgets.QFrame(self.tiempo_consumido_frame)
        self.relleno.setMaximumSize(QtCore.QSize(60, 16777215))
        self.relleno.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.relleno.setFrameShadow(QtWidgets.QFrame.Raised)
        self.relleno.setObjectName("relleno")
        self.horizontalLayout_3.addWidget(self.relleno)
        self.verticalLayout_4.addWidget(self.tiempo_consumido_frame)
        self.tiempo_consumido_frame_2 = QtWidgets.QFrame(self.cont_c)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tiempo_consumido_frame_2.sizePolicy().hasHeightForWidth())
        self.tiempo_consumido_frame_2.setSizePolicy(sizePolicy)
        self.tiempo_consumido_frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tiempo_consumido_frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.tiempo_consumido_frame_2.setObjectName("tiempo_consumido_frame_2")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.tiempo_consumido_frame_2)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.relleno_5 = QtWidgets.QFrame(self.tiempo_consumido_frame_2)
        self.relleno_5.setMinimumSize(QtCore.QSize(20, 0))
        self.relleno_5.setMaximumSize(QtCore.QSize(50, 16777215))
        self.relleno_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.relleno_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.relleno_5.setObjectName("relleno_5")
        self.horizontalLayout_6.addWidget(self.relleno_5)
        self.label_td = QtWidgets.QLabel(self.tiempo_consumido_frame_2)
        self.label_td.setMinimumSize(QtCore.QSize(35, 35))
        self.label_td.setMaximumSize(QtCore.QSize(35, 35))
        self.label_td.setText("")
        self.label_td.setPixmap(QtGui.QPixmap(resource_path("res/icons/light/clock-check.svg")))
        self.label_td.setObjectName("label_td")
        self.horizontalLayout_6.addWidget(self.label_td)
        self.tiempo_disponible = QtWidgets.QLabel(self.tiempo_consumido_frame_2)
        self.tiempo_disponible.setMinimumSize(QtCore.QSize(49, 40))
        self.tiempo_disponible.setMaximumSize(QtCore.QSize(110, 40))
        self.tiempo_disponible.setObjectName("tiempo_disponible")
        self.horizontalLayout_6.addWidget(self.tiempo_disponible)
        self.relleno_6 = QtWidgets.QFrame(self.tiempo_consumido_frame_2)
        self.relleno_6.setMaximumSize(QtCore.QSize(60, 16777215))
        self.relleno_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.relleno_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.relleno_6.setObjectName("relleno_6")
        self.horizontalLayout_6.addWidget(self.relleno_6)
        self.verticalLayout_4.addWidget(self.tiempo_consumido_frame_2)
        self.frame_4 = QtWidgets.QFrame(self.cont_c)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.frame_2 = QtWidgets.QFrame(self.frame_4)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.boton_cerrar_2 = QtWidgets.QPushButton(self.frame_2)
        self.boton_cerrar_2.setMinimumSize(QtCore.QSize(160, 40))
        self.boton_cerrar_2.setMaximumSize(QtCore.QSize(120, 30))
        self.boton_cerrar_2.setObjectName("boton_cerrar_2")
        self.verticalLayout_6.addWidget(self.boton_cerrar_2, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.verticalLayout_5.addWidget(self.frame_2)
        self.verticalLayout_4.addWidget(self.frame_4)
        self.verticalLayout_3.addWidget(self.cont_c)
        self.footer_c = QtWidgets.QFrame(self.content)
        self.footer_c.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.footer_c.setFrameShadow(QtWidgets.QFrame.Raised)
        self.footer_c.setObjectName("footer_c")
        self.verticalLayout_3.addWidget(self.footer_c)
        self.verticalLayout.addWidget(self.content)
        self.footer = QtWidgets.QFrame(self.main)
        self.footer.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.footer.setFrameShadow(QtWidgets.QFrame.Raised)
        self.footer.setObjectName("footer")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.footer)
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.frame_10 = QtWidgets.QFrame(self.footer)
        self.frame_10.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_10.setObjectName("frame_10")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.frame_10)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.pushButton_8 = QtWidgets.QPushButton(self.frame_10)
        self.pushButton_8.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButton_8.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(resource_path("res/icons/light/brand-github.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_8.setIcon(icon2)
        self.pushButton_8.setIconSize(QtCore.QSize(24, 24))
        self.pushButton_8.setObjectName("pushButton_8")
        self.horizontalLayout_11.addWidget(self.pushButton_8, 0, QtCore.Qt.AlignBottom)
        self.label_4 = QtWidgets.QLabel(self.frame_10)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_11.addWidget(self.label_4)
        self.frame_11 = QtWidgets.QFrame(self.frame_10)
        self.frame_11.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_11.setObjectName("frame_11")
        self.horizontalLayout_11.addWidget(self.frame_11)
        self.horizontalLayout_10.addWidget(self.frame_10, 0, QtCore.Qt.AlignBottom)
        self.verticalLayout.addWidget(self.footer)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Loged", "Loged"))
        self.label.setText(_translate("Loged", "Conectado a Internet"))
        self.tiempo_consumido.setText(_translate("Loged", "00:00:00"))
        self.tiempo_disponible.setText(_translate("Loged", "00:00:00"))
        self.boton_cerrar_2.setText(_translate("Loged", "Cerrar"))
        self.label_4.setText(_translate("Loged", "TheMrAleX"))