#Se debe instalar las siguientes librerias "Selenium", "Pandas" y "BeautifulSoup", "pip", "numpy", "openpyxl" 

#pip install selenium --user
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
#pip install pandas --user
import pandas as pd
#pip install bs4 --user
from bs4 import BeautifulSoup
from dbconnection import Conexion

from time import sleep
from time import time
start_time = time()

titulos = []
descripciones = []
precios = []
tiemposRestante = []

Pagina_Webs = []
Url_Busquedas = []
Url_Paginas  = []
Lugares = []
Url_Pagina_Ofertas = []


pagina_web ="Freelancer"



#funcion para cortar el string

def cortarString(s,n):    
      return s[n:]

def cortarStringDel(s,n):
      return s[:n]

def connect_bd():
    con = Conexion("161.35.60.197",
    "tcs7",
    "modulo4",
    "modulo4")
    con.connect()
    return con





#La url con los filtros ya seleccionados
#""" url= "https://www.freelancer.com.pe/jobs/?keyword=Analista%20programador&languages=es&fixed=true&fixed_min=100&fixed_max=5000&sort=budget_max" """
#url= "https://www.freelancer.com.pe/jobs/?keyword=dise%C3%B1o%20web"

#Se debe descargar chromedriver desde la siguiente url: "https://sites.google.com/a/chromium.org/chromedriver/downloads"
driver = webdriver.Chrome(executable_path=r"C:\chromedriver.exe")

dataframe = pd.DataFrame(columns=["Pagina_Web","Url_Pagina","Url_Busqueda","Lugar","Titulo","Descripcion","Precio","Url_Pagina_Oferta","Tiempo_Restantes"])
       #https://www.freelancer.com.pe/jobs/?keyword=INGENIERO%20DE%20SISTEMAS

##PAGINA
for i in range(1,12,1):
    

    url_pagina = 'https://www.freelancer.com.pe/'
    url_busqueda = url_pagina + 'jobs/'+str(i)+'/?keyword=INGENIERO%20DE%20SISTEMAS'
    #url_busqueda = url_pagina + 'jobs/'+str(1)+'/?keyword=docente&results=20'

    driver.get(url_busqueda)

    trabajos = driver.find_elements_by_class_name('JobSearchCard-item-inner')

    for trabajo in trabajos:

        detalle_oferta = ""
        lugar_oferta = ""

        result_html = trabajo.get_attribute('innerHTML')
        soup = BeautifulSoup(result_html,'html.parser')

        try: 
            tituloSM = soup.find("a",class_="JobSearchCard-primary-heading-link").text.replace('\n','')
            titulo = cortarString(tituloSM,32)
        except:
            tituloSM = 'No hay titulo'

        try:
            precioSM = soup.find("div",class_="JobSearchCard-secondary-price").text.replace('\n','')
            precioCM = cortarString(precioSM,61)
            precio = cortarStringDel(precioCM,50)
            precio = precio.strip()
            
        except:
            precio = "Sin precio"   
        
        #try: 
        #    tag = soup.find("div",class_="JobSearchCard-primary-tags").text.replace(' ','|')
        #except:
        #    tag = "No hay Tags"    
        
        try:
            tiempoFaltante = soup.find("span",class_="JobSearchCard-primary-heading-days").text.replace('\n','')
        except:
            tiempoFaltante = "No hay información"


        titulo_limpio = tituloSM.strip()
        link =  driver.find_elements_by_partial_link_text(titulo_limpio)
    
        if len(link) == 0  :
            print("No se encontro")
        else : 
            link[0].send_keys(Keys.CONTROL + Keys.RETURN)
            driver.switch_to.window(driver.window_handles[1])
            

            url_pagina_oferta = driver.current_url

            ofertas_detalle = driver.find_elements_by_class_name('PageProjectViewLogout-detail')

            for oferta in ofertas_detalle: 
                

                result_html_oferta = oferta.get_attribute('innerHTML')
                soup_oferta = BeautifulSoup(result_html_oferta,'html.parser')
                
                try:
                    lugar_sucio = soup_oferta.find_all("span",class_="PageProjectViewLogout-detail-reputation-item-locationItem")
                    lugar_oferta = lugar_sucio[1].text.strip()
                    if len(lugar_oferta) == 0 :
                        lugar_oferta = "No detallado"
                    
                    if type(lugar_oferta) == float: 
                        lugar_oferta = "No detallado"
                    

                except: 
                    lugar_oferta = "No detallado"


                try: 
                    descripcion_oferta = soup_oferta.find_all("p",class_="")
                    
                    for oferta in descripcion_oferta:
                        oferta_limpia = str(oferta)
                        oferta_mas_limpia = oferta_limpia.replace('<p>','')
                        oferta_mas_limpia = oferta_mas_limpia.replace('</p>','')
                        
                        detalle_oferta = detalle_oferta + oferta_mas_limpia
                    
                    if len(detalle_oferta) == 0:
                        detalle_oferta = "No detallado"
                    
                    if len(detalle_oferta) > 1990:
                        detalle_oferta = cortarStringDel(detalle_oferta,1990)

                    if type(detalle_oferta) == float: 
                        detalle_oferta = "No detallado"


                except:
                        detalle_oferta = "No detallado"

            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        

        dataframe = dataframe.append({"Pagina_Web":pagina_web,"Url_Pagina":url_pagina, "Url_Busqueda": url_busqueda,"Lugar":lugar_oferta, 'Titulo':titulo,'Descripcion':detalle_oferta,'Precio':precio,"Url_Pagina_Oferta":url_pagina_oferta,'Tiempo_Restantes':tiempoFaltante},ignore_index=True)
        print(dataframe)

