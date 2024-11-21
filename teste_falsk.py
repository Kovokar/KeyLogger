from flask import Flask, request, send_from_directory
import os
from datetime import datetime

app = Flask(__name__)

# Diretório para salvar os arquivos enviados
UPLOAD_FOLDER = 'uploads'  # Nome do diretório para armazenar os arquivos enviados
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_unique_filename(filename):
    """Gera um nome de arquivo único, adicionando um número sequencial."""
    basename, extension = os.path.splitext(filename)
    counter = 1
    unique_filename = filename
    # Enquanto o arquivo já existir, adiciona um número sequencial ao nome
    while os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)):
        unique_filename = f"{basename}_{counter}{extension}"
        counter += 1
    return unique_filename

def adicionar_horario_ao_arquivo(file):
    """Adiciona o horário atual ao início do conteúdo do arquivo."""
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    file_content = file.read().decode('utf-8')
    # Prepara o conteúdo do arquivo com o horário no início
    new_content = f"Data e Hora de Recebimento: {current_time}\n" + file_content
    return new_content.encode('utf-8')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    # Obtemos um nome de arquivo único
    unique_filename = get_unique_filename(file.filename)

    # Adiciona o horário atual ao conteúdo do arquivo
    updated_content = adicionar_horario_ao_arquivo(file)

    # Salva o arquivo com o nome único no diretório de uploads
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    with open(file_path, 'wb') as f:
        f.write(updated_content)

    # Lê o conteúdo do arquivo atualizado e imprime
    print("Conteúdo recebido do arquivo:", updated_content.decode('utf-8'))

    return "Arquivo recebido e salvo com sucesso", 200

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    # Envia o arquivo para o cliente
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
