#!/usr/bin/env python
# coding: utf-8

# # Trabalho Prático 02

# Tarefa01

# In[61]:


import requests
from bs4 import BeautifulSoup
import pandas as pd

headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0 "}

url = 'https://www.ubi.pt/Pagina/Faculdades'
page = requests.get(url, headers=headers)

soup = BeautifulSoup(page.content, 'html.parser')


Nome_faculdade = 'ConteudoHolder_LV_Paginas_Display_Blocos_0_Repeater_Pagina_0_LV_BLOCOS_DA_PAGINA_0_TituloURLLabel_'
descricao = 'ConteudoHolder_LV_Paginas_Display_Blocos_0_Repeater_Pagina_0_LV_BLOCOS_DA_PAGINA_0_TextoLabel_'
#Ver a olho humano o numero de faculdades da pagina
num_faculdades = 5 

# Nao funcionou

#ListOfTagContents = soup.select("span.blkTexto col-xs-12 col-sm-7 row")
#print(ListOfTagContents)
faculdades = []
titulos_faculdades = []
descricao_faculdade = []

base_link = "https://www.ubi.pt"
pd.set_option('display.max_colwidth', None)

links = [] 

# recolher o nome de cada faculdade
for i in range(0,num_faculdades): 
    titulos_faculdades = soup.find(id="ConteudoHolder_LV_Paginas_Display_Blocos_0_Repeater_Pagina_0_LV_BLOCOS_DA_PAGINA_0_TituloURLLabel_"+ str(i)).get_text().strip()
    descricao_auxiliar = soup.find(id="ConteudoHolder_LV_Paginas_Display_Blocos_0_Repeater_Pagina_0_LV_BLOCOS_DA_PAGINA_0_TextoLabel_"+ str(i))
    descricao_faculdade = descricao_auxiliar.find('p').get_text()
    listas_links = descricao_auxiliar.find_all('ul')
    for lista in listas_links:
         links.extend([base_link + a['href'] for a in lista.find_all('a', href=True)])
    links_str = ', '.join(links)    
    faculdades.append({'Nome Da Faculdade': titulos_faculdades,"Descrição":descricao_faculdade,'Links':links_str})
    links = [] 
    # Imagem não pode ser mostrada porque não existe link associado a esta

df = pd.DataFrame(faculdades)
df


# # Tarefa 02

# In[13]:


# Função usada para determinar a classe da notícia
def par_impar(num):
    if num % 2 == 0:
        return "even"
    else:
        return "odd"


# In[14]:


def CustomizeDataframe(df):
    def make_visible_img(url):
        if url is None or url == '':
            return 'Imagem não disponível'
        else:
            return f'<img src="{url}" style="max-height:124px;"></img>'

    def make_clickable_link(url, title):
        if url is None or url == '':
            return title
        else:
            return f'<a target="_blank" href="{url}">{title}</a>'

    df['Img'] = df.apply(lambda x: make_visible_img(x['Img']), axis=1)
    df['Título'] = df.apply(lambda x: make_clickable_link(x['news_url'], x['Título']), axis=1)

    return df


# In[ ]:


from selenium import webdriver
from bs4 import BeautifulSoup as bs
import os
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
from datetime import datetime
from IPython.display import HTML
import logging
import json


# accessing Chromedriver
options = webdriver.ChromeOptions()
options.add_argument("--disable-infobars")
options.add_argument("start-maximized")
options.add_argument("--disable-extensions")

# Pass the argument 1 to allow and 2 to block
options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications": 1
})

#credenciais para iniciar sessão na sic_noticias
credenciais = "pass.txt"

with open(credenciais, 'r') as arquivo:
    email_input = arquivo.readline().strip()
    pass_input = arquivo.readline().strip()

