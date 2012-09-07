# -*- coding: utf-8 -*-

# Wie vorher, jetzt aber mit Datenbank
# Jetzt mit neuer SWGUI und Tabellen Methoden darin

from SWGui import *

label=SWLabel("tabelle1")
tab=SWTable(0,0)
tab.connectDB("wp236.webpack.hosteurope.de","db10548912-py", # server, user
              "pypita9z","db10548912-pythontest", # password, datenbank
              "tabelle1")   # Tabellenname

counter=[0,0] # Zeilen- und Spaltenzahl
def NZe(): # Neue Zeile in Tabelle
    counter[0]+=1
    tab.newRow(tab.rowCount(),str(counter[0]))
def NSp(): 
    counter[1]+=1
    titel=SWTextDialog("Spaltenname?",initText="S"+str(counter[1]))
    if titel!=None: tab.newCol(tab.columnCount(),titel)

SWHBox()
SWButton("Neue Zeile",command=NZe)
SWButton("Neue Spalte",command=NSp)
SWButton(u"Aktuelle Zeile löschen",
                  command=lambda: tab.removeRow(tab.currentRow()))
SWButton(u"Aktuelle Spalte löschen",
                  command=lambda: tab.removeColumn(tab.currentColumn()))
def dateneintragen():
    s=SWTextDialog("Neue Liste in Python Syntax")
    tab.appendList(eval(s))
SWButton("Zeile Eintragen", command=dateneintragen)
SWLastContainer()
SWHBox()

def speichern(): tab.writeToDB()
def laden(): 
    if not(tab.refresh()): SWWarning("Problem - evtl existiert die Tabelle nicht")
SWButton("save",command=speichern)  
SWButton("load",command=laden)
def frageTabName():
    tab.name=SWTextDialog("Name?")
    if tab.name!=None:
        label.setText(tab.name)
        laden()
SWButton("Tabellennamensetzen",command=frageTabName)
SWButton("Tabellen in DB anzeigen",command=lambda : SWWarning(tab.getDBTables()))    

SWstart()
tab.closeDB()

