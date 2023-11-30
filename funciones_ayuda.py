import json
import time


def leer_login():
    with open('datos/login.json', 'r') as archivo:
        dato = json.load(archivo)
    valor = dato['login']
    if valor == 0:
        return False
    else:
        return True


def escribir_true():
    with open('datos/login.json', 'r') as archivo:
        dato = json.load(archivo)
    dato['login'] = 1

    with open('datos/login.json', 'w') as archivo:
        json.dump(dato, archivo)


def escribir_false():
    with open('datos/login.json', 'r') as archivo:
        dato = json.load(archivo)
    dato['login'] = 0

    with open('datos/login.json', 'w') as archivo:
        json.dump(dato, archivo)


class Cronometro:
    def __init__(self):
        self.inicio = None

    def iniciar_cronometro(self):
        self.inicio = time.time()

    def obtener_tiempo_transcurrido(self):
        if self.inicio is None:
            return "00:00:00"

        tiempo_actual = time.time() - self.inicio
        horas = int(tiempo_actual // 3600)
        minutos = int((tiempo_actual % 3600) // 60)
        segundos = int(tiempo_actual % 60)

        return f"{horas:02d}:{minutos:02d}:{segundos:02d}"


# leer modo
def leer_modo():
    with open('datos/login.json', 'r') as archivo1:
        dato1 = json.load(archivo1)
    valor = dato1['mod']
    if valor == 0:
        return False
    else:
        return True


def modo_claro():
    with open('datos/login.json', 'r') as archivo2:
        dato2 = json.load(archivo2)
    dato2['mod'] = 0

    with open('datos/login.json', 'w') as archivo3:
        json.dump(dato2, archivo3)


def modo_oscuro():
    with open('datos/login.json', 'r') as archivo:
        dato = json.load(archivo)
    dato['mod'] = 1

    with open('datos/login.json', 'w') as archivo:
        json.dump(dato, archivo)


# users

def cargar_datos():
    try:
        with open('datos/users.json', 'r') as datos:
            return json.load(datos)
    except FileNotFoundError:
        return {}


def guardar_datos(user, passw):
    dic = cargar_datos()
    dic[user] = passw
    with open('datos/users.json', 'w') as archivo:
        json.dump(dic, archivo)


def buscar_coincidencias(texto):
    dic = cargar_datos()
    for coincidencia in dic:
        if coincidencia.startswith(texto):
            passw = dic[coincidencia]
            return coincidencia, passw
        else:
            pass


# ultimo uso
def cargar_datos_last():
    try:
        with open('datos/last_save.json', 'r') as datos:
            return json.load(datos)
    except FileNotFoundError:
        return {}


def guardar_datos_last(user, passw):
    dic = {
        user: passw
    }
    with open('datos/last_save.json', 'w') as archivo:
        json.dump(dic, archivo)


def ver_nada():
    dic = cargar_datos_last()
    try:
        if dic['leo'] == None:
            return False
        else:
            return True
    except:
        return True


def cargar_usuario_verifica2():
    if ver_nada():
        dic = cargar_datos_last()
        for us in dic:
            return us, dic[us]
    else:
        pass


print(cargar_usuario_verifica2())
