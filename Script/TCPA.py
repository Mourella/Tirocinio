# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 16:08:53 2022

@author: Davide Morelli
"""

import os
import mysql.connector
db= mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="tcpa"
        )

cursor=db.cursor()
sql="INSERT INTO protein_expression VALUES (%s,%s,%s,%s,%s,%s)"
def ordinaFileTCPA(file):
   cont=0
   
   os.chdir("E:\TirocinioDati\TCPA\Kidney")
   value_protein=open("N"+file,"w")
   with open(file,encoding='utf-8') as f:
         a=f.read().split('\n')
         intestazione=a[0].split(",")[4:]
     
         for riga in range(1,len(a)): #scorro le righe
            cont+=1
            lista=a[riga].split(',') 
            lista1=lista[4:]
            for valore in range(len(lista1)): #lista tolti le descrizioni
                value_protein.write(lista[0]+","+lista[1]+","+lista[2]+","+lista[3]+","+intestazione[valore]+","+lista1[valore]+"\n")
            
   return cont          

def insertProtein_expression(file):
    os.chdir("E:\TirocinioDati\TCPA\Kidney")
    with open(file,encoding='utf-8') as f:
        a=f.read().split('\n')
        cont=0
        for stringa in range(len(a)):
            if a[stringa]!="":
                print(stringa,a[stringa])
                cursor.execute(sql,a[stringa].split(","))
                cont+=1
                
              
    db.commit()  
    print("RECORD INSERITI: ",cont) 
    return cont