from flask import Flask, render_template
from pathlib import Path
import subprocess

app = Flask(__name__)

# Caminho para o diretório do seu projeto Scrapy (relativo ao diretório do aplicativo Flask)
scrapy_path = Path(__file__).resolve().parent / 'include' / 'scrapyfurto'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_scrapy')
def start_scrapy():
    # Execute o comando Scrapy aqui
    subprocess.run(['scrapy', 'crawl', 'seu_spider'], cwd=scrapy_path)

    return "Scrapy crawling iniciado!"

if __name__ == '__main__':
    app.run(debug=True)
