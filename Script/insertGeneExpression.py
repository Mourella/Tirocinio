# -*- coding: utf-8 -*-
"""
Created on Sun Apr  3 11:24:42 2022

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
        database="geneexpression"
        )

cursor=db.cursor()
sql="INSERT INTO gene_expression VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
sql1="INSERT INTO gene_synonyms values (%s,%s)"
sql2="INSERT INTO gene_type VALUES(%s,%s)"



def insertGeneExpression(tipoSito):
    os.mkdir(os.path.join('E:\TirocinioDati\FileCaricati_Gene Expression Quantification',tipoSito))
    os.chdir("E:\TirocinioDati\FileFinaliModificati_Gene Expression Quantification") #CAMBIA DIRECTORY
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
        shutil.move(file, os.path.join('E:\TirocinioDati\FileCaricati_Gene Expression Quantification',tipoSito))
        countFile+=1
     
    return "INSERITI: "+str(record)+" RECORD","TEMPO TRASCORSO:" + str(datetime.datetime.now()-start)

def scriviRecordExpression(file,tipoSito):
    cont=0
    with open(file,encoding='utf-8') as f:
        a=f.read().split('\n')
        case=a[0].split('\t')[1]   #prende il caso del paziente dalla prima riga del file
       # submitter=a[0].split('\t')[0]
        
        FileName,estensione=os.path.splitext(file)
        for stringa in range(7,len(a)):
          
                
            if a[stringa]!="" and a[stringa][0]=='E':
               
                #rende il tutto una lista dal quale selezionare i valori
                dato=a[stringa].split('\t')
               
                values=(case,FileName,tipoSito,dato[0],dato[1],dato[6],dato[7],dato[8])
               
                cursor.execute(sql,values)
            
                cont+=1
                
              
    db.commit()  
    print("RECORD INSERITI: ",cont) 
    return cont


def scriviRecordName():
   
    cont=0
    c=0
    with open("gene_synonyms.txt",encoding='utf-8') as f:
        a=f.read().split('\n')
        
        
        for stringa in a:
            if stringa!="":
                stringa=stringa.split(',')
                ID=stringa[0]
                for sin in stringa[1:]:
                    values=(ID,sin)
             
                    cursor.execute(sql1,values)  #inserisco i dati passando la lista dei valori
                    c+=1
                cont+=1
                print(cont)
    db.commit()  
    return c

def scriviGeneType():
    cont=0
    with open("tester.tsv",encoding='utf-8') as f:
        a=f.read().split('\n')
        for stringa in range(7,len(a)): ###CAMBIAREEEEEEEEEE IL /
            print(cont)
            
            if a[stringa]!="" and a[stringa][0]=='E':
                
                   dato=a[stringa].split('\t')
                   values=(dato[0],dato[2])
                   cursor.execute(sql2,values)
            cont+=1
                   
    db.commit()  
    return cont
                 
