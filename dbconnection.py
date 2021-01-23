import psycopg2

class Conexion: 

    def __init__(self, host=None, service=None, user=None, passwd=None):
        self.host = host        
        self.service = service
        self.user = user
        self.passwd = passwd        


    def execute_statement(self, statement):
        mydb = self.connect()
        mycursor = mydb.cursor()
        mycursor.execute(statement)
        mydb.commit()


    def connect(self):  
        mydb = psycopg2.connect(
                host="161.35.60.197",
                database="tcs7",
                user="modulo4",
                password="modulo4")   
        print(mydb)    
        print("Conexion Exitosa")   
        return mydb
    

    def execute_web_scrapping(self,pagina_web,url_pagina,url_busqueda):
        mydb=self.connect()
        cursor = mydb.cursor()
        sql = "insert into webscraping (busqueda, busqueda_area, pagina_web, url_pagina, url_busqueda,fecha_creacion,fecha_modificacion, id_keyword) values (null,null,%s,%s,%s,current_date,current_date, %s)"
        params = (pagina_web, url_pagina,url_busqueda,11)
        cursor.execute(sql,params)
        mydb.commit()
        cursor.close()
        mydb.close()

    def execute_oferta(self,titulo_oferta,lugar_oferta,salario_oferta,url_oferta,url_pagina,oferta_detalle,descripcion):
        mydb=self.connect()
        cursor = mydb.cursor()
        cursor.callproc('insert_prue',[titulo_oferta,lugar_oferta,salario_oferta,url_oferta,url_pagina,oferta_detalle,descripcion])
        mydb.commit()
        cursor.close()
        mydb.close()
        print("Insercion Exitosa")