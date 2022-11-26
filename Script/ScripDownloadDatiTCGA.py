# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 11:55:32 2022

@author: Davide Morelli
"""

import patoolib
import requests
import json
import re
import os
import shutil
import datetime
import psutil

def process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss

 
tipoDato="Gene Expression Quantification"#"Gene Level Copy Number" Protein Expression Quantification
tipoSito="Cervix"#"Breast" Kidney Brain Cervix Lung Uterus
os.chdir("E:\TirocinioDati")
def download():
    mem_before=process_memory()
    Start=datetime.datetime.now()
    os.mkdir("E:\TirocinioDati\FileEstratti_"+tipoDato) #creoCartella
    
    Casi=open("Casi_"+tipoDato+".txt",'w')
    files_endpt = "https://api.gdc.cancer.gov/files"
    
    filters = {
        "op": "and",
        "content":[
            {
            "op": "in",
            "content":{
                "field": "cases.project.primary_site",
                "value": [tipoSito]  #filtro sul breast cancer
                #CAMBIALO ANCHE NELL'INSERT, ADESSO!
                }
            },
            
            {
            "op": "in",
            "content":{
                "field": "cases.project.project_id",
                "value": ["TCGA-CESC"]  #filtro sul tipo di progetto TCGA CERVIX "TCGA-CESC" LUNG "TCGA-LUAD" Uterus "TCGA-UCEC"
                }
            },
            
             {
            "op": "=",
            "content":{
                "field": "files.data_type",
                "value": [tipoDato] #in caso di GeneExpression mettilo #filtro su gene quantification
                }
            },
            
            
            {
          "op": "in",
           "content":{
                "field": "files.experimental_strategy",
                "value": ["RNA-Seq"] #strategy
              }
            },
             {
            "op": "in",
            "content":{
                "field": "files.access",
                "value": ["open"]  #visibilità
                }
            },
        ]
    }
    
    # Here a GET is used, so the filter parameters should be passed as a JSON string.
    
    params = {
        "filters": json.dumps(filters),
        #Puoi aggiungere altri campi che danno più info relative al file
        "fields": "file_id,cases.case_id,cases.samples.submitter_id,file_name,cases.samples.sample_type", 
        "format": "JSON",
        "size": "300" #CERVIX 300  # Lung 500 Uterus 500
        
        }
    
    response = requests.get(files_endpt, params = params)
    
    file_uuid_list = []
    cas1=""
    cas2=""
    # This step populates the download list with the file_ids from the previous query
    for file_entry in json.loads(response.content.decode("utf-8"))["data"]["hits"]:
        
       # print(file_entry['cases'][0]['case_id'],file_entry['cases'][0]['samples'][0]['submitter_id'],file_entry['cases'][0]['samples'][1]['sample_type'])
        
        
        file_uuid_list.append(file_entry["file_id"])
        cas1=file_entry['cases'][0]['case_id']
        cas2=file_entry['cases'][0]['samples'][0]['submitter_id'] 
        #sample_type=file_entry['cases'][0]['samples'][1]['sample_type']
        sample_type=file_entry['cases'][0]['samples'][0]['sample_type']
       
        Casi.write(file_entry['file_name']+'\t'+cas1+'\t'+cas2+'\t'+sample_type+'\n')
            
   
        
    
    data_endpt = "https://api.gdc.cancer.gov/data"
    
    params = {"ids": file_uuid_list}

    response = requests.post(data_endpt, data = json.dumps(params), headers = {"Content-Type": "application/json"})
    
    response_head_cd = response.headers["Content-Disposition"]
    
    file_name = re.findall("filename=(.+)", response_head_cd)[0]
    
   
 
    with open(file_name, "wb") as output_file:
        output_file.write(response.content)
    Casi.close()
    
      
    print("FATTO")
    print("DECOMPRIMO....")
    decomprimi()
    print("DECOMPRIMO FILE ESTRATTI....")
    decomprimiFileEstratti()
    print("AGGIUNGO AI FILE I CASI....")
    AggiungiCaso()
    #rimuovo le dir che non servono
    shutil.rmtree("E:\TirocinioDati\FileEstratti_"+tipoDato, ignore_errors=True) 
    shutil.rmtree('E:\TirocinioDati\FileFinali_'+tipoDato, ignore_errors=True)
    print("CPU TIME: "+str(datetime.datetime.now()-Start))
    mem_after=process_memory()
    print("MEMORIA USATA: "+str(round((mem_after-mem_before)/1000000,0))+" MB")
    
#ESTRAE FILE DAL TAR.GZ e li mette dentro FILEESTRATTI    
def decomprimi():
    for file in os.listdir():
        if file.endswith('gz'):
            patoolib.extract_archive(file,outdir="FileEstratti_"+tipoDato) #metto la roba decompressa in FileEstratti_tipoDato
            os.remove(file) #rimuovo quello estratto
            
            
            
#apre le cartelle decompresse in FileEstratti e le decomprimeNuovamente         
def decomprimiFileEstratti():
     
    directory=os.getcwd()
    os.mkdir('E:\TirocinioDati\FileFinali_'+tipoDato) #creoCartella
    
    cerca(str(directory)+'\FileEstratti_'+tipoDato)
    
def cerca(directory): ##USATA IN DECOMPRIMIFILEESTRATTI
    for elemento in os.listdir(directory):
        
        path=os.path.join(directory,elemento)
        if os.path.isdir(path):
            cerca(path)
        else:
          
            shutil.move(path,'E:\TirocinioDati\FileFinali_'+tipoDato) #sposta i file nella cartella finale
        
        
#scorre i file nella cartella FileFinali con il fine di modificarli
def AggiungiCaso():
    os.mkdir("E:\TirocinioDati\FileFinaliModificati_"+tipoDato) #creo FileFinaliModificati
    os.chdir("E:\TirocinioDati\FileFinali_"+tipoDato) #mi risposto nella cartella file finali
    for file in os.listdir():
        
        cas1,cas2,sample_type=cercaCaso(file)
        if cas1==None: continue
        apri(file,cas1,cas2,sample_type)
    SCRIVICASIPERCSV(tipoSito)
    return "finito"
            
#Scrive dentro i file finali DENTRO AGGIUNGICASO
def apri(file,cas1,cas2,sample_type):
    
    os.chdir("E:\TirocinioDati\FileFinaliModificati_"+tipoDato)
    fileGeni=open(file,'w')
    os.chdir("E:\TirocinioDati\FileFinali_"+tipoDato)
    with open(file,encoding='utf-8') as f:
        a=f.read()
        fileGeni.write(cas1+'\t'+cas2+'\t'+sample_type+"\n")
        fileGeni.write(a)
    fileGeni.close()
    
    
                
def cercaCaso(file):
    os.chdir("E:\TirocinioDati")
    with open("Casi_"+tipoDato+".txt") as f:
        a=f.read().split('\n')
        for stringa in a:
            stringa=stringa.split('\t')
            if file==stringa[0]:
                return stringa[1],stringa[2],stringa[3]
    return None,None,None
        
#Questa funzione prende i casi appena scaricati e li metti in un file nuovo
#poi te manualmente prendi i casi in quel file e li attacchi su FileCasi.txt PER IL CSV
def SCRIVICASIPERCSV(tipoSito):
    w=open("E:\TirocinioDati\CSV\casi2.txt",'w')
    with open("E:\TirocinioDati\Casi_Gene Expression Quantification.txt",'r') as f:
        for riga in f.read().split('\n'):
            if len(riga)>1:
                w.write(riga.split('\t')[2]+','+tipoSito+'\n')
    w.close()
    
    
def scrivi():
    lista=list()
    os.chdir("E:\TirocinioDati\FileCaricati_Gene Expression Quantification\Lung")
    for file in os.listdir():
        with open (file,'r') as f:
            a=f.read().split('\n')
        
            lista.append(a[0].split('\t')[1])
    w=open("E:\TirocinioDati\CSV\casi2.txt",'w')
    for caso in lista:
         w.write(caso+','+"Lung"+'\n')
    w.close()
        
        
        
        
        