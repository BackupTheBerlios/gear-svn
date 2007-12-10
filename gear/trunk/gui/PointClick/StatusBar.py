import wx


class MyStatusBar(wx.StatusBar):
	
	def __init__(self,parent,NrFields):
		self.parent = parent
		wx.StatusBar.__init__(self,self.parent)
		self.NrFields = NrFields
		self.Build()
	
	def Build(self):
		self.SetFieldsCount(self.NrFields)
		
	def AssignText(self,text,position):
		self.SetStatusText(text,position)
		
