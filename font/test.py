import ssl
import socket
import requests
from enet import econnect
def verificar_ssl(url):
    try:
        host = url.split('//')[1].split('/')[0]
        
        context = ssl.create_default_context()
        with socket.create_connection((host, 8443)) as conexion:
            print('valido')
    except ssl.SSLCertVerificationError as e:
        print(f'error {e}')
    except Exception as e:
        print(f'error {e}')
        
# verificar_ssl('https://secure.etecsa.net')

