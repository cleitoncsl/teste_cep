import os
from time import sleep
from playwright.sync_api import expect, sync_playwright
from datetime import datetime

url = 'https://buscacepinter.correios.com.br/app/faixa_cep_uf_localidade/index.php'

ufs = ['AC', 'AL']

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(
        color_scheme='dark'
    )

    page = context.new_page()
    page.goto(url)
    sleep(0.2)

    # Clique Botão UF:
    page.get_by_role("combobox", name="UF:*").select_option("AL")
    sleep(0.2)
    page.get_by_role("button", name="Buscar").click()
    sleep(1)

    tbl_campo_cep_uf = page.locator('id=resultado-UF')
    colunas_campo_cep = tbl_campo_cep_uf.locator('tr')
    linha_campo_uf_cep = colunas_campo_cep.locator('td').all_text_contents()[0]
    linha_campo_faixa_cep = colunas_campo_cep.locator('td').all_text_contents()[1]

    tbl_DNEC = page.locator('id=resultado-DNEC')
    linhas_tbl_DNEX = tbl_campo_cep_uf.locator('tr')
    linhas_tbl_DNEX = tbl_DNEC.locator('tbody')
    linhas_tbl_DNEX = tbl_DNEC.locator('tr')
    linhas = linhas_tbl_DNEX

    #-localizar o botão proximo-#
    def clickproximo(Campo):
        nome_campos = Campo
        try:
            btn_proximo = expect(page.get_by_role("link", name=nome_campos).click(timeout=100)).to_be_visible()
            print("botao nao localizado")
        except Exception as error:
            print(error)
            print(f'Estado não possui mais municipios')

    lista_UF = []
    Lista_faixa_UF_CEP = []
    lista_localidade = []
    lista_faixa_cep = []
    lista_situacao = []
    lista_tipo_faixa =[]

    index = 0
    qtde_linhas = linhas.count() - 2

    while index <= qtde_linhas:
        coluna_localidade = linhas.locator('//td[1]')
        coluna_localidade = coluna_localidade.nth(index).inner_text()
        lista_localidade.append(coluna_localidade)

        coluna_faixa_cep = linhas.locator('//td[2]')
        coluna_faixa_cep = coluna_faixa_cep.nth(index).inner_text()
        lista_faixa_cep.append(coluna_faixa_cep)

        coluna_situacao = linhas.locator('//td[3]')
        coluna_situacao = coluna_situacao.nth(index).inner_text()
        lista_situacao.append(coluna_situacao)

        coluna_tipo_faixa = linhas.locator('//td[4]')
        coluna_tipo_faixa = coluna_tipo_faixa.nth(index).inner_text()
        lista_tipo_faixa.append(coluna_tipo_faixa)

        lista_UF.append(linha_campo_uf_cep)
        Lista_faixa_UF_CEP.append(linha_campo_faixa_cep)


        index += 1
        print(
            f'{index} - '
            f'Cidade: {coluna_localidade}, '
            f'Faixa: {coluna_faixa_cep}, '
            f'Situação: {coluna_situacao}, '
            f'Tipo de Faixa: {coluna_tipo_faixa}'
              )



    #print(div1.text_content())
    current_timestamp = datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
    print('-----Fim-----')
    page.screenshot(path='result_'+current_timestamp+'.png', full_page=True)

    sleep(1)

    clickproximo('Próximo')

    browser.close()