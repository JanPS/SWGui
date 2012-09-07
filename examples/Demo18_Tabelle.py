from SWGui import *

def changeHandler(z,s): 
    print "Neu:",[z,s], " = ", tab.getItem(z,s)
def clickHandler(z,s): 
    print "Klick:",[z,s], " = ", tab.getItem(z,s)
    
SWLabel("Tabellen-Demo")
SWsetWindowTitle("Tabellen-Demo Nr. 1")
tab=SWTable(3,5)
tab.setChangedCommand(changeHandler)
tab.setClickedCommand(clickHandler)
def spaltenEvent(n): print "spalte ",n
tab.setColHeaderClickCommand(spaltenEvent)
def zeilennEvent(n): print "zeile ",n
tab.setRowHeaderClickCommand(spaltenEvent)

tab.setItem(2,2,"Hallo")
tab.setColHeaders(["Anzahl","Artikel","Preis","Bestellnummer","Kommentar"])
tab.setRowHeaders(["Zeile 0","Zeile 1","Zeile 2"])

SWstart()

