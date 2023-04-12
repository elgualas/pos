import mysql.connector

class Comunicacion():
    def __init__(self):
        self.conexion=mysql.connector.connect(host='database-2.cqvkjdbtsdxm.us-east-2.rds.amazonaws.com',
                                              database='prueba',
                                              user='gualas',
                                              password='Chrono69+')
    
    def inserta_producto(self ,codigo ,nombre, modelo, precio, cantidad):
        cursor=self.conexion.cursor()
        bd='''INSERT INTO tabla_datos (CODIGO, NOMBRE, MODELO, PRECIO, CANTIDAD)
        VALUES('{}','{}','{}','{}','{}')'''.format(codigo ,nombre, modelo, precio, cantidad)
        cursor.execute(bd)
        self.conexion.commit()
        cursor.close()

    def mostrar_items(self):
        cursor=self.conexion.cursor()
        bd='''select it.IdItem, mar.Nombre as Marca, it.Familia, it.Descripcion, it.Unidad_Med,pre.Precio_Venta,pre.Precio_Minimo 
            FROM items it 
            Join marca mar On(it.IdMarca=mar.IdMarca)
            Join precio pre On(it.IdItem=pre.IdItem);'''
        cursor.execute(bd)
        registro=cursor.fetchall()
        return registro
    
    def mostrar_clientes(self):
        cursor=self.conexion.cursor()
        bd='''SELECT * FROM clientes'''
        cursor.execute(bd)
        registro=cursor.fetchall()
        return registro

    def buscar_producto(self,nombre_producto):
        cursor=self.conexion.cursor()
        bd='''SELECT * FROM tabla_datos WHERE NOMBRE={}'''.format(nombre_producto)
        cursor.execute(bd)
        nombreX=cursor.fetchall()
        cursor.close()
        return nombreX

    def elimina_producto(self,nombre):
        cursor=self.conexion.cursor()
        bd='''DELETE FROM tabla_datos WHERE NOMBRE={}'''.format(nombre)
        cursor.execute(bd)
        nombreX=cursor.fetchall()
        cursor.close()
        

    def actualizar_producto(self ,Id ,codigo ,nombre, modelo, precio, cantidad):
        cursor=self.conexion.cursor()
        bd='''UPDATE tabla_datos SET CODIGO='{}', NOMBRE='{}', MODELO='{}', PRECIO='{}', CANTIDAD='{}'
        WHERE ID='{}' '''.format(codigo ,nombre, modelo, precio, cantidad,Id)
        cursor.execute(bd)
        a = cursor.rowcount
        self.conexion.commit()
        cursor.close()
        return a
    
    def buscar_usuario(self,users,password):
        cur=self.conexion.cursor()
        sql='''SELECT * FROM login_datos WHERE Users = %s and Password = %s '''
        cur.execute(sql,(users,password))
        usersx=cur.fetchall()
        cur.close()
        return usersx
    
    def buscar_cliente(self,nombre):
        cur=self.conexion.cursor()
        sql='''SELECT * FROM clientes WHERE Razon_Social LIKE '%{}%' or Num_Doc LIKE '%{}%';  '''.format(nombre,nombre)
        cur.execute(sql)
        usersx=cur.fetchall()
        cur.close()
        return usersx
    
    def buscar_item(self,nombre):
        cur=self.conexion.cursor()
        sql='''select it.IdItem, mar.Nombre as Marca, it.Familia, it.Descripcion, it.Unidad_Med,pre.Precio_Venta,pre.Precio_Minimo 
            FROM items it 
            JOIN marca mar ON(it.IdMarca=mar.IdMarca)
            JOIN precio pre ON(it.IdItem=pre.IdItem) WHERE it.IdItem like '%{}%' or it.Descripcion like '%{}%';'''.format(nombre,nombre)
        cur.execute(sql)
        usersx=cur.fetchall()
        cur.close()
        return usersx

