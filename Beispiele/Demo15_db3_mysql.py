# -*- coding: utf-8 -*-

# Wie vorher, jetzt aber mit Datenbank

from SWGui import *
#import sqlite3 
import MySQLdb


#conn = sqlite3.connect("meineDatenbank.db")
conn=MySQLdb.connect(host="wp236.webpack.hosteurope.de",user="db10548912-py",passwd="pypita9z",db="db10548912-pythontest")


# Soweit ich das verstehe sollte das gleiche Programm auch laufen, wenn man 
# statt sqlite 3 folgendes importiert (Mysqldb muss dazu erst installiert werden):
# import MySQLdb 
# conn = MySQLdb.connect("server-url","benutzername", "passwort", "datenbank") 


# ------------- Jetzt folgenden Funktionen zum speichern und holen von Tabellen
# ------------- sowie zum holnen der Tabellennamen und Spaltennamen in Tabellen
def erzeugeTabelleInDB(conn,tabellenname,daten):
    cursor = conn.cursor()
    befehl="DROP TABLE "+tabellenname
    print "SQL-Befehl erzeugt: ", befehl
    try: cursor.execute(befehl)
    except: pass
    befehl="CREATE TABLE "+tabellenname+" ("
    for spaltenname in daten[0]: befehl=befehl+spaltenname+" VARCHAR(45), "
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
    cursor.close()


def holeBestimmteDaten(conn,tabellenname,datennamen):
    cursor = conn.cursor()
    namen=""
    for n in datennamen: namen=namen+n+", "
    namen=str(namen[:-2])
    tabellenname=str(tabellenname)
    print "SELECT "+namen+" FROM "+tabellenname
    cursor.execute("SELECT "+namen+" FROM "+tabellenname) 
    res=[datennamen]+map(list,cursor.fetchall()) 
    cursor.close()
    return res

def holeSQLDaten(conn,anfrage):
    cursor = conn.cursor()
    cursor.execute(anfrage) 
    spNames=[x[0] for x in cursor.description]
    res=[spNames ]+map(list,cursor.fetchall()) 
    cursor.close()
    return res
    
def holeTabellenSpalten(conn,tabellenname): 
    cursor = conn.cursor()
    #befehl=str("SELECT sql FROM sqlite_master WHERE name = '"+tabellenname+"'")
    befehl=str("SHOW COLUMNS FROM "+tabellenname)
    print "SQL-Befehl: ",befehl, " Typ: ", type(befehl)
    cursor.execute(befehl)
    #s=cursor.fetchall()[0][0]
    #cursor.close()
    #s=s.split("(")[1][:-1]
    #s=s.split(",")
    #return [str(x.split()[0]) for x in s]
    s=cursor.fetchall()
    spalten=[]
    for spalte in s:
        spalten.append(spalte[0])
    return spalten
    

def holeDaten(conn,tabellenname):
    return holeBestimmteDaten(conn,tabellenname,holeTabellenSpalten(conn,tabellenname))

def holeTabellenNamen(conn):
    """holeTabellenNamen holt alle Tabellennamen aus einer Dstenbank
    
    """
    cursor = conn.cursor()
    #cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
    cursor.execute("SHOW TABLES")
    s=cursor.fetchall()
    s=[x[0] for x in s]
    cursor.close()
    return map(str,s)
#------------- Ende der allgemeinen Datenbankutilities


def fuelleTabelle(*args): 
    print "fuelle: ",tabbox.currentText()
    print "Fuelle d ", holeTabellenSpalten(conn,tabbox.currentText())
    tab.fillData(holeDaten(conn,tabbox.currentText()))

tabbox=SWComboBox(holeTabellenNamen(conn), command=fuelleTabelle)

print "Tabbox:", tabbox.currentText()
tab=SWTable(0,0)
fuelleTabelle()

def NZe(): tab.newRow(tab.rowCount(),"zn")
def NSp(): 
    titel=SWTextDialog("Spaltenname?",initText="NeueSpalte")
    if titel!=None: tab.newCol(tab.columnCount(),titel)

SWHBox()
buNeueZeile=SWButton("Neue Zeile",command=NZe)
buNeueSpalte=SWButton("Neue Spalte",command=NSp)
buDelRow=SWButton(u"Aktuelle Zeile löschen",
                  command=lambda: tab.removeRow(tab.currentRow()))
buColRow=SWButton(u"Aktuelle Spalte löschen",
                  command=lambda: tab.removeColumn(tab.currentColumn()))

SWLastContainer()
SWHBox()
def SQLAnfrage():
    q=SWTextDialog("SQL Frage?",initText="SELECT ")
    if q!=None: tab.fillData(holeSQLDaten(conn,q))  
buSQL=SWButton("SQL-Anfrage", command=SQLAnfrage)

def speichern():
    tabname=SWTextDialog("Tabellenname?",initText="Tabelle1")
    if tabname!=None:     
        erzeugeTabelleInDB(conn,tabname,tab.getData())
        tabbox.addItem(tabname)
buSave=SWButton("save",command=speichern)

def printTabellen(): print "Tabellennamen: ",holeTabellenNamen(conn)
SWButton("Liste Tabellen", command=printTabellen)

SWstart()
conn.close()
