# -*- coding: utf-8 -*-
"""
Created on Wed Nov  9 17:15:37 2022

@author: Davide Morelli
"""
import datetime
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import warnings
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

import pydotplus
import numpy
import psutil

    
from sklearn import tree
import os
warnings.filterwarnings('ignore')




 
# inner psutil function
def process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss


#Funzione di start  
def start(pathFile,criterio,split,s_leaf,ID):
    ID=criterio[0]+str(ID)
    print("Tree "+criterio+" "+str(split)+" "+str(s_leaf))
    mem_before=process_memory()
    Start=datetime.datetime.now()
  
    X,y,file=readFile(pathFile) #legge file
   
    K,N,L,P,H=train_test(X,y,os.path.basename(pathFile),criterio,split,s_leaf)
   
    H,S,StdDev=results(K,N,L,P,H)
    
    mem_after=process_memory()

    print("ID: ",ID,"H: ",round(H,3),"ValoreMedio: ",round(S,3),"DeviazioneStandard: ",round(StdDev,3))
    print("TEMPO TRASCORSO:" + str(datetime.datetime.now()-Start),"MEMORIA USATA: "+str(round((mem_after-mem_before)/1000000,0))+" MB")
    print()


''' Funzione che legge il file e restituisce:
    - ultima colonna y
    - tutte le righe con il loro contenuto X
    INFO COLONNE
    file.head()     
    file.info()               
    file.describe()
'''
def readFile(pathFile):
    os.chdir("E:\TirocinioDati\CSV")
    file = pd.read_csv(pathFile)
   
    X = file.iloc[:,:-1]  #prende tutte le colonne e le righe
    y = file.iloc[:,-1]  #prende ultima colonna ovvero il label

    return X,y,file
 

'''Questa funzione costruisce un albero decisionale per prevedere
il tessuto malato dalle concetrazioni'''
def train_test(X,y,nameTree,criterio,split,s_leaf):    
     K=0 #numero di foglie
     N=6637 #numero di samples della root
     L=list() #numero di samples per ogni foglia
     P=list() #probabilità che un samples cada nella foglia i
     H=list() #entropia o gini della foglia i
     
     #divide la matrice in sottoinsiemi di test.impara 
     X_train, X_test, y_train, y_test=train_test_split(X, y,random_state=2)
   
     
    
     clf = DecisionTreeClassifier(random_state=2,criterion=criterio,min_samples_split=split,min_samples_leaf=s_leaf)# criterion="entropy",splitter="random"min_samples_split=300,min_samples_leaf=100,
     clf.fit(X_train, y_train)
     leaf=clf.apply(X_train)
    
     
    
     #PER CAMBIARE I PARAMETRI DEVI LAVORARE SU CLF
     
     #Cambio dir e stampo un png con l'albero
     os.chdir("E:\TirocinioDati\CSV\TreePNG")   
     dot_data = tree.export_graphviz(clf,
                          out_file=None, #se None il risultato è una stringa
                          feature_names=list(X.columns),
                          class_names=["Healthy","Kidney","Breast","Brain","Uterus","Lung","Cervix"],
                          filled=True,
                          node_ids=True, #ID su ogni nodo,!!!
                          rounded=True,  
                          special_characters=True, max_depth=None)  
     
     graph = pydotplus.graph_from_dot_data(dot_data)  
     nodes = graph.get_node_list()
     colors =  ('red','palegreen','salmon','orange','lightblue', 'yellow', 'forestgreen','navajowhite','whitesmoke')
     
     for node in nodes:
         
        if node.get_name() not in ('node', 'edge'):
            
            
           # print(clf.tree_.feature[int(node.get_name())])
            values = clf.tree_.value[int(node.get_name())][0]
          
            #color only nodes where only one class is present
            if max(values) == sum(values):   
                
                K+=1
                L.append(max(values))
                P.append(max(values)/N)
                H.append(clf.tree_.impurity[int(node.get_name())]) 
                node.set_fillcolor(colors[numpy.argmax(values)])
                
            #le foglie non utili le colora
            elif int(node.get_name()) in leaf:
                K+=1
                L.append(max(values))
                P.append(max(values)/N)
                H.append(clf.tree_.impurity[int(node.get_name())]) 
               
                node.set_fillcolor(colors[-2])
            # I nodi non foglia li colora di grigio
            else:
                node.set_fillcolor(colors[-1])
     graph.write_png(criterio+str(split)+str(s_leaf)+".png")
     
     return K,N,L,P,H
   
'''  calcola:
H: entropia o gini attesa
S: valore medio dei samples
Var: varianza
StdDev:deviazione Standard    
RITORNA UNA TRIPLA'''
import math
def results(K,N,L,P,Hi):
    #entropia/gini atteso H = p(1)*H(1) + p(2)*H(2) + ...... p(K)*H(K) 
    H=sum(list(map(lambda x,y: x*y ,P,Hi)))
    
    #Definiamo il valore medio S dei samples come: S = (L(1) + L(2) + ...... L(K))/K
    S=sum(L)/K
    
    #Definiamo la varianza Var dei samples come: Var = ((L(1) - S)^2 +  (L(2) - S)^2 + ...  (L(K) - S)^2)/K
    Var=sum(list(map(lambda x: (x-S)**2 ,L)))/K
    
    #deviazione Standard
    StdDev=math.sqrt(Var)
    
    return (H,S,StdDev)
    
    
    
'''
 def genera():
    ID=1
    start("Media.csv","gini",100,60,ID)
    ID+=1
    start("Media.csv","gini",100,100,ID)
    ID+=1
    start("Media.csv","gini",150,200,ID)
    ID+=1
    start("Media.csv","gini",150,300,ID)
    ID+=1
    start("Media.csv","gini",100,300,ID)
    ID+=1
    start("Media.csv","entropy",100,60,ID)
    ID+=1
    start("Media.csv","entropy",100,100,ID)
    ID+=1
    start("Media.csv","entropy",150,200,ID)
    ID+=1
    start("Media.csv","entropy",150,300,ID)
    ID+=1
    start("Media.csv","entropy",100,300,ID)
    '''    
     
     

    
    
    
    
    
    
    
    