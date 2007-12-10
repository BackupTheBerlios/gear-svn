import wx
from wx.py.editor import Editor
from wx.py.buffer import Buffer


class EditorNotebook(wx.Notebook):

	def __init__(self,parente):
		wx.Notebook.__init__(self,parente,style=wx.NB_TOP)
		#te = SimpleTextEditor(self)
		self.ed = PythonEditor(self)
		self.AddPage(self.ed,'File')



class PythonEditor(wx.Panel):
	def __init__(self,parente,filename=None):
		wx.Panel.__init__(self,parente)
		sizer = wx.BoxSizer(wx.VERTICAL)
		self.buffer = Buffer()
		self.editor = Editor(self,id=-1,size=parente.GetClientSize())
		self.buffer.addEditor(self.editor)
		self.buffer.open(filename)
		self.buffer.interp.locals.clear()
		
		sizer.Add(self.editor.window, 1, wx.EXPAND, 0)
		self.SetSizer(sizer)
			

class SimpleTextEditor(wx.Panel):
		def __init__(self,parente):
			wx.Panel.__init__(self,parente)
			sizer = wx.BoxSizer(wx.VERTICAL)
			self.txt = wx.TextCtrl(self, style=wx.TE_MULTILINE,size=parente.GetClientSize())
			sizer.Add(self.txt, 1, wx.EXPAND, 0)
			self.SetSizer(sizer)





#==================================================================================================
#=============================================     MAIN      ======================================
#==================================================================================================


if __name__ == '__main__':
	app = wx.PySimpleApp()
	frame = wx.Frame(None)
	frame.SetSize((600,500))
	#frame.control = wx.TextCtrl(frame, style=wx.TE_MULTILINE)
	
	panel = EditorNotebook(frame)
	
	sizer_1 = wx.BoxSizer(wx.VERTICAL)
	sizer_1.Add(panel, 1, wx.EXPAND, 0)
	frame.SetAutoLayout(True)
	frame.SetSizer(sizer_1)
	


	frame.Show() 
	app.MainLoop()


