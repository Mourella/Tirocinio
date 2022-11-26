# -*- coding: utf-8 -*-
"""
Created on Wed Nov  9 11:06:46 2022

@author: Davide Morelli
"""


import mysql.connector
import os
import datetime

geneExpression = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="geneexpression"
        )


geCursor = geneExpression.cursor()



      
def label(site):
    if (site=="Kidney"): return 1
    elif (site=="Breast"): return 2
    elif (site=="Brain"): return 3
    elif (site=="Uterus"):return 4
    elif (site=="Lung"): return 5
    elif (site=="Cervix"): return 6
    

##FUNZIONE SERVITA PER ESTRARMI TUTTI I CASI
def scriviCasi():
    os.chdir("E:\TirocinioDati\CSV")
    with open ("FileCasi.txt",'w') as f:
      geCursor.execute("select distinct Case_ID,Site from geneexpression.gene_expression;")
      myresult =geCursor.fetchall();
      for tupla in myresult:
          print(tupla,len(myresult))
          f.write(tupla[0]+","+tupla[1]+'\n')
          

##T.Gene_ID,T1.Gene_ID,T1.Gene_name_TCGA,T.Gene_name) 
def listaGeni():
                             #Gene_ID
    geCursor.execute("select Gene_name from  hpm.HPMTCGAGeniComuni;") #SCEGLI LE COLONNE
    myresult = [x[0] for x in geCursor.fetchall()]
    myresult.append("Label")
    return myresult



 
def livelloHPM(sito):       #Gene_id
    geCursor.execute("select Gene_name,FPKM,Site from hpm.hpmgeni where(Site='"+sito+"' and Gene_ID in (select Gene_ID from hpm.HPMTCGAGeniComuni));")
    myresult=[(x[0],x[1]) for x in geCursor.fetchall()]
    return myresult


def prova():
    geCursor.execute("select max(FPKM) from geneexpression.gene_expression where(Gene_ID in (select Gene_ID from hpm.HPMTCGAGeniComuni));")
    myresult=geCursor.fetchall()
    return myresult

def livelliTCGA(caso):
                             #Gene_ID
    geCursor.execute("select Gene_name_TCGA,FPKM,Site from geneexpression.gene_expression where(Case_ID='"+caso+"' and Gene_ID in (select Gene_ID from hpm.HPMTCGAGeniComuni));")
   # geCursor.execute("select Gene_ID,FPKM from geneexpression.gene_expression where(Case_ID='"+caso+"');")

    myresult =geCursor.fetchall()
    
    return myresult


 
import psutil    

'''
Setto contatori, intestazione e TIME
creo il file Csv da processare
apro i casi di TCGA
per ogni caso faccio una query e mi prendo grazie ad essa solo i geni in comune con HPM
faccio un dizionario per cui ad ogni gene corrisponde una concentrazione.
Faccio la normalizzazione voluta dal prof e da qui creo 3 liste (a cui attacco la label ad ognuna)
e le scrivo. 
Faccio ciò per ogni caso
Stesso vale per HPM'''

def process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss

def scriviCSV() :
    mem_before=process_memory()
    M=25.054519831143633
    M1=31.282264393579723
    #MEDIA
  #  M=12.527259915571817
   # M1=15.641132196789862
   # M=125274.0 #VALORE MASSIMO TCGA
    #M1=12939.4 #valore MASSIMO HPM
  #  UNO=0
    l1,l2,contatore=0,0,0
    intestazione=[]
    Start=datetime.datetime.now()
    os.chdir("E:\TirocinioDati\CSV")
    newFile=open("prova.csv",'w')
    with open ("FileCasi.txt") as f:
       intestazione=listaGeni()
       newFile.write(",".join(intestazione)+"\n")
       ns=f.read().split('\n') ###per fare il test riduco le righe
       contatore=0
       
       for caso in ns:
           caso,cancro=caso.split(',')
           diz=dict()  #nuovo dizionario
           now=datetime.datetime.now()
           tupleCaso=livelliTCGA(caso)
         
           #faccio dizionario
           for tupla in tupleCaso:
               diz[tupla[0]]=tupla[1]
           
           #per gene in intestazione lo cerco nel dizionario e lo metto dentro
           riga=list()
           for gene in intestazione[:-1]:
               if gene in diz:
                   riga.append(diz[gene])   
               else:
                   riga.append(0)
                
           
         # NORMALIZZAZIONE: LN(a, i) = if (L(i) /M) <= a) then 0 else 1
           for a in [0.4,0.5,0.6]:#per ogni valore del tronci
               normalizzata=list(map(lambda x: 0 if (x/M)<=a else 1,riga))  #normalizza
             #  UNO+=normalizzata.count(1)
               normalizzata.append(label(cancro)) #metto la label 
               newFile.write(",".join(list(map(str,normalizzata)))+"\n") #scrivi riga x di 3
              
              
           ##controlli per contatori
               if (label(cancro))==1:l1+=1
               elif (label(cancro))==2:l2+=1
               contatore+=1
               print(str(contatore),datetime.datetime.now()-now,caso,cancro)
           
           
    #HPM

    riga=list()
    with open("CasiHpm.txt") as file:
       casi=file.read().split('\n')
       contatoreH=0
       for caso in casi:
          
           diz=dict()
           tupleCaso=livelloHPM(caso)
           contatoreH+=1
           for tupla in tupleCaso:
               diz[tupla[0]]=tupla[1]
               
           riga=list()
           
           for gene in intestazione[:-1]:
               if gene in diz:
                   riga.append(diz[gene])
               else:
                   riga.append(0.0)

           for a in [0.4,0.5,0.6]:#per ogni valore del tronci
               normalizzata=list(map(lambda x: 0 if (x/M1)<=a else 1,riga))  #normalizza
              # UNO+=normalizzata.count(1)
               normalizzata.append(0)#metto label
               newFile.write(",".join(list(map(str,normalizzata)))+"\n") #scrivi riga x di 3
               print(contatoreH)
               contatoreH+=1
           
    newFile.close()
    mem_after=process_memory()
    return str(datetime.datetime.now()-Start),l1,l2,contatoreH,"MEMORIA USATA: "+str(round((mem_after-mem_before)/1000000,0))+" MB"#,UNO

          