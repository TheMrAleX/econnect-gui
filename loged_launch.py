import sys
# importaciones de PyQt
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QCursor, QIcon, QFontDatabase, QFont
from loged_ui import Ui_MainWindow
# de mi modulo funciones_ayuda importo todo
from ayuda import *

# establezco la funcion para cambiar icono que usare mas tarde
def cambiar_icono(boton, icono):
    boton.setIcon(QIcon(icono))


class VentanaLogin(QMainWindow):
    def __init__(self, nauta):
        super().__init__()
        # inicializando clase nauta y creando variable ruta para los datos de login guardados.
        self.nauta = nauta
        self.ruta = resource_path('res/datos/datos.json')
        # guardando en variables ruta de iconos necesarios
        self.icono_x = resource_path('res/icons/light/x.svg')
        self.icono_x_dark = resource_path('res/icons/light/x_dark.svg')
        self.icono_min = resource_path('res/icons/light/arrows-diagonal-minimize.svg')
        self.icono_min_dark = resource_path('res/icons/light/arrows-diagonal-minimize_dark.svg')
        # iconos tema oscuro
        self.dicon_x = resource_path('res/icons/dark/x.svg')
        self.dicon_x_dark = resource_path('res/icons/dark/x_dark.svg')
        self.dicon_min = resource_path('res/icons/dark/arrows-diagonal-minimize.svg')
        self.dicon_min_dark = resource_path('res/icons/dark/arrows-diagonal-minimize_dark.svg')
        # inicializo variable dragPos para el movimiento, ui para la clase de la ventana y retiro el marco del programa
        self.dragPos = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        # cargar fuente desde archivo local
        font_db = QFontDatabase()
        font_id_regular = font_db.addApplicationFont(resource_path('res/font/Roboto-Regular.ttf'))
        font_id_black = font_db.addApplicationFont(resource_path('res/font/Roboto-Black.ttf'))

        # creando fuente a partir de los archivos locales
        roboto_regular_18 = QFont('Roboto', 18)
        roboto_regular_10 = QFont('Roboto', 10)
        roboto_black_16 = QFont('Roboto', 16, QFont.Black)
        roboto_black_12 = QFont('Roboto', 12, QFont.Black)

        # aplicando fuente en los widgets que lo requieran
        self.ui.label.setFont(roboto_black_16)
        self.ui.tiempo_consumido.setFont(roboto_regular_18)
        self.ui.tiempo_disponible.setFont(roboto_regular_18)
        self.ui.boton_cerrar_2.setFont(roboto_black_12)
        self.ui.label_4.setFont(roboto_regular_10)
        # el icono WiFi y otros en la ejecucion se ve mas pequeno que en la previsualizacion de QtDesigner y con este codigo lo ajusto al tamano deseado (no se porque pasa esto D:)
        self.icon_wifi = QIcon(resource_path('res/icons/light/wifi.svg'))
        self.pixmap_wifi = self.icon_wifi.pixmap(35, 35)
        self.ui.label_wifi.setPixmap(self.pixmap_wifi)
        # agrandar iconos tiempo disponible y tiempo consumido
        self.icon_tc = QIcon(resource_path('res/icons/light/clock-play.svg'))
        self.pixmap_tc = self.icon_tc.pixmap(35, 35)
        self.ui.label_tc.setPixmap(self.pixmap_tc)
        self.icon_td = QIcon(resource_path('res/icons/light/clock-check.svg'))
        self.pixmap_td = self.icon_td.pixmap(35, 35)
        self.ui.label_td.setPixmap(self.pixmap_td)
        # estableciendo acciones para el boton de cerrar sesion
        self.ui.boton_cerrar.clicked.connect(lambda: self.close())
        self.ui.boton_cerrar.leaveEvent = self.cambiar_mouse_default_para_x
        self.ui.boton_cerrar.enterEvent = self.cambiar_mouse_seleccionar_x
        # estableciendo acciones para el boton minimizar
        self.ui.boton_minimizar.clicked.connect(lambda: self.showMinimized())
        self.ui.boton_minimizar.leaveEvent = self.cambiar_mouse_default_para_min
        self.ui.boton_minimizar.enterEvent = self.cambiar_mouse_seleccionar_min
        # estableciendo acciones para que se pueda mover la ventana por el escritorio al mantener precio ado el frame header.
        self.ui.header.setMouseTracking(True)
        self.ui.header.mousePressEvent = self.presionar_mouse_para_mover
        self.ui.header.mouseMoveEvent = self.mover_ventana
        self.ui.header.mouseReleaseEvent = self.cambiar_mouse_al_mover
        # este codigo es para obtener el tiempo disponible en la cuenta, dato muy importante y unico, gracias a Goku:D
        try:
            tiempo_disponible = self.nauta.get_time()
            self.ui.tiempo_disponible.setText(tiempo_disponible)
            # print(f'{tiempo_disponible} wenas')
        except:
            try:
                tiempo_disponible = self.nauta.reanude_login(self.ruta)
                # print(f'{tiempo_disponible} hola')
                self.ui.tiempo_disponible.setText(tiempo_disponible)
            except Exception as e:
                # print(e)
                def mostrar_alerta():
                    alerta = QMessageBox()
                    alerta.setIcon(QMessageBox.Warning)
                    alerta.setWindowTitle('Alerta')
                    alerta.setText('Hemos detectado que no cerraste sesion en tu cuenta, cerraste el programa y ahora nos es imposible recuperar la sesion, si es el caso retira el vpn, cortafuegos o conectese a una red Nauta valida y reinicie el programa, si no es el caso toque el boton, Olvidar Sesion y reinicie el programa.')
                    alerta.addButton('Recordar Sesion', QMessageBox.AcceptRole)
                    alerta.addButton('Olvidar Sesion', QMessageBox.RejectRole)
                    res = alerta.exec_()  # Esto mostrará la alerta.
                    if res == QMessageBox.AcceptRole:
                        sys.exit()
                    else:
                        escribir(False)
                        sys.exit()
                mostrar_alerta()
        # aqui inicializo la clase Cronometro para el contador de tiempo consumido y se actualiza cada segundo
        self.cronometro = Cronometro()
        self.cronometro.iniciar()
        self.time = QTimer()
        self.time.timeout.connect(self.actualizar_cronometro)
        self.time.start(10)

        # definiendo acciones para el boton de cerrar sesion
        self.ui.boton_cerrar_2.clicked.connect(self.cerrar_sesion)
        # dandole el valor indicado para el estilo de la app y aplicarlo posteriormente
        self.dark_mode = leer_modo()
        # aplicando el estilo necesario dependiendo del valor obtenido
        if self.dark_mode:
            self.ui.main.setStyleSheet('background:#333;\nborder:none')
            self.ui.content.setStyleSheet('background:#333;\nborder:none')
            self.ui.frame_10.setStyleSheet('background-color:#333;\nborder:none')
            self.ui.pushButton_8.setStyleSheet('background-color:#333;\nborder:none')
            self.ui.label_4.setStyleSheet('color:#76768f')
            self.ui.header.setStyleSheet('background-color:#333;\nborder:none')
            self.ui.frame.setStyleSheet('background-color:#333;\nborder:none')
            self.ui.boton_cerrar.setStyleSheet('QPushButton {\n    background-color: #333;\n}\n')
            self.ui.boton_minimizar.setStyleSheet('QPushButton {\n    background-color: #333;\n}\n')
            self.ui.label.setStyleSheet('color:#8989a5')
            self.ui.tiempo_consumido.setStyleSheet('color:#c0c0e8')
            self.ui.tiempo_disponible.setStyleSheet('color:#c0c0e8')
            self.ui.boton_cerrar_2.setStyleSheet('QPushButton {\n    background-color: #76768f;\n	border-radius: 3px;\n	color:white\n\n}\n\nQPushButton:hover {\n    background-color: #5c5c70;\n}\n\nQPushButton:pressed {\n    background-color: #8989a5;\n}')
            #cambiando iconos
            cambiar_icono(self.ui.boton_cerrar, self.dicon_x)
            cambiar_icono(self.ui.boton_minimizar, self.dicon_min)
            cambiar_icono(self.ui.pushButton_8, resource_path('res/icons/dark/brand-github.svg'))
            self.icon_wifi = QIcon(resource_path('res/icons/dark/wifi.svg'))
            self.pixmap_wifi = self.icon_wifi.pixmap(35, 35)
            self.ui.label_wifi.setPixmap(self.pixmap_wifi)
            self.icon_tc = QIcon(resource_path('res/icons/dark/clock-play.svg'))
            self.pixmap_tc = self.icon_tc.pixmap(35, 35)
            self.ui.label_tc.setPixmap(self.pixmap_tc)
            self.icon_td = QIcon(resource_path('res/icons/dark/clock-check.svg'))
            self.pixmap_td = self.icon_td.pixmap(35, 35)
            self.ui.label_td.setPixmap(self.pixmap_td)
        else:
            self.ui.main.setStyleSheet('background:white;\nborder:none')
            self.ui.content.setStyleSheet('background-color:white;\nborder:none;')
            self.ui.frame_10.setStyleSheet('background-color:white;\nborder:none')
            self.ui.pushButton_8.setStyleSheet('background-color:white;\nborder:none')
            self.ui.label_4.setStyleSheet('color:#000add')
            self.ui.header.setStyleSheet('background-color:white;\nborder:none')
            self.ui.frame.setStyleSheet('background-color:white;\nborder:none')
            self.ui.boton_cerrar.setStyleSheet('QPushButton {\n    background-color: white;\n}\n')
            self.ui.boton_minimizar.setStyleSheet('QPushButton {\n    background-color: white;\n}\n')
            self.ui.label.setStyleSheet('color:#000add')
            self.ui.tiempo_consumido.setStyleSheet('color:#8388f2')
            self.ui.tiempo_disponible.setStyleSheet('color:#8388f2')
            self.ui.boton_cerrar_2.setStyleSheet('QPushButton {\n    background-color: #000add;\n	border-radius: 3px;\n	color:white\n\n}\n\nQPushButton:hover {\n    background-color: #0009bf;\n}\n\nQPushButton:pressed {\n    background-color: #0937ff;\n}')
            # cambiando iconos
            cambiar_icono(self.ui.boton_cerrar, self.icono_x)
            cambiar_icono(self.ui.boton_minimizar, self.icono_min)
            cambiar_icono(self.ui.pushButton_8, resource_path('res/icons/light/brand-github.svg'))
            self.icon_wifi = QIcon(resource_path('res/icons/light/wifi.svg'))
            self.pixmap_wifi = self.icon_wifi.pixmap(35, 35)
            self.ui.label_wifi.setPixmap(self.pixmap_wifi)
            self.icon_tc = QIcon(resource_path('res/icons/light/clock-play.svg'))
            self.pixmap_tc = self.icon_tc.pixmap(35, 35)
            self.ui.label_tc.setPixmap(self.pixmap_tc)
            self.icon_td = QIcon(resource_path('res/icons/light/clock-check.svg'))
            self.pixmap_td = self.icon_td.pixmap(35, 35)
            self.ui.label_td.setPixmap(self.pixmap_td)
    # aqui va toda la logica de cerrar sesion
    def cerrar_sesion(self):
        # probamos ejecutar el primer metodo de cierre de sesion
        try:
            # establezco el error de conexion generico y desactivo el boton cerrar para evitar doble toque
            error_conexion = 'No es posible llevar a cabo la acción solicitada en este momento debido a una falta de conectividad a la red Nauta. Por favor, asegúrate de que estás correctamente conectado a la red Nauta y de que no hay cortafuegos bloqueando la conexión. Además, verifica si tienes una VPN activa que pueda estar interfiriendo con la comunicación del programa.'
            self.ui.boton_cerrar_2.setDisabled(True)
            # si al cerrar la sesion la funcion close_connection nos devuelve True entonces colocamos false para que el programa entienda que la sesion se ha cerrado.
            if self.nauta.logout():
                escribir(False)
                # importamos la ventana principal, ocultamos la actual e inicializamos la principal
                from main_launch import Login
                self.hide()
                self.close()
                ventana_main = Login()
                ventana_main.show()
            # si el cierre devuelve False habilitamos el boton y mostramos el error
            else:
                self.ui.boton_cerrar_2.setDisabled(False)
                QMessageBox.critical(self, 'Error', f'{error_conexion}')
        # si el primer metodo de cierre no funciona hacemos el segundo metodo
        except:
            try:
                # deshabilitamos el boton para evitar doble toque, hacemos un cierre con los datos guardados 
                self.ui.boton_cerrar_2.setDisabled(True)
                cerrar = self.nauta.logout_back(self.ruta)
                # print(cerrar)
                # si el cierre es igual a None es que fue correcto, cerramos esta ventana y abrimos la principal
                if cerrar==True:
                    from main_launch import Login
                    escribir(False)
                    self.hide()
                    self.close()
                    ventana_main_dos = Login()
                    ventana_main_dos.show()
                # si devuelve un error al cerrar mostramos un error generico (nunca pasa esto pero por si las dudas)
                elif cerrar == False:
                    self.ui.boton_cerrar_2.setDisabled(False)
                    QMessageBox.critical(self, 'Error', 'Error al intentar cerrar la sesion')
                else:
                    pass
            # si ningun metodo sirve devolvemos un error generico (esto nunca pasa pero por si acaso)
            except Exception as e:
                self.ui.boton_cerrar_2.setDisabled(False)
                QMessageBox.critical(self, 'Error', 'Error al intentar cerrar la sesion')
                
    # cambiamos el icono de el boton cerrar y del cursor
    def cambiar_mouse_default_para_x(self, event):
        self.setCursor(QCursor(Qt.ArrowCursor))
        if self.dark_mode:
            cambiar_icono(self.ui.boton_cerrar, self.dicon_x)
        else:
            cambiar_icono(self.ui.boton_cerrar, self.icono_x)

    def cambiar_mouse_seleccionar_x(self, event):
        self.setCursor(QCursor(Qt.PointingHandCursor))
        if self.dark_mode:
            cambiar_icono(self.ui.boton_cerrar, self.dicon_x_dark)
        else:
            cambiar_icono(self.ui.boton_cerrar, self.icono_x_dark)
    # cambiamos el icono del boton minimizr y del cursor
    def cambiar_mouse_default_para_min(self, event):
        self.setCursor(QCursor(Qt.ArrowCursor))
        if self.dark_mode:
            cambiar_icono(self.ui.boton_minimizar, self.dicon_min)
        else:
            cambiar_icono(self.ui.boton_minimizar, self.icono_min)

    def cambiar_mouse_seleccionar_min(self, event):
        self.setCursor(QCursor(Qt.PointingHandCursor))
        if self.dark_mode:
            cambiar_icono(self.ui.boton_minimizar, self.dicon_min_dark)
        else:
            cambiar_icono(self.ui.boton_minimizar, self.icono_min_dark)

    # para que detecte si precionas el frame header
    def presionar_mouse_para_mover(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = event.pos()

    # funcion para mover la ventana
    def mover_ventana(self, event):
        if event.buttons() == Qt.LeftButton:
            x = event.globalX()
            y = event.globalY()
            x_w = self.offset.x()
            y_w = self.offset.y()
            self.move(x - x_w, y - y_w)

    #cambiar mouse al mover
    def cambiar_mouse_al_mover(self, event):
        self.setCursor(QCursor(Qt.ArrowCursor))

    # funcion para actualizar cronometro
    def actualizar_cronometro(self):
        tiempo_consumido = self.cronometro.obtener_tiempo_transcurrido()
        self.ui.tiempo_consumido.setText(tiempo_consumido)


# funcion para iniciar la ventana forzozamente (lo uso para debugs)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaLogin()
    ventana.show()
    sys.exit(app.exec_())