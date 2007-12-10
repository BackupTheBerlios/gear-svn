#==================================================================================================
#======================================          MENU        ======================================
#==================================================================================================
from xml.dom import minidom, Node
import sys, string,wx




class MyMenu(wx.MenuBar):
	
	def __init__(self,parent,inFileName):
		wx.MenuBar.__init__(self)
		self.file = inFileName
		self.parent = parent
		self.run(inFileName)




	def run(self,inFileName):                                            # [5]
		outFile = sys.stdout
		doc = minidom.parse(inFileName)
		rootNode = doc.documentElement
		level = 0
		self.BuildMenuBar(rootNode, outFile, level)

	
	def BuildMenuBar(self,parent, outFile, level,men=None):                               # [1]

		for node in parent.childNodes:
			if node.nodeType == Node.ELEMENT_NODE:
				tipo = node.nodeName


				#MENU
				if tipo=='Menu':
					m = wx.Menu()
					nome = node.getAttribute('name')
					
					if level==0:
						self.Append(m,nome)
					else:
						men.AppendMenu(-1,nome,m)
					
					#Rilancia la procedura
					self.BuildMenuBar(node, outFile, level+1,m)


				#MENUITEM
				elif tipo=='MenuItem':

					nome = node.getAttribute('name')
					evento = node.getAttribute('event')

					content = []                                        # [3]
					for child in node.childNodes:
						if child.nodeType == Node.TEXT_NODE:
							content.append(child.nodeValue)
						if content:
							strContent = string.join(content)
						else:
							strContent = nome
					

					MenItem = men.Append(-1,nome,strContent)
					self.parent.Bind(wx.EVT_MENU,eval(evento),MenItem)

				#SEPARATOR
				elif tipo=='Separator':
					men.AppendSeparator()

				#RADIO
				elif tipo=='RadioItem':
					content = []                                        # [3]
					for child in node.childNodes:
						if child.nodeType == Node.TEXT_NODE:
							content.append(child.nodeValue)
						if content:
							strContent = string.join(content)
						else:
							strContent = nome
					
					MenItem = men.AppendRadioItem(-1,strContent)

				#CHECK
				elif tipo=='CheckItem':
					content = []                                        # [3]
					for child in node.childNodes:
						if child.nodeType == Node.TEXT_NODE:
							content.append(child.nodeValue)
						if content:
							strContent = string.join(content)
						else:
							strContent = nome
					
					MenItem = men.AppendCheckItem(-1,strContent)
					
					

				#ALTRO (SALTA)
				else:
					print('errore')				
					

			

	def run(self,inFileName):                                            # [5]
		outFile = sys.stdout
		doc = minidom.parse(inFileName)
		rootNode = doc.documentElement
		level = 0
		self.BuildMenuBar(rootNode, outFile, level)



