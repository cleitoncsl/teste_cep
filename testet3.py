import os
import pandas as pd
from time import sleep
from playwright.sync_api import expect, sync_playwright
from datetime import datetime

url = 'https://buscacepinter.correios.com.br/app/faixa_cep_uf_localidade/index.php'
path = os.path.dirname(r'C:\Users\cleit\OneDrive\Documentos\TRABALHO\Alvorada\PYTHON\teste_cep\csv\\')

ufs = ['AC', 'AL', 'AM']
#ufs = ['AC']

def GetData(rows, UF, FaixaCEP, page):
    linha_campo_uf_cep = UF
    linha_campo_faixa_cep = FaixaCEP

    index = 0
    qtde_linhas = rows.count() - 2

    lista_UF = []
    Lista_faixa_UF_CEP = []
    lista_localidade = []
    lista_faixa_cep = []
    lista_situacao = []
    lista_tipo_faixa = []

    while index <= qtde_linhas:
        coluna_localidade = rows.locator('//td[1]')
        coluna_localidade = coluna_localidade.nth(index).inner_text()
        lista_localidade.append(coluna_localidade)

        coluna_faixa_cep = rows.locator('//td[2]')
        coluna_faixa_cep = coluna_faixa_cep.nth(index).inner_text()
        lista_faixa_cep.append(coluna_faixa_cep)

        coluna_situacao = rows.locator('//td[3]')
        coluna_situacao = coluna_situacao.nth(index).inner_text()
        lista_situacao.append(coluna_situacao)

        coluna_tipo_faixa = rows.locator('//td[4]')
        coluna_tipo_faixa = coluna_tipo_faixa.nth(index).inner_text()
        lista_tipo_faixa.append(coluna_tipo_faixa)

        lista_UF.append(linha_campo_uf_cep)
        Lista_faixa_UF_CEP.append(linha_campo_faixa_cep)

        index += 1
        print(
            f'{index} - '
            f'UF: {UF}, '
            f'Cidade: {coluna_localidade}, '
            f'Faixa: {coluna_faixa_cep}, '
            f'Situação: {coluna_situacao}, '
            f'Tipo de Faixa: {coluna_tipo_faixa}'
        )

        # print(div1.text_content())
    current_timestamp = datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
    print('-----Fim-----')
    page.screenshot(path='result_' + current_timestamp + '.png', full_page=True)

    ClickNext('Próximo', rows, UF, FaixaCEP, page)
    SaveFile(lista_UF, lista_localidade, lista_situacao, lista_tipo_faixa, lista_faixa_cep, Lista_faixa_UF_CEP, index)

def SaveFile(lista_UF, lista_localidade, lista_situacao, lista_tipo_faixa, lista_faixa_cep, Lista_faixa_UF_CEP, index):

    df = pd.DataFrame()
    df['UF'] = lista_UF
    df['Faixa de CEP'] = Lista_faixa_UF_CEP
    df['Localidade'] = lista_localidade
    df['Faixa de CEP'] = lista_faixa_cep
    df['Situação'] = lista_situacao
    df['Tipo de Faixa'] = lista_tipo_faixa

    data_frame = df
    print(df)

    arquivo = os.path.join(path, 'arquivo.xlsx')
    with pd.ExcelWriter(arquivo,
                        engine="xlsxwriter") as writer:
        data_frame.to_excel(writer)


def SelecionarUF(UF, page):
    estado = UF
    page.get_by_role("combobox", name="UF:*").select_option(estado)
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

    GetData(linhas, linha_campo_uf_cep, linha_campo_faixa_cep, page)


def ClickNext(Campo, rows, UF, FaixaCEP, page):

    nome_campos = Campo

    try:
        btn_prox = False
        btn_proximo = page.get_by_role("link", name=nome_campos)
        check = len(btn_proximo.text_content(timeout=100))

        if page.get_by_role("link", name=nome_campos) != None:
            page.get_by_role("link", name=nome_campos).click(timeout=100)

            sleep(0.4)

            btn_prox = True
            print("proxima pagina")
            CheckStatus(btn_prox, rows, UF, FaixaCEP)

    # except Exception as error:

    except:
        btn_prox = False
        # print(error)
        # print(f'Estado não possui mais municipios')

        # testando#
        # CheckStatus(False, rows, UF, FaixaCEP)

        print(f'Estado não possui mais municipios')
        print(f'Próximo Estado')
        # page.get_by_role("button", name="Nova Busca").click()

        # testando"
        # CheckStatus(False, rows, UF, FaixaCEP)


def CheckStatus(status, rows, UF, FaixaCEP):
    if status == True:
        GetData(rows, UF, FaixaCEP)

    else:
        return False

        sleep(0.4)

        page.get_by_role("button", name="Nova Busca").click()
        pass


def AbrirSite():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(
                color_scheme='dark'
            )
            page = context.new_page()
            page.goto(url)
            sleep(0.2)
            for i in ufs:
                print(f'Filial {i}')
                SelecionarUF(i, page)
                sleep(0.4)
                page.get_by_role("button", name="Nova Busca").click()
                print(f'Fim')


    except Exception as error:
        print(error)
        print(f'erro -> {error}')


if __name__ == "__main__":

    AbrirSite()

