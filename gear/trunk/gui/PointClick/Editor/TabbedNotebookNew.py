

from wx.py.buffer import Buffer
from wx.py.editor import *
import wx.py.crust
import wx.py.dispatcher
import wx.py.editwindow
import wx.py.frame
from wx.py.shell import Shell
import wx.py.version
from wx import stc
import wx.html


class EditorNotebookNew(wx.Notebook):
	"""A notebook containing a page for each editor."""

	def __init__(self, parent,filename=None):
		"""Create EditorNotebook instance."""
		wx.Notebook.__init__(self, parent, id=-1, style=wx.CLIP_CHILDREN)
		self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnPageChanging, id=self.GetId())
		self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged, id=self.GetId())
		self.Bind(wx.EVT_IDLE, self.OnIdle)



		#AGGIUNTO DA PAOLO
		self.buffers = {}
		self.buffer = None  # Current buffer.
		self.editor = None
		self._defaultText = ' - the tastiest Python editor.'
		self._statusText = self._defaultText
		if filename:
			self.bufferCreate(filename)

		self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)

	#============================= DA EDITORFRAME ==========================

	def hasBuffer(self):
		"""Return True if there is a current buffer."""
		if self.buffer:
			return True
		else:
			return False

	def bufferClose(self):
		"""Close buffer."""
		if self.bufferHasChanged():
			cancel = self.bufferSuggestSave()
			if cancel:
				return cancel
		self.bufferDestroy()
		cancel = False
		return cancel

	def bufferHasChanged(self):
		"""Return True if buffer has changed since last save."""
		if self.buffer:
			return self.buffer.hasChanged()
		else:
			return False


	def bufferSave(self):
		"""Save buffer to its file."""
		if self.buffer.doc.filepath:
			self.buffer.save()
			cancel = False
		else:
			cancel = self.bufferSaveAs()
		return cancel

	def bufferSaveAs(self):
		"""Save buffer to a new filename."""
		if self.bufferHasChanged() and self.buffer.doc.filepath:
			cancel = self.bufferSuggestSave()
			if cancel:
				return cancel
		filedir = ''
		if self.buffer and self.buffer.doc.filedir:
			filedir = self.buffer.doc.filedir
		result = saveSingle(directory=filedir)
		if result.path:
			self.buffer.saveAs(result.path)
			cancel = False
		else:
			cancel = True
		return cancel

	def bufferSuggestSave(self):
		"""Suggest saving changes.  Return True if user selected Cancel."""
		result = messageDialog(parent=None, message='%s has changed.\n Would you like to save it first?' % self.buffer.name,title='Save current file?')
		if result.positive:
			cancel = self.bufferSave()
		else:
			cancel = result.text == 'Cancel'
		return cancel

	def updateNamespace(self):
		"""Update the buffer namespace for autocompletion and calltips."""
		if self.buffer.updateNamespace():
			self.SetStatusText('Namespace updated')
		else:
			self.SetStatusText('Error executing, unable to update namespace')



	def setEditor(self, editor):
		self.editor = editor
		self.buffer = self.editor.buffer
		self.buffers[self.buffer.id] = self.buffer


	def OnClose(self, event):
		"""Event handler for closing."""
		for buffer in self.buffers.values():
			self.buffer = buffer
			if buffer.hasChanged():
				cancel = self.bufferSuggestSave()
				if cancel and event.CanVeto():
					event.Veto()
					return
		self.Destroy()



	#============================= DA EDITORNOTEBOOK ==========================


	def OnIdle(self, event):
		"""Event handler for idle time."""
		self._updateTabText()
		event.Skip()

	def _updateTabText(self):

		"""Show current buffer display name on all but first tab."""
		size = 3
		changed = ' **'
		unchanged = ' --'
		selection = self.GetSelection()
		if selection < 1:
			return

		#print("===============================================================================")
		#print(selection.__class__)
		
		#TODO: if introdotto da Paolo
		if selection.__class__!="<type 'str'>":
			return
		
		text = self.GetPageText(selection)
		window = self.GetPage(selection)
		if not window.editor:
			return
		if text.endswith(changed) or text.endswith(unchanged):
			name = text[:-size]
		else:
			name = text
		if name != window.editor.buffer.name:
			text = window.editor.buffer.name
		if window.editor.buffer.hasChanged():
			if text.endswith(changed):
				text = None
			elif text.endswith(unchanged):
				text = text[:-size] + changed
			else:
				text += changed
		else:
			if text.endswith(changed):
				text = text[:-size] + unchanged
			elif text.endswith(unchanged):
				text = None
			else:
				text += unchanged
		if text is not None:
			self.SetPageText(selection, text)
			self.Refresh()  # Needed on Win98.

	def OnPageChanging(self, event):
		"""Page changing event handler."""
		event.Skip()

	def OnPageChanged(self, event):
		"""Page changed event handler."""
		new = event.GetSelection()
		window = self.GetPage(new)
		#if new.__class__=="<class 'wx.html.HtmlWindow'>":		#Paolo-temporaneo
		#	return
		dispatcher.send(signal='EditorChange', sender=self,editor=window.editor)
		window.SetFocus()
		event.Skip()





	#============================= DA EDITORNOTEBOOKFRAME ==========================

	def bufferCreate(self, filename=None):
		"""Create new buffer."""
		buffer = Buffer()
		panel = wx.Panel(parent=self, id=-1)
		panel.Bind(wx.EVT_ERASE_BACKGROUND, lambda x: x)        
		editor = Editor(parent=panel)
		panel.editor = editor
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(editor.window, 1, wx.EXPAND)
		panel.SetSizer(sizer)
		panel.SetAutoLayout(True)
		sizer.Layout()
		buffer.addEditor(editor)
		buffer.open(filename)
		self.setEditor(editor)
		self.AddPage(page=panel, text=self.buffer.name, select=True)
		self.editor.setFocus()

	def bufferDestroy(self):
		"""Destroy the current buffer."""
		selection = self.GetSelection()
