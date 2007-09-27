# -*- coding: cp1252 -*-

import win32com.client
import time


def insertIntoCell( strCellName, strText, objTable):
objCellText = objTable.getCellByName( strCellName)
objCellCursor = objCellText.createTextCursor()
objCellCursor.setPropertyValue("CharColor",16777215)
objCellText.insertString(objCellCursor, strText, False)


objServiceManager = win32com.client.Dispatch("com.sun.star.ServiceManager")
objDesktop = objServiceManager.CreateInstance("com.sun.star.frame.Desktop")

args = []

#si nouveau document, ligne suivante
#objDocument = objDesktop.loadComponentFromURL("private:factory/swriter", 
"_blank", 0, args)
"""
//swriter pour le traitement de texte.
//scalc pour le tableur
//sdraw pour l'éditeur de dessin
//simpress pour l'éditeur de présentation (équivalent de PowerPoint)
//smath pour l'éditeur de formule mathématique
//swriter/Global Document document maitre
//swriter/web Pour l'éditeur HTML
"""
#si document existant
objDocument = objDesktop.loadComponentFromURL("file:///C:/ootest.odt", 
"_blank", 0, args)


objText = objDocument.GetText()
objCursor = objText.createTextCursor()
objText.insertString(objCursor, "Vous avez les salutations de PONX.\nCeci 
est la deuxième ligne.\n", 0)
objText.insertString(objCursor, "Troisième ligne.\n", 0)
objText.insertString(objCursor, "4è ligne éèë?@ç.\n\n\n", 0)



# Tableau

#Crée un tableau de 4 colonnes x 4 lignes
objTable= objDocument.createInstance( "com.sun.star.text.TextTable")
objTable.IsWidthRelative = True
objTable.RelativeWidth = 80 # largeur de 80 %
objTable.BackColor = 255*256*256+255*256+204 # fond en jaune clair
objTable.HoriOrient = 2 # 0 LEFT 1 RIGHT 2 CENTER
objTable.initialize(8, 4) # lignes / colonnes

#Insère la table
objText.insertTextContent(objCursor, objTable, 0)

#1ère ligne
objRows = objTable.getRows()
objRow0 = objRows.getByIndex(0)

#Couleur de fond
objTable.setPropertyValue("BackTransparent", 0)
objTable.setPropertyValue("BackColor", 255*256*256+255*256+204)

#Autre couleur de fond, pour la première ligne
objRow0.setPropertyValue("BackTransparent", 0)
objRow0.setPropertyValue("BackColor", 6710932)
objRow0.setPropertyValue("IsAutoHeight", False)
objRow0.setPropertyValue("Height", 3000) #30 mm

#Remplissage 1ère ligne
insertIntoCell("A1","FirstColumn",objTable)
insertIntoCell("B1","SecondColumn",objTable)
insertIntoCell("C1","ThirdColumn",objTable)
insertIntoCell("D1","SUM",objTable)

#Remplissage suite
objTable.getCellByName("A2").setValue(22.5)
objTable.getCellByName("B2").setValue(5615.3)
objTable.getCellByName("C2").setValue(-2315.7)
objTable.getCellByName("D2").setFormula("sum(<A2>|<B2>|<C2>)")

objTable.getCellByName("A3").setValue(21.5)
objTable.getCellByName("B3").setValue(615.3)
objTable.getCellByName("C3").setValue(-315.7)
objTable.getCellByName("D3").setFormula("sum(<A3:C3>)")

objTable.getCellByName("A4").setValue(121.5)
objTable.getCellByName("B4").setValue(-615.3)
objTable.getCellByName("C4").setValue(415.7)
objTable.getCellByName("D4").setFormula("sum ")


#on sélectionne la colonne C
sCell = objTable.createCursorByCellName("C1")
sCell.goDown(4, True)
sCell.BackColor = 255*256*256+200*256+200 #rouge clair

""" ça ne marche pas (spécif OO-2.0 ?)
cols = objTable.getColumns()
col = cols.getByIndex(2)
"""


#Couleur des caractères et ombre
objCursor.setPropertyValue("CharColor", 255)
objCursor.setPropertyValue("CharShadowed", True)

#Saut de paragraphe
#The second argument is a 
com::sun::star::text::ControlCharacter::PARAGRAPH_BREAK constant
objText.insertControlCharacter(objCursor, 0 , False)

#Insertion texte
objText.insertString(objCursor, " Texte coloré - bleu avec ombre\n", False)


#Saut de paragraphe (caractère spécial PARAGRAPH_BREAK = 0).
objText.insertControlCharacter(objCursor, 0, False)


#on repasse en noir, sans ombre
objCursor.setPropertyValue("CharColor", 0)
objCursor.setPropertyValue("CharShadowed", False)


# Attention : ces 4 lignes fonctionnent en invisible.
objText.insertString(objCursor, "RRRRRRRRRRR", False)
objCursor.goLeft(3, False)
objCursor.goLeft(5, True)
objCursor.String="+++"
objCursor.gotoEndOfParagraph(False)

#Saut de paragraphe
objText.insertControlCharacter(objCursor, 0, False)

#Création d'un cadre (TextFrame)
objTextFrame= objDocument.createInstance("com.sun.star.text.TextFrame")
objTextFrame.Width = 10400 # 104 mm largeur
#objTextFrame.Height =2000 # 20 mm de haut # ne sert à rien, le cadre 
d'agrandit tout seul

#Affectation type de cadre (AnchorType.AS_CHARACTER = 1)
objTextFrame.setPropertyValue("AnchorType", 1)

#insertion du cadre
objText.insertTextContent(objCursor, objTextFrame, False)

#Lecture du texte du cadre
objFrameText= objTextFrame.getText()

#Positionnement curseur interne
objFrameTextCursor= objFrameText.createTextCursor()

#Insertion texte
objFrameText.insertString(objFrameTextCursor, "Encore du 
texte\naaaaaaaaaaaa\nbbbbbbb\nccccc\n", False)
objFrameText.insertString(objFrameTextCursor, "\net une autre ligne.", 
False)
objFrameText.insertString(objFrameTextCursor, "AAAAAAAA1\n", False)
objFrameText.insertString(objFrameTextCursor, "AAAAAAAA2\n", False)
objFrameText.insertString(objFrameTextCursor, "AAAAAAAA3\n", False)
objFrameText.insertString(objFrameTextCursor, "AAAAAAAA4\n", False)
objFrameText.insertString(objFrameTextCursor, "AAAAAAAA5", False)







#Création d'un cadre (TextFrame)
objTextFrame= objDocument.createInstance("com.sun.star.text.TextFrame")
objTextFrame.Width = 8000 # 80 mm largeur

objTextFrame.setPropertyValue("AnchorType", 1)

# on va mettre la cadre à la place d'autre chose (remplacement)
och=objDocument.createSearchDescriptor()
och.SearchString="%CADRE1%"
och.SearchWords = False #mots entiers seulement ?
position=objDocument.findFirst(och)
position.String=""


# on remplit le cadre
objText.insertTextContent(position, objTextFrame, False)
objFrameText= objTextFrame.getText()
objFrameTextCursor= objFrameText.createTextCursor()
objFrameText.insertString(objFrameTextCursor, "1111111\n", False)
objFrameText.insertString(objFrameTextCursor, "2222222222\n", False)
objFrameText.insertString(objFrameTextCursor, "333333333", False)



#couleur texte et sans ombre
objCursor.setPropertyValue("CharColor", 255*256*256+0*256+0)
objCursor.setPropertyValue("CharShadowed", False)

#Insertion texte
objText.insertString(objCursor, "\n\n\nThat's all for now !!", False)


#recherche et remplacement
orempl=objDocument.createReplaceDescriptor()
orempl.SearchString="ABC"
orempl.ReplaceString="XXXYYYZZZ"
orempl.SearchWords = False #mots entiers seulement ?
orempl.SearchCaseSensitive = True #sensible à la casse ?
nb = objDocument.replaceAll(orempl)

print "Nb remplacements :",nb


#recherche, effacement et insertion
och=objDocument.createSearchDescriptor()
och.SearchString="%TXT1%"
och.SearchWords = False #mots entiers seulement ?
position=objDocument.findFirst(och)

position.String="" #remplacement
position.setPropertyValue("CharColor", 255*256*256) #rouge Rouge*256*256 + 
Vert*256 + Bleu
#position.goRight(1, False)
objText.insertString(position, "Texte de remplacement", 0)
objText.insertString(position, "Texte ajouté", 0)


#impression, sauvergarde, sortie
objDocument.Print(args)
objDocument.storeAsURL("file:///C:/ootest2.odt", args)
objDesktop.Terminate()
