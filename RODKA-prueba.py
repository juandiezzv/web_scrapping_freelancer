#Se debe instalar las siguientes librerias "Selenium", "Pandas" y "BeautifulSoup", "pip", "numpy", "openpyxl" 

#pip install selenium --user
from selenium import webdriver
#pip install pandas --user
import pandas as pd
#pip install bs4 --user
from bs4 import BeautifulSoup

from time import sleep
from time import time
start_time = time()

titulos = []
descripciones = []
precios = []
tags = []
tiempoRestante = []


#funcion para cortar el string

def cortarString(s,n):    
      return s[n:]

def cortarStringDel(s,n):
      return s[:n]

#La url con los filtros ya seleccionados
""" url= "https://www.freelancer.com.pe/jobs/?keyword=Analista%20programador&languages=es&fixed=true&fixed_min=100&fixed_max=5000&sort=budget_max" """
url= "https://www.freelancer.com.pe/jobs/?keyword=dise%C3%B1o%20web"

#Se debe descargar chromedriver desde la siguiente url: "https://sites.google.com/a/chromium.org/chromedriver/downloads"
driver = webdriver.Chrome(executable_path=r"C:\chromedriver.exe")

dataframe = pd.DataFrame(columns=["Titulo","Descripcion","Precio","Tags","Tiempo Restantes"])

driver.get(url)

trabajos = driver.find_elements_by_class_name('JobSearchCard-item-inner')

for trabajo in trabajos:

    result_html = trabajo.get_attribute('innerHTML')
    soup = BeautifulSoup(result_html,'html.parser')

    try: 
        tituloSM = soup.find("a",class_="JobSearchCard-primary-heading-link").text.replace('\n','')
        titulo = cortarString(tituloSM,32)
    except:
        tituloSM = 'No hay titulo'

    try:
        descripcionSM = soup.find("p",class_="JobSearchCard-primary-description").text.replace('\n','')
        descripcion = cortarString(descripcionSM,92)
    except:
        descripcion = "Sin Descripción"   
    
    try:
        precioSM = soup.find("div",class_="JobSearchCard-secondary-price").text.replace('\n','')
        precioCM = cortarString(precioSM,61)
        precio = cortarStringDel(precioCM,50)
        
    except:
        precio = "Sin precio"   
    
    try: 
        tag = soup.find("div",class_="JobSearchCard-primary-tags").text.replace(' ','|')
    except:
        tag = "No hay Tags"    
    
    try:
        tiempoFaltante = soup.find("span",class_="JobSearchCard-primary-heading-days").text.replace('\n','')
    except:
        tiempoFaltante = "No hay información"
    
    dataframe = dataframe.append({'Titulo':titulo,'Descripcion':descripcion,'Precio':precio,'Tags':tag,'TiempoRestantes':tiempoFaltante},ignore_index=True)

driver.close()


dataframe.to_csv("C:/Pruebas/freelancer.csv",index=False)

sleep(2)

read_file = pd.read_csv(r'C:/Pruebas/freelancer.csv')
read_file.to_excel(r'C:/Pruebas/freelancerexcel.xlsx', index = None, header=True)

sleep(5)
""" LEEMOS EL ARCHIVO EXCEL """
df = pd.read_excel('C:/Pruebas/freelancerexcel.xlsx',sheet_name='Sheet1')


""" PASAMOS A ARREGLOS """
titulos=df.Titulo
descripciones=df.Descripcion
precios=df.Precio
tags=df.Tags
tiempoRestante=df.TiempoRestantes

i=1
for title in titulos:
    print(i, title)
    i=i+1
"""
i=1
for desc in descripciones:
    print(i, desc)
    i=i+1

i=1
for price in precios:
    print(i, price)
    i=i+1

i=1
for tag in tags:
    print(i, tag)
    i=i+1

i=1
for time in tiempoRestante:
    print(i, time)
    i=i+1"""
