import scrapy
import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from pathlib import Path


class FurtodeveiculoSpider(scrapy.Spider):
    name = "Furtodeveiculo"
    allowed_domains = ["ssp.sp.gov.br"]
    start_urls = ["https://www.ssp.sp.gov.br/transparenciassp/Consulta2022.aspx"]

    def __init__(self, *args, **kwargs):
        super(FurtodeveiculoSpider, self).__init__(*args, **kwargs)
        options = Options()
        # options.add_argument("headless")  # Executar o Edge em modo headless para não exibir a interface gráfica
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
        anos = ["2020", "2021", "2022"]
        meses = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
        DOWNLOADS = Path.home() / "Downloads"

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
                xls_filename_path = (f'{DOWNLOADS}/DadosBO_{ano}_{mes}(FURTO DE VEÍCULOS).xls')
                xls_filename = pd.read_csv(xls_filename_path, encoding='UTF-16-le', sep='\t', skipinitialspace=bool, dtype=str)
                csv_filename = f"dados_{ano}_{mes}.csv"

                # Aguarde o arquivo ser baixado completamente (ajuste conforme necessário)

                # # Renomear o arquivo XLS baixado para incluir ano e mês no nome
                # new_xls_filename = f"dados_{ano}_{mes}.xls"
                # os.rename(xls_filename, new_xls_filename)

                # Converter XLS para CSV usando pandas
                xls_filename.to_csv(csv_filename, index=False)
                # csv_data = pd.read_csv(csv_filename, sep='/t')#, engine="xlrd"
                # csv_data.to_csv(csv_filename, index=False)

                # Limpar o arquivo XLS após a conversão
                os.remove(xls_filename_path)
        tables = []
        for ano in anos:
            for mes in meses:
                csv_filename = f"dados_{ano}_{mes}.csv"
                if ano == 2020 and mes == 1:
                    csv = pd.read_csv(csv_filename, index_col=None, header=0)
                    tables.append(csv)
                else:
                    csv = pd.read_csv(
                        csv_filename, low_memory=False, index_col=None, header=0
                    )
                    tables.append(csv)
        result = "Todas Tabelas.csv"
        merge = pd.concat(tables)
        merge.to_csv(result, index=False)

    def closed(self, reason):
        self.driver.quit()  # Fechar o navegador quando o spider é fechado
