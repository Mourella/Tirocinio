# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 11:15:33 2022

@author: Davide Morelli
"""
import requests
import datetime
import os



    
''' con questo script prendo i nomi e cerco i suoi sinonimi su ensmble
  ext = "/xrefs/name/human/"+x+"?"'''

def ispeziona(file):
    print("INIZIO SUI NOMI")
    fileNomeGeni=open("fileNomeGeni1.txt",'w',encoding="utf-8")
    cont=0
    start=datetime.datetime.now()
    
   
    with open(file,encoding='utf-8') as f:
        a=f.read().split('\n')
        
        for stringa in range(7,len(a)):
            
                
            if a[stringa]!="" and a[stringa][0]=='E':
                
                dato=a[stringa].split('\t')
                print(cont+8,"DATO "+dato[1])
                nome=nomiSinonimi(dato[1])
                
                if nome!=None: 
                    
                    fileNomeGeni.write(dato[1]+','+nome+'\n')
                else:
                    fileNomeGeni.write(dato[1]+'\n')
      
            cont+=1
      
    fileNomeGeni.close()
    return datetime.datetime.now()-start#"SALVATO IN FILEMODIFICATI"
                
               
    
      
def nomiSinonimi(x): 
   
    server = "https://rest.ensembl.org"
    ext = "/xrefs/name/human/"+x+"?"
    stringa=""
    insieme=set()
    r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
     
    if r.ok:
        decoded = r.json()
        for db in decoded:
            if db['synonyms']!=[]: 
                insieme= insieme|set(db['synonyms'])
                
        if len(insieme)==0: return None
        for sinonimo in insieme:
            stringa+=sinonimo+","
        stringa+=str(len(insieme))
    return stringa
  
    



##DA NOMI A CODICE ENS
def codiceENSG(ListaProteineOGeni):
    os.chdir("E:\TirocinioDati\DataHumanProteome\Kidney_GeneLevelExpression")
    contatore,riga=0,0
    noTrovati=[]
    server = "https://rest.ensembl.org"
    with open("TCPA_proteineENS.txt",'w',encoding='utf-8') as f:
      for nome in ListaProteineOGeni:
          
            print(riga)
            riga+=1
            ext = "/xrefs/symbol/homo_sapiens/"+nome+"?"
         
            r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
         
            if not r.ok:
                r.raise_for_status()
                sys.exit()
         
            decoded = r.json()
          
            if len(repr(decoded))<3: 
                contatore+=1
                noTrovati.append(nome)
                #<3 è vuota
               
            else :
                ##print (decoded[0]['id'])
                f.write(decoded[0]['id']+","+nome+'\n')
    return contatore,noTrovati
             

def lastVersion(gene):
    
 
    server = "https://rest.ensembl.org"
    ext = "/archive/id/"+gene+"?"
 
    r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
 
    if not r.ok:
        r.raise_for_status()
        sys.exit()
 
    decoded = r.json()
    return repr(decoded['latest'])
        
##serve a creare un nuovo file con geni geni contenenti la versione
def updateVersionFileGene(file):
    
    fileGeni=open("N"+file,'w')
    with open("HPM_geniEns.txt",encoding='utf-8') as f:    
          a=f.read().split('\n')
          for riga in range(len(a)):
              print(riga)
              riga=a[riga].split(",")
              fileGeni.write(lastVersion(riga[0])+","+riga[1]+"\n")

              
    

  
            
        
        
        