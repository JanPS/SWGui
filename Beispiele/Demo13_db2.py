# -*- coding: utf-8 -*-

# Wie vorher, jetzt aber mit Datenbank

from SWGui import *
import sqlite3 

conn = sqlite3.connect("meineDatenbank.db")
cursor = conn.cursor()

def erzeugeTabelleInDB(conn,cursor,tabellenname,daten):
    befehl="DROP TABLE "+tabellenname
    print "SQL-Befehl erzeugt: ", befehl
    try: cursor.execute(befehl)
    except: pass
    befehl="CREATE TABLE "+tabellenname+" ("
    for spaltenname in daten[0]: befehl=befehl+spaltenname+" TEXT, "
    befehl=befehl[:-2]+")"
    print "SQL-Befehl erzeugt: ", befehl
    cursor.execute(befehl)
    for z in daten[1:]:
        befehl="INSERT INTO "+tabellenname+" VALUES ("
        for x in z: befehl=befehl+"'"+str(x)+"', "
        befehl=befehl[:-2]+")"
        print "SQL-Befehl erzeugt: ", befehl
        cursor.execute(befehl)
    conn.commit()

spruenge = [["Vorname","Nachname","Sprung1","Sprung2","Sprung3"],
            ["Arno", "Nym", 340, 220, 415], 
            ["Wal", "Ross", 340, 20, 450], 
            ["Peter", "Pan", 0, 414, 405]]

tab=SWTable(0,0)
tab.fillData(spruenge)
erzeugeTabelleInDB(conn,cursor,"Weitsprungwettbewerb",spruenge)

def dr():
    print "Alles über die Tabelle"
    print tab.columnCount()," Spalten und ",tab.rowCount()," Zeilen"
    print "Current zeile,spalte", [tab.currentRow(), tab.currentColumn ()]
    print [tab.getColHead(i) for i in range(tab.columnCount())]
    for z in tab.getItems(): print z
    print "Nochamsl ueber getData"
    print tab.getData()
    
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
def speichern():
    erzeugeTabelleInDB(conn,cursor,"Spruenge",tab.getData())
buSave=SWButton("save",command=speichern)

SWstart()
