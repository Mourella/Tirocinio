# -*- coding: utf-8 -*-
"""
Created on Tue May 24 22:55:46 2022

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
        database="proteinexpression"
        )

cursor=db.cursor()
sql="INSERT INTO agid_gene_id VALUES (%s,%s)"
sql1="INSERT INTO protein_expression VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"


def insertAGID_GeneID():
    cont=0
    with open("AGIDGeneID.txt",encoding='utf-8') as f:
        a=f.read().split('\n')
        for stringa in range(len(a)):
            if a[stringa]!="":
                dato=a[stringa].split('\t')
                AGID=dato[0]
                for gene in dato[2].split("/"):
                    cont+=1
                    
                    cursor.execute(sql,[AGID]+[gene])
                print(cont)
    db.commit()  
    print("RECORD INSERITI: ",cont) 
    return cont
                


def  fileAGIDGENE():
    AGIDFile=open("AGIDGeneID.txt",'w')
    with open("TCGA_antibodies_descriptions.gencode.v36.tsv",encoding='utf-8') as f:
        c=f.read().split('\n')
        for stringa in range(1,len(c)):
            if c[stringa]!="":
                dato=c[stringa].split('\t')
                AGIDFile.write(dato[0]+'\t'+dato[2]+'\t'+dato[7]+'\n')
                
                
def insertProteinExpression(tipoSito):
   ## os.mkdir("E:\TirocinioDati\FileCaricati_Protein Expression Quantification")
    os.mkdir(os.path.join("E:\TirocinioDati\FileCaricati_Protein Expression Quantification",tipoSito))
    os.chdir("E:\TirocinioDati\FileFinaliModificati_Protein Expression Quantification") #CAMBIA DIRECTORY
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
        shutil.move(file,os.path.join("E:\TirocinioDati\FileCaricati_Protein Expression Quantification",tipoSito))
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
           
                
            if a[stringa]!="" and a[stringa][0]=='A':
                
                #rende il tutto una lista dal quale selezionare i valori
                dato=a[stringa].split('\t')
               
                
                cursor.execute(sql1,lista+dato)
            
                cont+=1
                
              
    db.commit()  
    print("RECORD INSERITI: ",cont) 
    return cont                
                