driver.close()

dataframe.to_csv("C:/Pruebas/freelancer.csv",index=False)

sleep(2)

read_file = pd.read_csv(r'C:/Pruebas/freelancer.csv')
read_file.to_excel(r'C:/Pruebas/freelancerexcel.xlsx', index = None, header=True)




df = pd.read_excel('C:/Pruebas/freelancerexcel.xlsx',sheet_name='Sheet1')

""" PASAMOS A ARREGLOS """
titulos=df.Titulo
descripciones=df.Descripcion
precios=df.Precio
tiemposRestantes=df.Tiempo_Restantes


Pagina_Webs = df.Pagina_Web
Url_Busquedas = df.Url_Busqueda
Url_Paginas  = df.Url_Pagina
Lugares = df.Lugar
Url_Pagina_Ofertas = df.Url_Pagina_Oferta

pagina_web = Pagina_Webs[0]
url_pagina = Url_Paginas[0]
url_busqueda = Url_Busquedas[0]

#conexion.execute_web_scrapping(pagina_web,url_pagina,url_busqueda)

conexion = connect_bd()

print(len(titulos))
print(len(descripciones))
print(len(precios))
print(len(tiemposRestantes))
print(len(Pagina_Webs))
print(len(Url_Busquedas))
print(len(Url_Paginas))
print(len(Lugares))
print(len(Url_Pagina_Ofertas))

numeroOfertas = len(titulos)

conexion.execute_web_scrapping(pagina_web,url_pagina,url_busqueda)



for j in range(1,numeroOfertas,1):
    
    if type(descripciones[j]) == float: 
        descripciones[j] = "No detallado"  
    elif len(descripciones[j]) > 1990:
        descripciones[j] = cortarStringDel(descripciones[j],1990)

    if type(Lugares[j]) == float: 
        Lugares[j] = "No detallado"  
    elif len(Lugares[j]) > 1990:
        Lugares[j] = cortarStringDel(Lugares[j],1990)

    conexion.execute_oferta(titulos[j],Lugares[j],precios[j],Url_Pagina_Ofertas[j],Url_Busquedas[j],descripciones[j],descripciones[j])
    print("Se inserto Registro")