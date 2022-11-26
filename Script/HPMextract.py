# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 18:00:22 2022

@author: Davide Morelli
"""
import os
import mysql.connector
db= mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="hpm"
        )

cursor=db.cursor()
sql="INSERT INTO gene_expression VALUES (%s,%s,%s)"
sql3="INSERT INTO gene_synonyms VALUES (%s,%s)"
sql1="INSERT INTO protein_expression VALUES (%s,%s,%s,%s)"
sql2="INSERT INTO peptide_protein_gene VALUES (%s,%s,%s,%s,%s)"
.
#COLONNA : colonna inerente alla tipo di cancro
#tipoSito: cancro
#file, il file csv trasformato in txt da cui prendere i dati
#Tipo di dato, GeneLevelEsprezzion, proteine...
def estraiLevel(colonna,tipoSito,file,tipoDato):
    os.chdir("E:\TirocinioDati\DataHumanProteome")
    path=os.path.join("E:\TirocinioDati\DataHumanProteome",tipoSito+"_"+tipoDato)
    os.mkdir(path)
    levelFile=open(os.path.join(path,tipoSito+"_"+tipoDato+".txt"),'w')
    with open(file) as f:
          a=f.read().split('\n')
   
          for riga in range(len(a)-1):
             lista=a[riga].split(',')
             if lista!=[]:
                 if riga<len(a)-2:
                     
                     ##PER LE PROTEINE HAI AGGIUNTO LISTA[1]
                #     levelFile.write(lista[0]+'\t'+lista[1]+'\t'+lista[colonna]+'\t'+tipoSito+'\n')
                # else :levelFile.write(lista[0]+'\t'+lista[1]+'\t'+lista[colonna]+'\t'+tipoSito)
                     levelFile.write(lista[0]+'\t'+lista[colonna]+'\t'+tipoSito+'\n')
                 else :levelFile.write(lista[0]+'\t'+lista[colonna]+'\t'+tipoSito)
             
                
 #Insert geni in HPM             
def insertGeneExpressionHPM(file):
     #os.chdir("E:\TirocinioDati\DataHumanProteome")
     cont=0
     with open(file,encoding='utf-8') as f:
          a=f.read().split('\n')
          for stringa in range(1,len(a)):
              if a[stringa]!="":
                  dato=a[stringa].split('\t')
               
                  values=(dato[0],dato[2],dato[1])
                  cursor.execute(sql,values)
                  cont+=1
                  
                       
     db.commit()  
     print("RECORD INSERITI: ",cont) 
     return cont
 
#Insert sinonimi
def insertGeneSynonyms(file):
     os.chdir("E:\TirocinioDati\DataHumanProteome\Kidney_GeneLevelExpression")
     cont=0
     with open(file,encoding='utf-8') as f:
          a=f.read().split('\n')
          for stringa in range(len(a)):
              if a[stringa]!="":
                  dato=a[stringa].split(',')
               
                  values=(dato[0],dato[1])
                  cursor.execute(sql3,values)
                  cont+=1
                  
                       
     db.commit()  
     print("RECORD INSERITI: ",cont) 
     return cont
 
#Insert proteine          
def insertProteinExpressionHPM(file):
     cont=0
     with open(file,encoding='utf-8') as f:
          a=f.read().split('\n')
          
          for stringa in range(1,len(a)):
              if a[stringa]!="":
                 dato=a[stringa].split('\t')
                 print(dato,cont)
                 values=(dato[0],dato[1],dato[3],dato[2])
                 cursor.execute(sql1,values)
                 cont+=1
                  
                       
     db.commit()  
     print("RECORD INSERITI: ",cont) 
     return cont
    

#Ordina il file scaricato
def leggi(file):
     fileProtNomeGeni=open("proteineNomi.txt",'w')
     with open(file,encoding='utf-8') as f:
          scritta=" "
          a=f.read().split('\n')
          for stringa in range(1,len(a)-1):
              dato=a[stringa].split(",")  #splitto sulla ,
              #salvo ogni parte della string in variabili così da poter
              #lavorare su quelle che hanno più sinonimi nella stessa stringa
              peptide=dato[0]   
              lunghezza=dato[1]
              proteina=dato[2].split('\t') #splitto le proteine per gli spaz
              nomi=dato[3]
              for prot in proteina: #per ogni sinonimo proteina splitta e prendi 2 sinonimi in particolare 
                  #accession e NP_...
               # prot=prot.split('|')[1],prot.split('|')[3] OGNI RIGA NP e 0922 separati
                prot1=prot.split('|')[1]
                prot2=prot.split('|')[3]
                
                for nome in nomi.split('\t'): #divido i sinonimi del nome
                       #scrivo sinonino proteina sinonimo nome per ogni nome e proteina
                      # print(peptide,lunghezza,prote,nome)
                      scrivo=peptide+'\t'+lunghezza+'\t'+prot1+'\t'+prot2 +'\t'+nome+'\n'
                      if stringa<len(a)-2 and (scritta!=scrivo): #evito i doppioni
                          fileProtNomeGeni.write(peptide+'\t'+lunghezza+'\t'+prot1+'\t'+prot2 +'\t'+nome+'\n')
                          scritta=peptide+'\t'+lunghezza+'\t'+prot1+'\t'+prot2 +'\t'+nome+'\n'
                      else:fileProtNomeGeni.write(peptide+'\t'+lunghezza+'\t'+prot1+'\t'+prot2 +'\t'+nome)
            
              
#Insert Peptide        
def insertPeptide_protein_genes(file):
     cont=0
     with open(file,encoding='utf-8') as f:
          a=f.read().split('\n')
          
          for stringa in range(1,len(a)):
              if a[stringa]!="":
                 dato=a[stringa].split('\t')
                 if len(dato)<6:
                     cursor.execute(sql2,dato)
                     cont+=1
                 
                  
                       
     db.commit()  
     print("RECORD INSERITI: ",cont) 
     return cont         
             
    
    
    
    
    
    
    
    
    
    