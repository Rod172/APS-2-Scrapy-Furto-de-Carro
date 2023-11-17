from flask import Flask, render_template, request
from flask_cors import CORS
from pathlib import Path
import subprocess

app = Flask(__name__, template_folder=Path(__file__).resolve().parent)
CORS(app)

# Caminho para o diretório do seu projeto Scrapy (relativo ao diretório do aplicativo Flask)
scrapy_path = Path(__file__).resolve().parent / 'include' / 'scrapyfurto'

@app.route('/')
def index():
    return render_template('Home.html')

@app.route('/start_server', methods=['POST'])
def start_server():
    try:
        subprocess.Popen(["./start_server.sh"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return "Server started!"
    except Exception as e:
        return str(e)

@app.route('/start_scrapy', methods=['POST'])
def start_scrapy():
    if request.method == 'POST':
        # Execute o comando Scrapy aqui
        subprocess.run(['scrapy', 'crawl', 'Furtodeveiculo'], cwd=scrapy_path)

        return "Scrapy crawling iniciado!"
    else:
        return "Método não permitido", 405

if __name__ == '__main__':
    app.run(debug=True)
