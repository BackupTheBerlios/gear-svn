import wx
from wx.py.shell import Shell
from wx.py.editor import Editor
from wx.py.buffer import Buffer



class BottomPanel(wx.Notebook):

	def __init__(self,parente):
		wx.Notebook.__init__(self,parente,style=wx.NB_BOTTOM)
		#te = SimpleTextEditor(self)
		self.sh = PythonShell(self)
		#self.ed = PythonEditor(self)
		#self.AddPage(te,'Edit')
		self.AddPage(self.sh,'Shell')
		#self.AddPage(ed,'Editor')





class PythonShell(wx.Panel):
	def __init__(self,parente):
		wx.Panel.__init__(self,parente)
		sizer = wx.BoxSizer(wx.VERTICAL)
		self.shell = Shell(self,id=-1,size=parente.GetClientSize())
		sizer.Add(self.shell, 1, wx.EXPAND, 0)
		self.SetSizer(sizer)
			












#==================================================================================================
#=============================================     MAIN      ======================================
#==================================================================================================


if __name__ == '__main__':
	app = wx.PySimpleApp()
	frame = wx.Frame(None)
	frame.SetSize((600,500))
	#frame.control = wx.TextCtrl(frame, style=wx.TE_MULTILINE)
	
	panel = BottomPanel(frame)
	
	sizer_1 = wx.BoxSizer(wx.VERTICAL)
	sizer_1.Add(panel, 1, wx.EXPAND, 0)
	frame.SetAutoLayout(True)
	frame.SetSizer(sizer_1)
	


	frame.Show() 
	app.MainLoop()


