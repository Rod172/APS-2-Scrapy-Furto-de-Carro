import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
import pandas as pd
from pathlib import Path
import os
import time


class FurtodeveiculoSpider(scrapy.Spider):
    name = "Furtodeveiculo"
    allowed_domains = ["ssp.sp.gov.br"]
    start_urls = ["https://www.ssp.sp.gov.br/transparenciassp/Consulta2022.aspx"]

    def __init__(self, *args, **kwargs):
        super(FurtodeveiculoSpider, self).__init__(*args, **kwargs)
        options = Options()
        options.headless = True  # Executar o Chrome em modo headless para não exibir a interface gráfica
        self.driver = webdriver.Edge(options=options)

    def parse(self, response):
        self.driver.get(response.url)
        time.sleep(5)  # Esperar a página carregar completamente

        # Clicar no botão "FURTO DE VEÍCULO"
        furto_veiculo_button = self.driver.find_element(
            By.ID, "cphBody_btnFurtoVeiculo"
        )
        furto_veiculo_button.click()
        time.sleep(3)  # Esperar um pouco para a próxima página carregar

        # Lista de anos e meses
        anos = ["2022", "2021", "2020"]
        meses = ["12", "11", "10", "09", "08", "07", "06", "05", "04", "03", "02", "01"]
        DOWNLOADS = Path.home() / 'Downloads'

        # Loop pelos anos e meses
        for ano in anos:
            for mes in meses:
                # Selecionar o ano
                ano_button = self.driver.find_element(By.ID, f'cphBody_lkAno{ano[2:]}')
                ano_button.click()
                time.sleep(1)  # Esperar um pouco para a próxima ação

                # Selecionar o mês
                mes_button = self.driver.find_element(By.ID, f'cphBody_lkMes{mes}')
                mes_button.click()
                time.sleep(1)  # Esperar um pouco para a próxima ação

                # Clicar no botão de exportar
                export_button = self.driver.find_element(By.ID, 'cphBody_ExportarBOLink')
                export_button.click()
                time.sleep(10)  # Esperar o download ser concluído (ajuste conforme necessário)

                # Esperar o download ser concluído e renomear o arquivo XLS baixado
                xls_filename = f'DOWNLOADS/DadosBO_{ano}_{mes}(FURTO DE VEÍCULOS).xls'
                csv_filename = f"dados_{ano}_{mes}.csv"

                # Aguarde o arquivo ser baixado completamente (ajuste conforme necessário)

                # Renomear o arquivo XLS baixado para incluir ano e mês no nome
                new_xls_filename = f"dados_{ano}_{mes}.xls"
                os.rename(xls_filename, new_xls_filename)

                # Converter XLS para CSV usando pandas
                xls_data = pd.read_excel(new_xls_filename, engine="xlrd")
                xls_data.to_csv(csv_filename, index=False)

                # Limpar o arquivo XLS após a conversão
                os.remove(new_xls_filename)

    def closed(self, reason):
        self.driver.quit()  # Fechar o navegador quando o spider é fechado
