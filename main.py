# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication
from ui_arayuz import arayuz
    
uygulama= QApplication([])
pencere=arayuz()
pencere.show()
uygulama.exec_()