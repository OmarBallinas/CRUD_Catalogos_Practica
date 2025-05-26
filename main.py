# main.py
import wx
from LoginGUI import LoginGUI

if __name__ == "__main__":
    app = wx.App(False)  # Inicializa la app gráfica
    frame = LoginGUI()   # Muestra la pantalla de login
    app.MainLoop()       # Inicia el bucle de eventos