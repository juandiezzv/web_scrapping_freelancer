
from dbconnection import Conexion

import pandas as pd

def connect_bd():
    con = Conexion("161.35.60.197",
    "tcs7",
    "modulo4",
    "modulo4")
    con.connect()
    return con

def cortarString(s,n):    
      return s[n:]

def cortarStringDel(s,n):
      return s[:n]


conexion = connect_bd()



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