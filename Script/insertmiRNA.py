# -*- coding: utf-8 -*-
"""
Created on Sun May 15 20:23:52 2022

@author: Davide Morelli
"""

import shutil
import datetime
import os
import mysql.connector
db= mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="mirnaexpression"
        )

cursor=db.cursor()
sql="INSERT INTO mirna_expression VALUES (%s,%s,%s,%s,%s,%s,%s)"

def insertmiRNA(tipoSito):
    #os.mkdir("E:\TirocinioDati\FileCaricati_miRNA Expression Quantification")
    os.mkdir(os.path.join("E:\TirocinioDati\FileCaricati_miRNA Expression Quantification",tipoSito))
    os.chdir("E:\TirocinioDati\FileFinaliModificati_miRNA Expression Quantification") #CAMBIA DIRECTORY
    NFile=len(os.listdir())
    record=0
    countFile=1
    start=datetime.datetime.now()
    
    for file in os.listdir():
        
        now=datetime.datetime.now() #timestamp
        print("FILE: ",file," ",countFile,"DI ",NFile)
        
        
        record+=scriviRecordExpression(file,tipoSito)
       
        print("TEMPO INSERT FILE: ",countFile," ",datetime.datetime.now()-now) 
        print(" ")
        shutil.move(file,os.join.path("E:\TirocinioDati\FileCaricati_miRNA Expression Quantification",tipoSito))
        countFile+=1
        
    return "INSERITI: "+str(record)+" RECORD","TEMPO TRASCORSO:" + str(datetime.datetime.now()-start)

def scriviRecordExpression(file,tipoSito):
    
    cont=0
    with open(file,encoding='utf-8') as f:
        a=f.read().split('\n')
        case=a[0].split('\t')[1]   #prende il caso del paziente dalla prima riga del file
       
        
        FileName,estensione=os.path.splitext(file)
        lista=[case,FileName,tipoSito]
        for stringa in range(2,len(a)):
           
                
            if a[stringa]!="" and a[stringa][0]=='h':
               
                #rende il tutto una lista dal quale selezionare i valori
                dato=a[stringa].split('\t')
               
                
               
                cursor.execute(sql,lista+dato)
            
                cont+=1
                
              
    db.commit()  
    print("RECORD INSERITI: ",cont) 
    return cont