##         print "Destroy Selection:", selection
		if selection > 0:  # Don't destroy the PyCrust tab.
			if self.buffer:
				del self.buffers[self.buffer.id]
				self.buffer = None  # Do this before DeletePage().
			self.DeletePage(selection)

	def bufferNew(self):
		"""Create new buffer."""
		self.bufferCreate()
		cancel = False
		return cancel

	def bufferOpen(self):
		"""Open file in buffer."""
		filedir = ''
		if self.buffer and self.buffer.doc.filedir:
			filedir = self.buffer.doc.filedir
		result = openMultiple(directory=filedir)
		for path in result.paths:
			self.bufferCreate(path)
		cancel = False
		return cancel

	#============================= DA FRAME ==========================

	def OnFileNew(self, event):
		self.bufferNew()

	def OnFileOpen(self, event):
		self.bufferOpen()

	def OnFileClose(self, event):
		self.bufferClose()

	def OnFileSave(self, event):
		self.bufferSave()

	def OnFileSaveAs(self, event):
		self.bufferSaveAs()


	def OnFind(self,event):
		self.editor.window.FindText()	

	#============================ AGGIUNTE DA PAOLO ==================
	def GetFileName(self):
		return self.buffer.doc.filepath

	def GetSelection(self):
		ActiveTab = self.editor.window
		selez = stc.StyledTextCtrl.GetSelectedText(ActiveTab)
		return(selez)


	def OnRightDown(self,event):
		self.PopupMenu(MyPopupMenu(self), event.GetPosition())


	def bufferCreateHTML(self, filename=None,PageName=None):
		"""Create new HTML buffer."""
		html = wx.html.HtmlWindow(self)
		#print("===============================================================================")
		#print(html.__class__)
		html.LoadPage(filename)
		panel = wx.Panel(parent=self, id=-1)
		panel.Bind(wx.EVT_ERASE_BACKGROUND, lambda x: x)        


		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(html, 1, wx.EXPAND)
		panel.SetSizer(sizer)
		panel.SetAutoLayout(True)
		sizer.Layout()

		self.AddPage(page=panel, text=PageName, select=True)




class MyPopupMenu(wx.Menu):
    def __init__(self):
        wx.Menu.__init__(self)
        #self.WinName = WinName
        item = wx.MenuItem(self, wx.NewId(), "Item One")
        self.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.OnItem1, item)
        item = wx.MenuItem(self, wx.NewId(),"Item Two")
        self.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.OnItem2, item)
        item = wx.MenuItem(self, wx.NewId(),"Item Three")
        self.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.OnItem3, item)

    def OnItem1(self, event):
        print "Item One selected in the 1 window"

    def OnItem2(self, event):
        print "Item Two selected in the 2 window"

    def OnItem3(self, event):
        print "Item Three selected in the 3 window"


