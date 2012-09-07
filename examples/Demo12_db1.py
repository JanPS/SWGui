# -*- coding: utf-8 -*-

from SWGui import *


spruenge = [["Vorname","Nachname","Sprung1","Sprung2","Sprung3"],
            ["Arno", "Nym", 340, 220, 415], 
            ["Wal", "Ross", 340, 20, 450], 
            ["Peter", "Pan", 0, 414, 405]]

tab=SWTable(0,0)
tab.fillData(spruenge)

def dr():
    print "Alles über die Tabelle"
    print tab.columnCount()," Spalten und ",tab.rowCount()," Zeilen"
    print "Current zeile,spalte", [tab.currentRow(), tab.currentColumn ()]
    print [tab.getColHead(i) for i in range(tab.columnCount())]
    for z in tab.getItems(): print z
buPrint=SWButton("drucken",command=dr)

def NZe(): tab.newRow(tab.rowCount(),"zn")
def NSp(): 
    titel=SWTextDialog("Spaltenname?",initText="NeueSpalte")
    tab.newCol(tab.columnCount(),titel)
buNeueZeile=SWButton("Neue Zeile",command=NZe)
buNeueSpalte=SWButton("Neue Spalte",command=NSp)
buDelRow=SWButton(u"Aktuelle Zeile löschen",
                  command=lambda: tab.removeRow(tab.currentRow()))
buColRow=SWButton(u"Aktuelle Spalte löschen",
                  command=lambda: tab.removeColumn(tab.currentColumn()))


SWstart()
