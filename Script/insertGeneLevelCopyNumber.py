# -*- coding: utf-8 -*-
"""
Created on Sun May 15 20:48:26 2022

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
        database="genelevelcopynumber"
        )

cursor=db.cursor()
sql="INSERT INTO gene_level_copy_number VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

def insertGeneLevelCopyNumber(tipoSito):
  
    os.mkdir(os.path.join("E:\TirocinioDati\FileCaricati_Gene Level Copy Number",tipoSito))
    os.chdir("E:\TirocinioDati\FileFinaliModificati_Gene Level Copy Number") #CAMBIA DIRECTORY
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
        shutil.move(file,os.path.join("E:\TirocinioDati\FileCaricati_Gene Level Copy Number",tipoSito))
        countFile+=1
     
    return "INSERITI: "+str(record)+" RECORD","TEMPO TRASCORSO:" + str(datetime.datetime.now()-start)

def scriviRecordExpression(file,tipoSito):
    
    cont=0
    with open(file,encoding='utf-8') as f:
        a=f.read().split('\n')
        case=a[0].split('\t')[1]   #prende il caso del paziente dalla prima riga del file
       
        sample=a[0].split('\t')[2] 
       
        
        FileName,estensione=os.path.splitext(file)
        lista=[case,FileName,tipoSito,sample]
        for stringa in range(2,len(a)):
           
                
            if a[stringa]!="" and a[stringa][0]=='E':
               
                #rende il tutto una lista dal quale selezionare i valori
                dato=a[stringa].split('\t')
                l=[]
                for x in dato:
                    if x!="": l.append(x)
                    else: l.append(0)
                
                
               
                cursor.execute(sql,lista+l)
            
                cont+=1
                
              
    db.commit()  
    print("RECORD INSERITI: ",cont) 
    return cont