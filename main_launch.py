import sys

from main_ui import Ui_MainWindow as login_ui
from PyQt5.QtWidgets import QMainWindow, QApplication, QCompleter, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt, QStringListModel
from PyQt5 import QtGui
from PyQt5.QtGui import QFontDatabase, QFont, QIcon, QCursor

from enet import econnect
from ayuda import resource_path, cargar_usuario_verificado, guardar_datos, guardar_datos_last, escribir, modo, leer_modo, buscar_coincidencias, leer_login

from loged_launch import VentanaLogin

def cambiar_icono(boton, icono):
    boton.setIcon(QIcon(icono))

class Login(QMainWindow):
    def __init__(self):
        super().__init__()
        # inicializamos en la variable ui la instancia de login_ui
        self.ui = login_ui()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.ui.setupUi(self)
        # creamos una instancia de la clase nauta del modulo econnect.
        self.nauta = econnect.nauta()
        self.dark_mode = False
        # creando y personalizando el widget QCompleter.
        self.completer = QCompleter()
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.popup().setStyleSheet('background-color:#f2f2f2;\ncolor:#6065e1')
        # definiendo variables con las rutas de los iconos utilizados.
        self.icono_x = resource_path('res/icons/light/x.svg')
        self.icono_x_dark = resource_path('res/icons/light/x_dark.svg')
        self.icono_min = resource_path('res/icons/light/arrows-diagonal-minimize.svg')
        self.icono_min_dark = resource_path('res/icons/light/arrows-diagonal-minimize_dark.svg')
        self.icono_unview = resource_path('res/icons/light/eye-closed.svg')
        self.icono_unview_dark = resource_path('res/icons/light/eye-closed_dark.svg')
        self.icono_view = resource_path('res/icons/light/eye.svg')
        self.icono_view_dark = resource_path('res/icons/light/eye_dark.svg')
        roboto_regular = resource_path('res/font/Roboto-Regular.ttf')
        roboto_black = resource_path('res/font/Roboto-Black.ttf')
        self.dicon_x = resource_path('res/icons/dark/x.svg')
        self.dicon_min = resource_path('res/icons/dark/arrows-diagonal-minimize.svg')
        self.dicon_view = resource_path('res/icons/dark/eye.svg')
        self.dicon_view_dark = resource_path('res/icons/dark/eye_dark.svg')
        self.dicon_unview = resource_path('res/icons/dark/eye-closed.svg')
        self.dicon_unview_dark = resource_path('res/icons/dark/eye-closed_dark.svg')

        # cargar fuente desde archivo local para evitar una mala visualizacion en sistemas que no tengan la fuente Roboto
        font_db = QFontDatabase()
        font_id_regular = font_db.addApplicationFont(roboto_regular)
        font_id_black = font_db.addApplicationFont(roboto_black)
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
            self.cambiar_modo('oscuro')
        else:
            self.cambiar_modo('claro')
        # este fragmento es parte de una funcion que al iniciar sesion guarda el ultimo usuario valido que inicio sesion y lo sugiere por defecto.
        if cargar_usuario_verificado() is None:
            pass
        else:
            userl, passwordl = cargar_usuario_verificado()
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
        print(usuario, password)
        try:
            # si el metodo verify_conection de econnect nos devuelve True intentamos iniciar, si no es asi lanzamos el error de conexion
            conexion = self.nauta.test_net()
            print(conexion)
            if conexion:
                self.ui.boton_iniciar.setText('Conectando...')
                inicio = self.nauta.login_net(usuario, password)
                print(inicio)
                # hacemos el inicio con el usuario y la contrasena anteriormente guardada y si nos devuelve true
                # cerramos la ventana y abrimos la de login heredando la instancia nauta.
                if inicio == True:
                    # aqui si el inicio fue correcto guardamos el usuario y contrasena para ser sugeridos el proximo inicio de sesion.
                    guardar_datos(usuario, password)
                    guardar_datos_last(usuario, password)
                    # aqui guardamos los datos necesarios para recuperar la sesion en caso de que el programa se cierre poder recuperarla.
                    self.nauta.save_data(resource_path('res/datos/datos.json'))
                    # aqui inicializamos la ventana de login y cerramos la actual
                    ventana_login = VentanaLogin(self.nauta)
                    self.close()
                    ventana_login.show()
                    # aqui escribimos True para que el programa al abrir entienda que la sesion esta iniciada por si es cerrado sea capaz de recordar la sesion.
                    escribir(True)

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
            print(f'{e}')
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
            cambiar_icono(self.ui.boton_cerrar, self.dicon_x)
        else:
            cambiar_icono(self.ui.boton_cerrar, self.icono_x)

    # cambiar mouse a puntero normal y cambiar icono minimizar a normal
    def cambiar_mouse_default_para_minimizar(self, event):
        self.setCursor(QCursor(Qt.ArrowCursor))
        if self.dark_mode:
            cambiar_icono(self.ui.boton_minimizar, self.dicon_min)
        else:
            cambiar_icono(self.ui.boton_minimizar, self.icono_min)

    # cambiar puntero a seleccion para x dark
    def cambiar_cursor_seleccionar_x(self, event):
        self.setCursor(QCursor(Qt.PointingHandCursor))
        if self.dark_mode:
            cambiar_icono(self.ui.boton_cerrar, resource_path('res/icons/dark/x_dark.svg'))
        else:
            cambiar_icono(self.ui.boton_cerrar, self.icono_x_dark)

    # cambiar puntero para seleccion min dark
    def cambiar_cursor_seleccionar_min(self, event):
        self.setCursor(QCursor(Qt.PointingHandCursor))
        if self.dark_mode:
            cambiar_icono(self.ui.boton_minimizar, resource_path('res/icons/dark/arrows-diagonal-minimize_dark.svg'))
        else:
            cambiar_icono(self.ui.boton_minimizar, self.icono_min_dark)

    # boton de ver pass
    def ver_contrasena(self, check):
        if check:
            self.check_ver = True
            self.ui.pass_entry.setEchoMode(QLineEdit.Normal)
            if self.dark_mode:
                cambiar_icono(self.ui.view_buttom, self.dicon_view_dark)
            else:
                cambiar_icono(self.ui.view_buttom, self.icono_view_dark)
            self.ui.pass_entry.setPlaceholderText('Contraseña')
        else:
            self.check_ver = False
            self.ui.pass_entry.setEchoMode(QLineEdit.Password)
            if self.dark_mode:
                cambiar_icono(self.ui.view_buttom, self.dicon_unview_dark)
            else:
                cambiar_icono(self.ui.view_buttom, self.icono_unview_dark)
            self.ui.pass_entry.setPlaceholderText('*********')
    # evento al entrar al boton de ver pass
    def enter_buttom_ver(self, event):
        if self.ui.view_buttom.isChecked():
            if self.dark_mode:
                cambiar_icono(self.ui.view_buttom, self.dicon_view_dark)
                self.setCursor(QCursor(Qt.PointingHandCursor))
            else:
                self.ui.view_buttom.setIcon(QIcon(self.icono_view_dark))
                self.setCursor(QCursor(Qt.PointingHandCursor))
        else:
            if self.dark_mode:
                cambiar_icono(self.ui.view_buttom, self.dicon_unview_dark)
                self.setCursor(QCursor(Qt.PointingHandCursor))
            else:
                self.ui.view_buttom.setIcon(QIcon(self.icono_unview_dark))
                self.setCursor(QCursor(Qt.PointingHandCursor))
    # evento al salir del boton ver pass
    def leave_buttom_ver(self, event):
        if self.ui.view_buttom.isChecked():
            if self.dark_mode:
                cambiar_icono(self.ui.view_buttom, self.dicon_view)
                self.setCursor(QCursor(Qt.ArrowCursor))
            else:
                self.ui.view_buttom.setIcon(QIcon(self.icono_view))
                self.setCursor(QCursor(Qt.ArrowCursor))
        else:
            if self.dark_mode:
                cambiar_icono(self.ui.view_buttom, self.dicon_unview)
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
            modo('oscuro')
            self.ui.boton_modo.setChecked(True)
            self.dark_mode = leer_modo()
            self.completer.popup().setStyleSheet('background-color:#454545;\ncolor:white')
            cambiar_icono(self.ui.boton_modo, resource_path('res/icons/dark/sun.svg'))
            self.ui.main.setStyleSheet('background-color:#333')
            self.ui.content.setStyleSheet('background-color: #333;\nborder:none;')
            self.ui.label_2.setPixmap(QtGui.QPixmap(resource_path("res/icons/dark/Logo_Etecsa.png")))
            self.ui.label_3.setStyleSheet('color: #76768f')
            self.ui.label_4.setPixmap(QtGui.QPixmap(resource_path("res/icons/dark/user-shield.svg")))
            self.ui.label_5.setPixmap(QtGui.QPixmap(resource_path("res/icons/dark/password-user.svg")))
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
            cambiar_icono(self.ui.pushButton_5, resource_path('res/icons/dark/brand-github.svg'))
            # cambiar_icono(self.ui.pushButton_4, 'icons/dark/settings-code.svg')
            cambiar_icono(self.ui.boton_cerrar, self.dicon_x)
            cambiar_icono(self.ui.boton_minimizar, self.dicon_min)
            if self.check_ver:
                cambiar_icono(self.ui.view_buttom, resource_path('res/icons/dark/eye.svg'))
            else:
                cambiar_icono(self.ui.view_buttom, resource_path('res/icons/dark/eye-closed.svg'))
        else:
            modo('claro')
            self.ui.boton_modo.setChecked(False)
            self.dark_mode = leer_modo()
            self.completer.popup().setStyleSheet('background-color:#f2f2f2;\ncolor:#6065e1')
            cambiar_icono(self.ui.boton_modo, resource_path('res/icons/light/moon.svg'))
            self.ui.main.setStyleSheet('background-color:white')
            self.ui.content.setStyleSheet('background-color: white;\nborder:none;')
            self.ui.label_2.setPixmap(QtGui.QPixmap(resource_path("res/icons/light/Logo_Etecsa.png")))
            self.ui.label_3.setStyleSheet('color: #000add')
            self.ui.label_4.setPixmap(QtGui.QPixmap(resource_path("res/icons/light/user-shield.svg")))
            self.ui.label_5.setPixmap(QtGui.QPixmap(resource_path("res/icons/light/password-user.svg")))
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
            cambiar_icono(self.ui.pushButton_5, resource_path('res/icons/light/brand-github.svg'))
            # cambiar_icono(self.ui.pushButton_4, 'icons/light/settings-code.svg')
            cambiar_icono(self.ui.boton_cerrar, self.icono_x)
            cambiar_icono(self.ui.boton_minimizar, self.icono_min)
            if self.check_ver:
                cambiar_icono(self.ui.view_buttom, resource_path('res/icons/light/eye.svg'))
            else:
                cambiar_icono(self.ui.view_buttom, resource_path('res/icons/light/eye-closed.svg'))

# codigo para instanciar la clase y ejecutarla.
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Login()
    if leer_login():
        ventana_login = VentanaLogin(ventana.nauta)
        ventana_login.show()
    else:
        ventana.show()
    sys.exit(app.exec_())