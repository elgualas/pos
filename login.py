import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView
from PyQt5.QtCore import QPropertyAnimation,QEasingCurve
from PyQt5 import QtCore,QtWidgets
from PyQt5.uic import loadUi
from conexion import Comunicacion
from main import *

class VentanaLogin(QMainWindow):
    def __init__(self):
        super(VentanaLogin,self).__init__()
        loadUi('interfaz_login.ui',self)

        self.base_datos=Comunicacion()
        self.click_posicion = None

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        self.gripSize=10
        self.grip=QtWidgets.QSizeGrip(self)
        self.grip.resize(self.gripSize,self.gripSize)

        self.frame.mouseMoveEvent=self.mover_ventana

        self.bt_ingresar.clicked.connect(self.iniciar_sesion)

    def mousePressEvent(self, event):
        self.click_posicion = event.globalPos()

    def mover_ventana(self, event):
        if self.isMaximized() == False:         
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.click_posicion)
                self.click_posicion = event.globalPos()
                event.accept()
    
    def iniciar_sesion(self):
        usuario=self.users.text()
        password=self.password.text()
        if usuario !='' and password!='': ##tener en cuenta '; OR TRUE --
                usuario_intro=self.users.text()
                usuario_intro=str(usuario_intro)
                password_intro=self.password.text()
                password_intro=str(password_intro)
                user=self.base_datos.buscar_usuario(usuario_intro,password_intro)
                if len(user)==1:
                     self.hide()
                     self.ventana=VentanaMain()
                     
                else:
                     print(len(user))
                     self.signal_incorrecto.setText('Contraseña o Usuario Incorrecta')
        else:
                self.signal_incorrecto.setText('Hay Espacios Vacios')

class VentanaMain(QMainWindow):
     def __init__(self):
          super().__init__()
          self.ventana=VentanaPrincipal()
          self.ventana.show()
    
if __name__=="__main__":
    app=QApplication(sys.argv)
    mi_app=VentanaLogin()
    mi_app.show()
    sys.exit(app.exec_())