for i in range(0,48):
    
    browser = webdriver.Chrome()
    browser.get("https://sicnoticias.pt") # Abriu o link 

    cookies = browser.find_element(By.XPATH, '//button[@id="didomi-notice-agree-button"]')# clicar no "aceitar" do cookie 
    cookies.click() 

    butao = browser.find_element(By.XPATH, '//body[@id="body"]/div[@id="root"]/header[@class="main-header"]/div[@class="main-header-inner"]/div[@class="elements-wrapper header-wrapper"]/div[@class="elements-wrapper header-top-wrapper"]/div[@class="user-alert-wrapper container container-2 container-2-2 container-even container-last"]/span/button[1]')
    butao.click()

    iniciar_sessao = browser.find_element(By.XPATH, '//div[@class="g-toggle-menu-container"]//aside[@class="sidebar sidebar-splitter right-sidebar"]//div[@class="sidebar-inner"]//div[@class="perfil-wrapper container container-unique"]//div[@class="sessao-subscrever-wrapper container container-2 container-2-3 container-even"]//div[@class="sessao-perfil-wrapper container container-unique"]//div[@class="user-login-wrapper container container-2 container-2-2 container-even container-last"]//button[@class="g-button common-button bt-login"]')
    iniciar_sessao.click()

    email = browser.find_element(By.XPATH, '//input[@id="pass-confirm-form_1"]')
    palavra_passe = browser.find_element(By.XPATH, '//input[@id="pass-confirm-form_2"]')

    email.send_keys(email_input)
    palavra_passe.send_keys(pass_input)

    btn_entrar = browser.find_element(By.XPATH, '//button[contains(text(),"Entrar")]')
    btn_entrar.click()

    time.sleep(30)

    # Se tentar clicar no butao "Ver Mais" vai me dar problemas porque o seu XPATH
    # muda consoate o tamanho da tela
    #btn_ver_mais = browser.find_element(By.XPATH, '//div[@class="list-wrapper latest-scrollable dynamic-height-element"]//div[@class="list-footer"]//a[@class="follow-link follow-link--button"]')
    #btn_ver_mais.click()

    butao_notificacao_mais_tarde = browser.find_element(By.XPATH,'//*[@id="onesignal-slidedown-cancel-button"]')
    butao_notificacao_mais_tarde.click()


    btn_ver_mais = browser.find_element(By.XPATH, '//*[@id="root"]/main/section[6]/div/div/div/div[2]/div[1]/a')
    actions = ActionChains(browser)
    actions.move_to_element(btn_ver_mais).perform()
    time.sleep(10)
    btn_ver_mais.click()

    source_data = browser.page_source
    bs_data = bs(source_data, 'html.parser')

    conteiner = bs_data.find('ul', class_='list-articles item-count-12 latest latest--boxed latest--horizontal latest--aggregator')
    
    # Até Aqui o web scraping faz login na pagina da sc_noticias 
    # Espera 30 segundo para aparecer o pop-up
    # Cancela o Pop-up
    # Arrasta a tela até ao butão "Ver Mais"
    # Clica no Botão "Ver Mais"
    
    ###########################################################################################
    
    # Percorre todas as notícas presentes na página
    # Guarda num ficheiro JSON cada noticia 
    # É usado um ficheiro log para controlar o fluxo de execução 
    
    noticias = []
    for i in range(1,13):
        try:
            item = par_impar(i)
            # aceder aos 12 destaques de noticias apresentados
            li_noticias = conteiner.find('li', class_="item-"+str(i)+" item-"+item)
            descricao = ''
            categoria = li_noticias.find('p', class_="category").get_text()
            mes_ano = li_noticias.find('p', class_="time-stamp").get_text()
            if "Há" in mes_ano:
                mes_ano = datetime.now().strftime("%d/%m")

            title_url = li_noticias.find('h2', class_="title")
            title = title_url.get_text().strip()

            new_url = title_url.find('a', href=True).get('href')

            descricao = li_noticias.find('p', class_="lead").get_text() if li_noticias.find('p', class_="lead") else ''

            news_url = title_url.find('a', href=True).get('href')
            link = "https://sicnoticias.pt"
            if link not in news_url:
                news_url = link + news_url
            try:
                img_tag = li_noticias.find('picture', class_="landscape").find('img')
                if not img_tag:  
                    img_tag = li_noticias.find('img')  
                desired_img_url = img_tag['src'] if img_tag else None
            except AttributeError:
                desired_img_url = None

            noticias.append({
                'Notícia': 'Sic Noticias',
                'categoria': categoria,
                'Título': title,
                'Descrição': descricao,
                'Mes_Ano': mes_ano,
                'Img': desired_img_url,
                'news_url': news_url,
                'real_time': datetime.now().isoformat()
            })
        except Exception as e:
            logging.warning(f"Erro ao processar notícia: {e}")
        
    with open('noticias.json', 'a') as arquivo:
        json.dump(noticias, arquivo, ensure_ascii=False, indent=4)
        
    logging.basicConfig(level=logging.INFO, filename="logs.log", filemode="a", 
                    format="%(asctime)s; Line:%(lineno)s; %(levelname)s: %(message)s",
                    datefmt="%d-%b-%Y %H:%M")
    logging.warning("12 Ultimas noticias guardadas com sucesso!")

    ###########################################################################################
    
    # É mostrado na tela um display acerca da notícia com imagem, link e outras informações.

    df = pd.DataFrame(noticias)
    df = CustomizeDataframe(df)
    df.drop('news_url', axis=1, inplace=True)
    df.drop('real_time', axis=1, inplace=True)
    df_html = df.to_html(escape=False)  
    display(HTML(df_html))
    time.sleep(3600)

