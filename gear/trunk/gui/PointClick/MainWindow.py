#==================================================================================================
#=========================================   APPLICAZIONE   =======================================
#==================================================================================================
import wx
from MenuBar import MyMenu
from StatusBar import MyStatusBar
from ToolBar import MyToolBar
#from rpy import *
import sys, string,wx
import PanelBottom.PanelBottom as PB
import Editor.TabbedNotebook 
import Editor.TabbedNotebookNew as ED
#import wx.py.editor as ED

ID_SIMPLE = wx.NewId() 
class MyFrame(wx.Frame): 


	def __init__(self): 
		wx.Frame.__init__(self, None, -1,"Enable/Disable Menu Example") 


		#Split windows
		self.window_1 = wx.SplitterWindow(self, -1, style=wx.SP_3D|wx.SP_BORDER)
		self.window_1_pane_1 = wx.Panel(self.window_1, -1)
		self.window_2 = wx.SplitterWindow(self.window_1_pane_1, -1, style=wx.SP_3D|wx.SP_BORDER)
		self.browser = wx.Panel(self.window_2, -1)
		self.editor = ED.EditorNotebookNew(self.window_2,filename='Nuovo')
		self.output = PB.BottomPanel(self.window_1)

		self.__do_layout()
		
		self.menuBar = MyMenu(self,'Menu.xml') 
		self.SetMenuBar(self.menuBar)

		self.StatusBar = MyStatusBar(self,3)
		self.SetStatusBar(self.StatusBar)
		
		self.ToolBar = MyToolBar(self,'StatusBar.xml')
		self.SetToolBar(self.ToolBar)
		self.ToolBar.Realize()




	def __do_layout(self):
		# begin wxGlade: MyFrame.__do_layout
		self.window_1.SetMinimumPaneSize(100)		
		sizer_1 = wx.BoxSizer(wx.VERTICAL)
		sizer_2 = wx.BoxSizer(wx.VERTICAL)
		self.window_2.SplitVertically(self.browser, self.editor)
		self.window_2.SetMinimumPaneSize(100)
		sizer_2.Add(self.window_2, 1, wx.EXPAND, 0)
		self.window_1_pane_1.SetAutoLayout(True)
		self.window_1_pane_1.SetSizer(sizer_2)
		sizer_2.Fit(self.window_1_pane_1)
		sizer_2.SetSizeHints(self.window_1_pane_1)
		self.window_1.SplitHorizontally(self.window_1_pane_1, self.output)
		sizer_1.Add(self.window_1, 1, wx.EXPAND, 0)
		self.SetAutoLayout(True)
		self.SetSizer(sizer_1)
		self.Layout()
		# end wxGlade



	def FileOpen (self,event):
		wx.MessageBox('Finestra di messaggio','Comunicazione',wx.OK|wx.ICON_INFORMATION,self)
		return None


	def grafico(self,event):
		x = range(0, 10)
		y = [ 2*i for i in x ]
		#r.plot_default(x, y)	
		


	def OnRunScript (self,event):
		Script = str(self.editor.GetFileName())
		wx.MessageBox('Chiudi',Script,wx.OK|wx.ICON_INFORMATION,self)
		self.output.sh.shell.runfile(str(Script))
		#self.output.sh.shell.push('execfile(%r)' % (Script))
		return None

	def OnRunSelection (self,event):
		selection = self.editor.GetSelection()
		self.output.sh.shell.push(selection)
		return None

	def OnHelp (self,event):
		self.editor.bufferCreateHTML('C:/Programmi/R/R-2.2.0/library/Bhat/html/00Index.html','R-Help')



				
	def FileNewModel ():
		return None

	def FileNewGraphic ():
		return None

	def RiFileNewModel ():
		return None

	def RiFileNewGraphic ():
		return None

	def WindowCascade ():
		return None

	def WindowAlign ():
		return None


	


if __name__ == '__main__':
	app = wx.PySimpleApp()
	frame = MyFrame()
	frame.SetSize((600,500))
	frame.Maximize()
	frame.Show() 
	frame.StatusBar.AssignText('testo',1)
	app.MainLoop()


