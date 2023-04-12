import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView
from PyQt5.QtCore import QPropertyAnimation,QEasingCurve
from PyQt5 import QtCore,QtWidgets
from PyQt5.uic import loadUi
from conexion import Comunicacion

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super(VentanaPrincipal,self).__init__()
        loadUi('interfaz_ventas.ui',self)

        self.bt_menu.clicked.connect(self.mover_menu)
        self.base_datos=Comunicacion()

        self.bt_restaurar.hide()

        self.bt_refrescar.clicked.connect(self.mostrar_items)
        self.bt_agregar.clicked.connect(self.registrar_productos)
        self.bt_borrar.clicked.connect(self.eliminar_productos)
        self.bt_actualiza_tabla.clicked.connect(self.modificar_productos)
        self.bt_actualiza_buscar.clicked.connect(self.buscar_por_nombre_actualiza)
        self.bt_buscar_borrar.clicked.connect(self.buscar_por_nombre_eliminar)
        self.bt_refrescar_clientes.clicked.connect(self.mostrar_clientes)
        self.bt_buscar_cliente.clicked.connect(self.mostrar_clientes_buscados)
        self.bt_buscar_item.clicked.connect(self.mostrar_items_buscados)
        
        self.bt_minimizar.clicked.connect(self.control_bt_minimizar)
        self.bt_restaurar.clicked.connect(self.control_bt_normal)
        self.bt_maximizar.clicked.connect(self.control_bt_maximizar)
        self.bt_cerrar.clicked.connect(lambda: self.close())

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)

        self.gripSize=10
        self.grip=QtWidgets.QSizeGrip(self)
        self.grip.resize(self.gripSize,self.gripSize)

        self.frame_superior.mouseMoveEvent=self.mover_ventana

        self.bt_datos.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_datos))
        self.bt_registrar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_registrar))
        self.bt_actualizar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_actualizar))
        self.bt_eliminar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_eliminar))
        self.bt_clientes.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_clientes))

        self.tabla_borrar.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla_productos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla_clientes.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def control_bt_minimizar(self):
            self.showMinimized()

    def control_bt_normal(self):
            self.showNormal()
            self.bt_restaurar.hide()
            self.bt_maximizar.show()
        
    def control_bt_maximizar(self):
            self.showMaximized()
            self.bt_maximizar.hide()
            self.bt_restaurar.show()

    def resizeEvent(self, event):
            rect=self.rect()
            self.grip.move(rect.right()-self.gripSize, rect.bottom()- self.gripSize)

    def mousePressEvent(self, event):
            self.click_position=event.globalPos()

    def mover_ventana(self, event):
            if self.isMaximized()==False:
                if event.buttons()==QtCore.Qt.LeftButton:
                    self.move(self.pos() + event.globalPos()- self.click_position)
                    self.click_position=event.globalPos()
                    event.accept()
            if event.globalPos().y()<=10:
                self.showMaximized()
                self.bt_maximizar.hide()
                self.bt_restaurar.show()
            else:
                self.showNormal()
                self.bt_restaurar.hide()
                self.bt_maximizar.show()
        
    def mover_menu(self):
            if True:
                width=self.frame_control.width()
                normal=0
                if width==0:
                    extender=200
                else:
                    extender=normal
                self.animacion=QPropertyAnimation(self.frame_control, b'minimumWidth')
                self.animacion.setDuration(300)
                self.animacion.setStartValue(width)
                self.animacion.setEndValue(extender)
                self.animacion.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
                self.animacion.start()
                
    def mostrar_items(self):
            datos=self.base_datos.mostrar_items()
            i=len(datos)
            self.tabla_productos.setRowCount(i)
            tablerow=0
            for row in datos:
                self.Id=row[0]
                self.tabla_productos.setItem(tablerow,0,QtWidgets.QTableWidgetItem(row[0]))
                self.tabla_productos.setItem(tablerow,1,QtWidgets.QTableWidgetItem(row[1]))
                self.tabla_productos.setItem(tablerow,2,QtWidgets.QTableWidgetItem(row[2]))
                self.tabla_productos.setItem(tablerow,3,QtWidgets.QTableWidgetItem(row[3]))
                self.tabla_productos.setItem(tablerow,4,QtWidgets.QTableWidgetItem(row[4]))
                self.tabla_productos.setItem(tablerow,5,QtWidgets.QTableWidgetItem(row[5]))
                self.tabla_productos.setItem(tablerow,6,QtWidgets.QTableWidgetItem(row[6]))
                tablerow +=1
                self.signal_actualizar.setText("")
                self.signal_registrar.setText("")
                self.signal_eliminacion.setText("")

    def mostrar_clientes(self):
            datos=self.base_datos.mostrar_clientes()
            i=len(datos)
            self.tabla_clientes.setRowCount(i)
            tablerow=0
            for row in datos:
                self.Id=row[0]
                self.tabla_clientes.setItem(tablerow,0,QtWidgets.QTableWidgetItem(row[0]))
                self.tabla_clientes.setItem(tablerow,1,QtWidgets.QTableWidgetItem(row[1]))
                self.tabla_clientes.setItem(tablerow,2,QtWidgets.QTableWidgetItem(row[2]))
                self.tabla_clientes.setItem(tablerow,3,QtWidgets.QTableWidgetItem(row[3]))
                self.tabla_clientes.setItem(tablerow,4,QtWidgets.QTableWidgetItem(row[4]))
                self.tabla_clientes.setItem(tablerow,5,QtWidgets.QTableWidgetItem(row[5]))
                self.tabla_clientes.setItem(tablerow,6,QtWidgets.QTableWidgetItem(row[6]))
                tablerow +=1

    def mostrar_clientes_buscados(self):
            id_cliente=self.clientes_buscar.text().upper()
            id_cliente=str(id_cliente)
            datos=self.base_datos.buscar_cliente(id_cliente)
            if len(datos)!=0:
                i=len(datos)
                self.tabla_clientes.setRowCount(i)
                tablerow=0
                for row in datos:
                    self.Id=row[0]
                    self.tabla_clientes.setItem(tablerow,0,QtWidgets.QTableWidgetItem(row[0]))
                    self.tabla_clientes.setItem(tablerow,1,QtWidgets.QTableWidgetItem(row[1]))
                    self.tabla_clientes.setItem(tablerow,2,QtWidgets.QTableWidgetItem(row[2]))
                    self.tabla_clientes.setItem(tablerow,3,QtWidgets.QTableWidgetItem(row[3]))
                    self.tabla_clientes.setItem(tablerow,4,QtWidgets.QTableWidgetItem(row[4]))
                    self.tabla_clientes.setItem(tablerow,5,QtWidgets.QTableWidgetItem(row[5]))
                    self.tabla_clientes.setItem(tablerow,6,QtWidgets.QTableWidgetItem(row[6]))
                    tablerow +=1
            else:
                self.clientes_buscar.setText('NoExiste')

    def mostrar_items_buscados(self):
            id_cliente=self.line_buscar.text().upper()
            id_cliente=str(id_cliente)
            datos=self.base_datos.buscar_item(id_cliente)
            if len(datos)!=0:
                i=len(datos)
                self.tabla_productos.setRowCount(i)
                tablerow=0
                for row in datos:
                    self.Id=row[0]
                    self.tabla_productos.setItem(tablerow,0,QtWidgets.QTableWidgetItem(row[0]))
                    self.tabla_productos.setItem(tablerow,1,QtWidgets.QTableWidgetItem(row[1]))
                    self.tabla_productos.setItem(tablerow,2,QtWidgets.QTableWidgetItem(row[2]))
                    self.tabla_productos.setItem(tablerow,3,QtWidgets.QTableWidgetItem(row[3]))
                    self.tabla_productos.setItem(tablerow,4,QtWidgets.QTableWidgetItem(row[4]))
                    self.tabla_productos.setItem(tablerow,5,QtWidgets.QTableWidgetItem(row[5]))
                    self.tabla_productos.setItem(tablerow,6,QtWidgets.QTableWidgetItem(row[6]))
                    tablerow +=1
            else:
                self.line_buscar.setText('NoExiste')

    def registrar_productos(self):
            codigo=self.reg_codigo.text().upper()
            nombre=self.reg_nombre.text().upper()
            modelo=self.reg_modelo.text().upper()
            precio=self.reg_precio.text().upper()
            cantidad=self.reg_cantidad.text().upper()
            if codigo !='' and nombre!='' and modelo!='' and precio!=''and cantidad !='':
                self.base_datos.inserta_producto(codigo, nombre, modelo, precio, cantidad)
                self.signal_registrar.setText('Productos Registrados')
                self.reg_codigo.clear()
                self.reg_nombre.clear()
                self.reg_modelo.clear()
                self.reg_precio.clear()
                self.reg_cantidad.clear()
            else:
                self.signal_registrar.setText('Hay Espacios Vacios')
        
    def buscar_por_nombre_actualiza(self):
            id_producto=self.act_buscar.text().upper()
            id_producto=str("'"+id_producto+"'")
            self.producto=self.base_datos.busca_producto(id_producto)
            if len(self.producto)!=0:
                self.Id=self.producto[0][0]
                self.act_codigo.setText(self.producto[0][1])
                self.act_nombre.setText(self.producto[0][2])
                self.act_modelo.setText(self.producto[0][3])
                self.act_precio.setText(self.producto[0][4])
                self.act_cantidad.setText(self.producto[0][5])
            else: 
                self.signal_actualizar.setText('No existe')

    def modificar_productos(self):
            if self.producto !='':
                codigo=self.act_codigo.text().upper()
                nombre=self.act_nombre.text().upper()
                modelo=self.act_modelo.text().upper()
                precio=self.act_precio.text().upper()
                cantidad=self.act_cantidad.text().upper()
                act=self.base_datos.actualiza_productos(self.Id, codigo, nombre, modelo, precio, cantidad)

                if act==1:
                    self.signal_actualizar.setText("Actualizado")
                    self.act_codigo.clear()
                    self.act_nombre.clear()
                    self.act_modelo.clear()
                    self.act_precio.clear()
                    self.act_buscar.setText('')
                elif act==0:
                    self.signal_actualizar.setText('ERRROR')
                else:
                    self.signal_actualizar.setText('INCORRECTO')

    def buscar_por_nombre_eliminar(self):
            nombre_producto=self.eliminar_buscar.text().upper()
            nombre_producto=str("'"+nombre_producto+"'")
            producto=self.base_datos.buscar_producto(nombre_producto)
            self.tabla_borrar.setRowCount(len(producto))

            if len(producto)==0:
                self.signal_eliminacion.setText('No existe')
            else:
                self.signal_eliminacion.setText('Producto seleccionado')
            tablerow=0
            for row in producto:
                self.tabla_borrar.setItem(tablerow,0,QtWidgets.QTableWidgetItem(row[1]))
                self.tabla_borrar.setItem(tablerow,1,QtWidgets.QTableWidgetItem(row[2]))
                self.tabla_borrar.setItem(tablerow,2,QtWidgets.QTableWidgetItem(row[3]))
                self.tabla_borrar.setItem(tablerow,3,QtWidgets.QTableWidgetItem(row[4]))
                self.tabla_borrar.setItem(tablerow,4,QtWidgets.QTableWidgetItem(row[5]))
                tablerow+=1
            
    def eliminar_productos(self):
            self.row_flag=self.tabla_borrar.currentRow()
            if self.row_flag==0:
                self.tabla_borrar.removeRow(0)
                self.base_datos.elimina_productos("'"+self.producto_a_borrar+"'")
                self.signal_eliminacio.setText('Producto eliminado')
                self.eliminar_buscar.setText('')


if __name__=="__main__":
    app=QApplication(sys.argv)
    mi_app=VentanaPrincipal()
    mi_app.show()
    sys.exit(app.exec_())



                
                
        







        
            



