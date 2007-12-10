#==================================================================================================
#======================================          TOOLBAR        ======================================
#==================================================================================================
from xml.dom import minidom, Node
import sys, string,wx





class MyToolBar(wx.ToolBar):
	
	def __init__(self,parent,inFileName):
		wx.ToolBar.__init__(self,parent,style=wx.TB_HORIZONTAL | wx.NO_BORDER)
		self.file = inFileName
		self.parent = parent
		self.run(inFileName)
		self.Layout()

	def Layout(self):
		self.SetToolBitmapSize((16,16))



	def run(self,inFileName):                                            # [5]
		outFile = sys.stdout
		doc = minidom.parse(inFileName)
		rootNode = doc.documentElement
		level = 0
		self.BuildToolBar(rootNode, outFile, level)

	
	def BuildToolBar(self,parent, outFile):                               # [1]

		for node in parent.childNodes:
			if node.nodeType == Node.ELEMENT_NODE:
				tipo = node.nodeName


				#MENUITEM
				if tipo=='Button':

					lab = node.getAttribute('label')
					evento = node.getAttribute('event')
					img = node.getAttribute('image')
					
					content = []                                        # [3]
					for child in node.childNodes:
						if child.nodeType == Node.TEXT_NODE:
							content.append(child.nodeValue)
						if content:
							strContent = string.join(content)
						else:
							strContent = nome
					
					bmp = wx.Image(img,wx.BITMAP_TYPE_PNG).ConvertToBitmap()
					ToolBarItem = self.AddSimpleTool(-1,bmp,lab,strContent)
					self.parent.Bind(wx.EVT_MENU,eval(evento),ToolBarItem)

				#SEPARATOR
				elif tipo=='Separator':
					self.AddSeparator()

				#ALTRO (SALTA)
				else:
					print('errore')				
					

			

	def run(self,inFileName):                                            # [5]
		outFile = sys.stdout
		doc = minidom.parse(inFileName)
		rootNode = doc.documentElement
		level = 0
		self.BuildToolBar(rootNode, outFile)

