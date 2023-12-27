import sys, os, pickle, time

def resource_path(relpat):
    # una funcion de pyinstaller para gestionar rutas

    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relpat)

# almaceno en la variable login la ruta del archivo login pasada por la funcion de pyinstaller
login = resource_path('res/datos/login.enet')

def leer_login():
    # esta funcion lee el archivo login y verifica con 0 y 1 si hay o no hay un login abierto (0 false, 1 true)
    with open(login, 'rb') as archivo:
        dato = pickle.load(archivo)
    valor = dato['login']
    if valor == 0:
        return False
    else:
        return True
    
def escribir(var=None):
    # esta funcion escribe en el archivo login un 1 y un 0 dependiendo si iniciamos sesion o no
    if var is True:
        # si le pasamos True como argumento a la funcion escribira 1 en el archivo dando por hecho que se inicio la sesion
        with open(login, 'rb') as archivo:
            datos = pickle.load(archivo)
        datos['login'] = 1
    
        with open(login, 'wb') as archivo1:
            pickle.dump(datos, archivo1)

        return True
    
    elif var is False:
        # si le pasamos True como argumento a la funcion escribira 0 en el archivo dando por hecho que se cerro la sesion
        with open(login, 'rb') as archivo:
            datos = pickle.load(archivo)
        datos['login'] = 0
    
        with open(login, 'wb') as archivo1:
            pickle.dump(datos, archivo1)
        return False
    
    elif var is None:
        # aqui gestiono por si se me olvida pasarle algun argumento
        print('Ningun valor ah sido pasado como argumento, no se realizara ninguna accion')
        return None
    else:
        # aqui gestiono por si paso algun argumento no valido
        print('Ningun valor correcto ah sido pasado como argumento, no se realizara ninguna accion')
        return ''

class Cronometro:
    # clase que imita un cronometro simple
    def __init__(self):
        # el constructor da inicio a la variable inicio con None
        self.inicio = None
    def iniciar(self):
        # el metodo iniciar captura el tiempo que es cuando se ejecuta el metodo
        self.inicio = time.time()
    def obtener_tiempo_transcurrido(self):
        # el metodo obtener tiempo, verifica si self.inicio no es None, si no lo es resta la hora actual con la capturada al dar inicio
        if self.inicio is None:
            return '00:00:00'
        tiempo_transcurrido = time.time() - self.inicio
        # aqui se obtienen las horas minutos y segundos ya convertidos
        horas = int(tiempo_transcurrido // 3600)
        minutos = int((tiempo_transcurrido % 3600) // 60)
        segundos = int(tiempo_transcurrido % 60)
        # y retornamos una cadena de texto formateada {hh:mm:ss}
        return f'{horas:02d}:{minutos:02d}:{segundos:02d}'
    
def leer_modo():
# esta funcion lee el archivo login donde se almacena el valor de la clave modo, si es 0 o 1 para el modo claro y oscuro respectivamente
    with open(login, 'rb') as archivo:
        dato = pickle.load(archivo)
    if dato['mod'] == 0:
        return False
    else:
        return True

def modo(modo=None):
    # esta funcion al pasarle como argumento 'claro' o 'oscuro', escribira el correspondiente valor en el archivo de modo
    if modo == 'claro':
        with open(login, 'rb') as archivo:
            dato = pickle.load(archivo)
            print(dato)
        dato['mod'] = 0

        with open(login, 'wb') as archivo1:
            pickle.dump(dato, archivo1)
            
    elif modo == 'oscuro':
        with open(login, 'rb') as archivo:
            dato = pickle.load(archivo)
            print(dato)
        dato['mod'] = 1

        with open(login, 'wb+') as archivo1:
            pickle.dump(dato, archivo1)
    else:
        print('modo inc')

# en este archivo guardamos todos los usuarios guardados y en la variable users almacenamos su ruta
users = resource_path('res/datos/users.enet')
def cargar_datos():
    # esta funcion obtiene los usuarios guardados en el archivo y los retorna
    with open(users, 'rb') as archivo:
        return pickle.load(archivo)

def guardar_datos(u,p):
    # esta funcion es para guardar un usuario y contrasena que le pasemos como argumento
    datos = cargar_datos()
    datos[u] = p
    with open(users, 'wb') as archivo1:
        pickle.dump(datos, archivo1)
    
def buscar_coincidencias(text):
    # esta funcion es para un buscador integrado en el programa recorre todos los usuarios guardados y revisa si el argumento que le pasamos es igual al empezar del usuario escrito y si es asi se retorna el usuario y contrasena para su posterior uso
    datos = cargar_datos()
    for coincidencia in datos:
        if coincidencia.startswith(text):
            password = datos[coincidencia]
            return coincidencia, password
        else:
            pass

# en este archivo guardo el ultimo usuario que inicio sesion correctamente para recomendarlo en el proximo inicio del programa
last = resource_path('res/datos/last_save.enet')

def cargar_datos_last():
    with open(last, 'rb') as datos:
        return pickle.load(datos)

def guardar_datos_last(u, p):
    datos = {u:p}
    with open(last, 'wb') as archivo:
        pickle.dump(datos, archivo)


def cargar_usuario_verificado():
    dic = cargar_datos_last()
    for usuario in dic:
        return usuario, dic[usuario]
# print(pickle.load(open('res/datos/login.enet', 'rb')))


"""with open('res/datos/last_save.enet', 'wb')as a:
    d= {}
    pickle.dump(d, a)"""