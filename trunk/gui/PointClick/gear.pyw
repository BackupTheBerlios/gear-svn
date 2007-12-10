import wx
from MainWindow import *


#==================================================================================================
#=============================================     MAIN      ======================================
#==================================================================================================


if __name__ == '__main__':
	app = wx.PySimpleApp()
	frame = MyFrame()
	frame.SetSize((600,500))
	frame.Maximize()
	frame.Show() 
	frame.StatusBar.AssignText('testo',1)
	app.MainLoop()




