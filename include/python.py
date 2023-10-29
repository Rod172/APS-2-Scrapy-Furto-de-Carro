import requests
from bs4 import BeautifulSoup

# URL da página a ser acessada
url = "URL_DA_PÁGINA_AQUI"

# Realize uma solicitação GET para a página
response = requests.get(url)

# Verifique se a solicitação foi bem-sucedida
if response.status_code == 200:
    # Parse o conteúdo da página com BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontre os links de download e faça o download dos dados
    links = soup.find_all('a', text="FURTO DE VEÍCULO")
    for link in links:
        download_url = link.get("href")
        # Use a biblioteca requests para baixar o arquivo
        response = requests.get(download_url)
        # Salve o arquivo no seu sistema
        with open("nome_do_arquivo.zip", "wb") as file:
            file.write(response.content)
else:
    print("Falha ao acessar a página")