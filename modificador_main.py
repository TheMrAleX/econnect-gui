import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QMessageBox, QCompleter
from PyQt5.QtCore import Qt, QStringListModel
from PyQt5.QtGui import QCursor, QIcon, QFontDatabase, QFont
from PyQt5 import QtGui
from ui import Ui_MainWindow
# importations para la ui
from enet import econnect
from modificador_login import VentanaLogin
from funciones_ayuda import *


def cambiar_icono(boton, icono):
    boton.setIcon(QIcon(icono))


class MiVentana(QMainWindow):
    def __init__(self):
        super().__init__()
        # creamos una instancia de la clase nauta del modulo econnect.
        self.nauta = econnect.nauta()
        # verificamos el modo elegido por el usuario en los archivos y lo aplicamos.
        self.dark_mode = leer_modo()
        # creando y personalizando el widget QCompleter.
        self.completer = QCompleter()
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.popup().setStyleSheet('background-color:#f2f2f2;\ncolor:#6065e1')
        # definiendo variables con las rutas de los iconos utilizados.
        self.icono_x = 'icons/light/x.svg'
        self.icono_x_dark = 'icons/light/x_dark.svg'
        self.icono_min = 'icons/light/arrows-diagonal-minimize.svg'
        self.icono_min_dark = 'icons/light/arrows-diagonal-minimize_dark.svg'
        self.icono_unview = 'icons/light/eye-closed.svg'
        self.icono_unview_dark = 'icons/light/eye-closed_dark.svg'
        self.icono_view = 'icons/light/eye.svg'
        self.icono_view_dark = 'icons/light/eye_dark.svg'
        # inicializo variable dragPos para el movimiento, ui para la clase de la ventana y retiro el marco del programa
        self.dragPos = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        # cargar fuente desde archivo local para evitar una mala visualizacion en sistemas que no tengan la fuente Roboto
        font_db = QFontDatabase()
        font_id_regular = font_db.addApplicationFont('font/Roboto-Regular.ttf')
        font_id_black = font_db.addApplicationFont('font/Roboto-Black.ttf')
        # creando fuente a partir de los archivos cargados
        roboto_regular_10 = QFont('Roboto', 10)
        roboto_black_22 = QFont('Roboto', 22, QFont.Black)
        roboto_regular_10 = QFont('Roboto', 10)
        # aplicando fuentes a los widgets que lo requieran
        self.ui.label_3.setFont(roboto_black_22)
        self.ui.user_entry.setFont(roboto_regular_10)
        self.ui.pass_entry.setFont(roboto_regular_10)
        self.ui.label.setFont(roboto_regular_10)
        # acciones del boton cerrar
        self.ui.boton_cerrar.clicked.connect(lambda: self.close())
        self.ui.boton_cerrar.enterEvent = self.cambiar_cursor_seleccionar_x
        self.ui.boton_cerrar.leaveEvent = self.cambiar_mouse_default_para_x
        # acciones del boton minimizar
        self.ui.boton_minimizar.clicked.connect(lambda: self.showMinimized())
        self.ui.boton_minimizar.enterEvent = self.cambiar_cursor_seleccionar_min
        self.ui.boton_minimizar.leaveEvent = self.cambiar_mouse_default_para_minimizar
        # comportamiento del widget header para arrastrar la ventana por el escritorio
        self.ui.header.setMouseTracking(True)
        self.ui.header.mousePressEvent = self.presionar_mouse_para_mover
        self.ui.header.mouseMoveEvent = self.mover_ventana
        self.ui.header.mouseReleaseEvent = lambda event: self.setCursor(QCursor(Qt.ArrowCursor))
        # esto es para que el campo password sea oculto y no sea visible el texto del mismo
        self.ui.pass_entry.setEchoMode(QLineEdit.Password)
        # esto es para que al precionar la tecla enter se inicie sesion sin tener que mover el cursor
        self.ui.user_entry.returnPressed.connect(self.iniciar_sesion)
        self.ui.user_entry.textChanged.connect(self.autocompletado_nauta)
        self.ui.pass_entry.returnPressed.connect(self.iniciar_sesion)
        # esto es para establecer las acciones del boton para hacer visible el campo de password o no hacerlo
        self.check_ver = False
        self.ui.view_buttom.setCheckable(True)
        cambiar_icono(self.ui.view_buttom, self.icono_unview)
        self.ui.view_buttom.toggled.connect(self.ver_contrasena)
        self.ui.view_buttom.enterEvent = self.enter_buttom_ver
        self.ui.view_buttom.leaveEvent = self.leave_buttom_ver
        # esto es para establecer las acciones que hara el boton de iniciar sesion
        self.ui.boton_iniciar.clicked.connect(self.iniciar_sesion)
        self.ui.boton_iniciar.setDefault(True)
        # esto es para establecer las acciones que hara el boton de cambiar entre el modo claro y oscuro
        self.ui.boton_modo.setCheckable(True)
        self.ui.boton_modo.clicked[bool].connect(self.cambiar_modo)
        #esto es para eliminar unos bordes generales de 2 widgets en la gui y se vea mas minimalista, bordes afuera :D
        self.ui.frame_5.setStyleSheet('border:none')
        self.ui.footer.setStyleSheet('border:none')
        # este fragmento lee la variable dark_mode si es positiva cambia el boton de tema al correspondiente y aplica el tema, si dark mode no es True hace el mismo proceso para el modo claro.
        if self.dark_mode:
            self.ui.boton_modo.setChecked(True)
            self.cambiar_modo(self.dark_mode)
        else:
            self.cambiar_modo(self.dark_mode)
        # este fragmento es parte de una funcion que al iniciar sesion guarda el ultimo usuario valido que inicio sesion y lo sugiere por defecto.
        if cargar_usuario_verifica2() is None:
            pass
        else:
            userl, passwordl = cargar_usuario_verifica2()
            self.ui.user_entry.setText(userl)
            self.ui.pass_entry.setText(passwordl)

    # funcion iniciar sesion
    def iniciar_sesion(self):
        # aqui establezco el error de conexion generico, y desactivo el boton para evitar doble toques.
        error_conexion = 'No es posible llevar a cabo la acción solicitada en este momento debido a una falta de conectividad a la red Nauta.\n\nPor favor, asegúrate de que estás correctamente conectado a la red Nauta y de que no hay cortafuegos bloqueando la conexión. Además, verifica si tienes una VPN activa que pueda estar interfiriendo con la comunicación del programa.'
        self.ui.boton_iniciar.setDisabled(True)
        # obtenemos en 2 variables el texto ingresando en ambos campos
        usuario = self.ui.user_entry.text()
        password = self.ui.pass_entry.text()
        try:
            # si el metodo verify_conection de econnect nos devuelve True intentamos iniciar, si no es asi lanzamos el error de conexion
            conexion = self.nauta.test_net()
            if conexion:
                self.ui.boton_iniciar.setText('Conectando...')
                inicio = self.nauta.login_net(usuario, password)
                # hacemos el inicio con el usuario y la contrasena anteriormente guardada y si nos devuelve true
                # cerramos la ventana y abrimos la de login heredando la instancia nauta.
                if inicio == True:
                    # aqui si el inicio fue correcto guardamos el usuario y contrasena para ser sugeridos el proximo inicio de sesion.
                    guardar_datos(usuario, password)
                    guardar_datos_last(usuario, password)
                    # aqui guardamos los datos necesarios para recuperar la sesion en caso de que el programa se cierre poder recuperarla.
                    self.nauta.save_data('datos/datos.json')
                    # aqui inicializamos la ventana de login y cerramos la actual
                    ventana_login = VentanaLogin(self.nauta)
                    self.close()
                    ventana_login.show()
                    # aqui escribimos True para que el programa al abrir entienda que la sesion esta iniciada por si es cerrado sea capaz de recordar la sesion.
                    escribir_true()

                else:
                    #  si el inicio no es correcto habilitamos el boton iniciar y lanzamos el mensaje devuelto por el portal cautivo
                    self.ui.boton_iniciar.setDisabled(False)
                    self.ui.boton_iniciar.setText('Error')
                    QMessageBox.critical(self, 'Error', f'{inicio}')
                    self.ui.boton_iniciar.setText(' Iniciar')
            else:
                self.ui.boton_iniciar.setDisabled(False)
                QMessageBox.critical(self, 'Error de Conexión',f'{error_conexion}')
        # si algo falla devuelve el error en print(solo para desarrolladores si algun dia cambia algo en los servidores)
        except Exception as e:
            self.ui.boton_iniciar.setDisabled(False)
    # aqui establezco la funcion para que al precionar el mouse en el frame header se detecte.
    def presionar_mouse_para_mover(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = event.pos()

    # aqui va toda la logica para mover la ventana al mantener precionado en el frame header.
    def mover_ventana(self, event):
        if event.buttons() == Qt.LeftButton:
            x = event.globalX()
            y = event.globalY()
            x_w = self.offset.x()
            y_w = self.offset.y()
            self.move(x-x_w, y-y_w)

    # cambiar mouse a puntero y cambiar icono x a normal
    def cambiar_mouse_default_para_x(self, event):
        self.setCursor(QCursor(Qt.ArrowCursor))
        if self.dark_mode:
            cambiar_icono(self.ui.boton_cerrar, 'icons/dark/x.svg')
        else:
            cambiar_icono(self.ui.boton_cerrar, self.icono_x)

    # cambiar mouse a puntero normal y cambiar icono minimizar a normal
    def cambiar_mouse_default_para_minimizar(self, event):
        self.setCursor(QCursor(Qt.ArrowCursor))
        if self.dark_mode:
            cambiar_icono(self.ui.boton_minimizar, 'icons/dark/arrows-diagonal-minimize.svg')
        else:
            cambiar_icono(self.ui.boton_minimizar, self.icono_min)

    # cambiar puntero a seleccion para x dark
    def cambiar_cursor_seleccionar_x(self, event):
        self.setCursor(QCursor(Qt.PointingHandCursor))
        if self.dark_mode:
            cambiar_icono(self.ui.boton_cerrar, 'icons/dark/x_dark.svg')
        else:
            cambiar_icono(self.ui.boton_cerrar, self.icono_x_dark)

    # cambiar puntero para seleccion min dark
    def cambiar_cursor_seleccionar_min(self, event):
        self.setCursor(QCursor(Qt.PointingHandCursor))
        if self.dark_mode:
            cambiar_icono(self.ui.boton_minimizar, 'icons/dark/arrows-diagonal-minimize_dark.svg')
        else:
            cambiar_icono(self.ui.boton_minimizar, self.icono_min_dark)

    # boton de ver pass
    def ver_contrasena(self, check):
        if check:
            self.check_ver = True
            self.ui.pass_entry.setEchoMode(QLineEdit.Normal)
            if self.dark_mode:
                cambiar_icono(self.ui.view_buttom, 'icons/dark/eye_dark.svg')
            else:
                cambiar_icono(self.ui.view_buttom, self.icono_view_dark)
            self.ui.pass_entry.setPlaceholderText('Contraseña')
        else:
            self.check_ver = False
            self.ui.pass_entry.setEchoMode(QLineEdit.Password)
            if self.dark_mode:
                cambiar_icono(self.ui.view_buttom, 'icons/dark/eye-closed_dark.svg')
            else:
                cambiar_icono(self.ui.view_buttom, self.icono_unview_dark)
            self.ui.pass_entry.setPlaceholderText('*********')
    # evento al entrar al boton de ver pass
    def enter_buttom_ver(self, event):
        if self.ui.view_buttom.isChecked():
            if self.dark_mode:
                cambiar_icono(self.ui.view_buttom, 'icons/dark/eye_dark.svg')
                self.setCursor(QCursor(Qt.PointingHandCursor))
            else:
                self.ui.view_buttom.setIcon(QIcon(self.icono_view_dark))
                self.setCursor(QCursor(Qt.PointingHandCursor))
        else:
            if self.dark_mode:
                cambiar_icono(self.ui.view_buttom, 'icons/dark/eye-closed_dark.svg')
                self.setCursor(QCursor(Qt.PointingHandCursor))
            else:
                self.ui.view_buttom.setIcon(QIcon(self.icono_unview_dark))
                self.setCursor(QCursor(Qt.PointingHandCursor))
    # evento al salir del boton ver pass
    def leave_buttom_ver(self, event):
        if self.ui.view_buttom.isChecked():
            if self.dark_mode:
                cambiar_icono(self.ui.view_buttom, 'icons/dark/eye.svg')
                self.setCursor(QCursor(Qt.ArrowCursor))
            else:
                self.ui.view_buttom.setIcon(QIcon(self.icono_view))
                self.setCursor(QCursor(Qt.ArrowCursor))
        else:
            if self.dark_mode:
                cambiar_icono(self.ui.view_buttom, 'icons/dark/eye-closed.svg')
                self.setCursor(QCursor(Qt.ArrowCursor))
            else:
                self.ui.view_buttom.setIcon(QIcon(self.icono_unview))
                self.setCursor(QCursor(Qt.ArrowCursor))
    # logica de autocompletado
    def autocompletado_nauta(self, text):
        try:
            user, passw = buscar_coincidencias(text)
            if user != None:
                user = str(user)
                relleno = [f'{user}']
                completer_model = QStringListModel(relleno)
                self.completer.setModel(completer_model)
                self.ui.user_entry.setCompleter(self.completer)
                if [text] == relleno:
                    self.ui.pass_entry.setText(passw)
                else:
                    self.ui.pass_entry.setText('')
        except:
            relleno = [f'{text}@nauta.com.cu', f'{text}@nauta.co.cu']
            completer_model = QStringListModel(relleno)
            self.completer.setModel(completer_model)
            self.ui.user_entry.setCompleter(self.completer)
    # toda la logica y definicion de estilos segun que modo este activo
    def cambiar_modo(self, check):
        if check:
            modo_oscuro()
            self.dark_mode = leer_modo()
            self.completer.popup().setStyleSheet('background-color:#454545;\ncolor:white')
            cambiar_icono(self.ui.boton_modo, 'icons/dark/sun.svg')
            self.ui.main.setStyleSheet('background-color:#333')
            self.ui.content.setStyleSheet('background-color: #333;\nborder:none;')
            self.ui.label_2.setPixmap(QtGui.QPixmap("icons/dark/Logo_Etecsa.png"))
            self.ui.label_3.setStyleSheet('color: #76768f')
            self.ui.label_4.setPixmap(QtGui.QPixmap("icons/dark/user-shield.svg"))
            self.ui.label_5.setPixmap(QtGui.QPixmap("icons/dark/password-user.svg"))
            self.ui.user_entry.setStyleSheet('color: white')
            self.ui.frame_6.setStyleSheet('background-color:#76768f')
            self.ui.pass_entry.setStyleSheet('color: white')
            self.ui.frame_7.setStyleSheet('background-color:#76768f')
            self.ui.frame_5.setStyleSheet('background-color:#333')
            self.ui.header.setStyleSheet('background-color:#333;\nborder:none')
            self.ui.frame.setStyleSheet('background-color:#333')
            # self.ui.pushButton_4.setStyleSheet('QPushButton {\n    background-color: #333;\n}')
            self.ui.boton_minimizar.setStyleSheet('QPushButton {\n    background-color: #333;\n}')
            self.ui.boton_cerrar.setStyleSheet('QPushButton {\n    background-color: #333;\n}')
            self.ui.pushButton_5.setStyleSheet('QPushButton {\n    background-color: #333;\n}')
            self.ui.label.setStyleSheet('color: #76768f')
            self.ui.boton_iniciar.setStyleSheet('QPushButton {\n    background-color: #76768f;\n	border-radius: 3px;\n	color:white\n\n}\n\nQPushButton:hover {\n    background-color: #5c5c70;\n}\n\nQPushButton:pressed {\n    background-color: #8989a5;\n}')
            # cambiando los iconos a blanco
            cambiar_icono(self.ui.pushButton_5, 'icons/dark/brand-github.svg')
            # cambiar_icono(self.ui.pushButton_4, 'icons/dark/settings-code.svg')
            cambiar_icono(self.ui.boton_cerrar, 'icons/dark/x.svg')
            cambiar_icono(self.ui.boton_minimizar, 'icons/dark/arrows-diagonal-minimize.svg')
            if self.check_ver:
                cambiar_icono(self.ui.view_buttom, 'icons/dark/eye.svg')
            else:
                cambiar_icono(self.ui.view_buttom, 'icons/dark/eye-closed.svg')
        else:
            modo_claro()
            self.dark_mode = leer_modo()
            self.completer.popup().setStyleSheet('background-color:#f2f2f2;\ncolor:#6065e1')
            cambiar_icono(self.ui.boton_modo, 'icons/light/moon.svg')
            self.ui.main.setStyleSheet('background-color:white')
            self.ui.content.setStyleSheet('background-color: white;\nborder:none;')
            self.ui.label_2.setPixmap(QtGui.QPixmap("icons/light/Logo_Etecsa.png"))
            self.ui.label_3.setStyleSheet('color: #000add')
            self.ui.label_4.setPixmap(QtGui.QPixmap("icons/light/user-shield.svg"))
            self.ui.label_5.setPixmap(QtGui.QPixmap("icons/light/password-user.svg"))
            self.ui.user_entry.setStyleSheet('color: #000add')
            self.ui.frame_6.setStyleSheet('background-color:#000add')
            self.ui.pass_entry.setStyleSheet('color: #000add')
            self.ui.frame_7.setStyleSheet('background-color:#000add')
            self.ui.boton_iniciar.setStyleSheet('QPushButton {\n    background-color: #000add;\n	border-radius: 3px;\n	color:white\n\n}\n\nQPushButton:hover {\n    background-color: #0009bf;\n}\n\nQPushButton:pressed {\n    background-color: #0937ff;\n}')
            self.ui.frame_5.setStyleSheet('background-color:white')
            self.ui.header.setStyleSheet('background-color:white;\nborder:none')
            self.ui.frame.setStyleSheet('background-color:white')
            # self.ui.pushButton_4.setStyleSheet('QPushButton {\n    background-color: white;\n}')
            self.ui.boton_minimizar.setStyleSheet('QPushButton {\n    background-color: white;\n}')
            self.ui.boton_cerrar.setStyleSheet('QPushButton {\n    background-color: white;\n}')
            self.ui.pushButton_5.setStyleSheet('QPushButton {\n    background-color: white;\n}')
            self.ui.label.setStyleSheet('color: #000add')

            # cambiando iconos normales
            cambiar_icono(self.ui.pushButton_5, 'icons/light/brand-github.svg')
            # cambiar_icono(self.ui.pushButton_4, 'icons/light/settings-code.svg')
            cambiar_icono(self.ui.boton_cerrar, self.icono_x)
            cambiar_icono(self.ui.boton_minimizar, self.icono_min)
            if self.check_ver:
                cambiar_icono(self.ui.view_buttom, 'icons/light/eye.svg')
            else:
                cambiar_icono(self.ui.view_buttom, 'icons/light/eye-closed.svg')

# codigo para instanciar la clase y ejecutarla.
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MiVentana()
    if leer_login():
        ventana_login = VentanaLogin(ventana.nauta)
        ventana_login.show()
    else:
        ventana.show()
    sys.exit(app.exec_())