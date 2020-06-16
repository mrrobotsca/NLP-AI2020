# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 14:14:47 2019

@author: DK0086
"""
import odema as od
import numpy as np
from datetime import datetime
import pandas as pd
import geopy.distance
import math
import os
import time
import sys
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="Dash")


#######################################################################
#  1em Partie :
# Connection a Database des ordre D3 et traitement des donnees

tec=pd.read_csv(r'Territoire_vs_technicien.csv', sep=";",encoding = "ISO-8859-1" )
sql = "SELECT MVW_BW_AVIS.AVIS, MVW_BW_AVIS.DESCRIPTION, MVW_BW_AVIS.TYP, MVW_BW_AVIS.DATE_AVIS,  \
        MVW_BW_AVIS.ANNEE_DATE_AVIS, MVW_BW_AVIS.MOIS_DATE_AVIS, MVW_BW_AVIS.STATSYS, MVW_BW_AVIS.STAT_UTIL,  \
        MVW_BW_AVIS.ORDRE, MVW_BW_ORDRES.DATE_CREATION, MVW_BW_AVIS.POSTETECHNIQUE, MVW_BW_AVIS.CODAGE, \
        MVW_BW_AVIS.DIV, MVW_BW_AVIS.RESPONSABLE FROM ODEMA.MVW_BW_AVIS MVW_BW_AVIS LEFT OUTER JOIN ODEMA.MVW_BW_ORDRES MVW_BW_ORDRES ON (MVW_BW_AVIS.ORDRE = MVW_BW_ORDRES.ORDRE)"
div=tec.loc[:,'Division'].astype(str)
divv=[]
for row in div:
    a=row
    if len(a)==3:
        a='0'+a
        divv.append(a)
    else:
        divv.append(a)

localisation= tec.loc[:,'Désignation']
lon=[]
lat=[]
for row in localisation:
    location = geolocator.geocode(row,timeout=15)
    print(location.address)
    lat.append(location.latitude)
    lon.append(location.longitude)

tec['longitude']=lon
tec['latitude']=lat
tec['Division']=divv
tec.index = tec['Division']

df = od.read_odema(sql=sql)

test = df[df['DIV'].isin(divv)].copy()
test['IPOT'] = test['STAT_UTIL'].fillna('').str.contains('IPOT')
test['ANOI'] = test['STAT_UTIL'].fillna('').str.contains('ANOI')
test['AINF'] = test['STAT_UTIL'].fillna('').str.contains('AINF')
test["TYP"] = np.where(test['TYP'] == "D3",
                       np.where(test['IPOT'],
                                "D3-IPOT",
                                np.where(test['AINF'],
                                         'D3-AINF',
                                         np.where(test['ANOI'],
                                                  'D3-ANOI',
                                                  "D3-AUTRE")
                                                  )
                               ),
                       test['TYP'])

R5=['R01','R02','R03','R04','R05']
R10=['R06','R07','R08','R09','R10']
test['R5_et_moins']=test['CODAGE'].isin(R5)
test['R6_et_plus']=test['CODAGE'].isin(R10)
test = test[test['CODAGE'].isin(R5) | test['CODAGE'].isin(R10)]
test = test[test['TYP'].isin(['D2','D4','D9','D3']) | test['TYP'].str.contains('D3')]
test['TYPE_CODE']=test['TYP']
test["Technicien"] = test["DIV"].map(tec["Techniciens"]).fillna("non-assigne")
test["Désignation"] = test["DIV"].map(tec["Désignation"]).fillna("non-assigne")
test["Territoires"] = test["DIV"].map(tec["Territoires"]).fillna("non-assigne")
test["longitude"] = test["DIV"].map(tec["latitude"]).fillna("non-assigne")
test["latitude"] = test["DIV"].map(tec["longitude"]).fillna("non-assigne")


testcopy = test.copy()


df_ordres = testcopy[testcopy['ORDRE'].notnull()].copy()
testcopy["date"] = testcopy["DATE_AVIS"]
df_ordres["date"] = df_ordres["DATE_CREATION"]
testcopy=testcopy[(testcopy.date.dt.year>=2012)& (testcopy.date.dt.year<=2020)]
df_ordres=df_ordres[(df_ordres.date.dt.year>=2012)& (df_ordres.date.dt.year<=2020)]
testcopy["TYP"] = testcopy["TYP"] + "-lances"
df_ordres["TYP"] = df_ordres["TYP"] + "-confirmes"
testcopy = testcopy.append(df_ordres)

del testcopy["DATE_AVIS"], testcopy["DATE_CREATION"], testcopy['AINF'], testcopy['ANOI'], testcopy['IPOT'], testcopy['R5_et_moins'], testcopy['R6_et_plus']



test["TYP"] = np.where(test['R5_et_moins'],test['TYP']+"-R5",test['TYP']+"-R10")
df_ordres = test[test['ORDRE'].notnull()].copy()
test["date"] = test["DATE_AVIS"]
df_ordres["date"] = df_ordres["DATE_CREATION"]
test=test[(test.date.dt.year>=2012)& (test.date.dt.year<=2020)]
df_ordres=df_ordres[(df_ordres.date.dt.year>=2012)& (df_ordres.date.dt.year<=2020)]
test["TYP"] = test["TYP"] + "-lances"
df_ordres["TYP"] = df_ordres["TYP"] + "-confirmes"
test = test.append(df_ordres)






del test["DATE_AVIS"], test["DATE_CREATION"],test['AINF'], test['ANOI'], test['IPOT'], test['R5_et_moins'], test['R6_et_plus']


test = test.append(testcopy)


#######################################################################
#  2em Partie :
# Connection a Database des ordre 443 et traitement des donnees


sql_req_443 =  \
   "SELECT MVW_BW_ORDRES.TYPE, \
       MVW_BW_ORDRES.CODE_NATURE, \
       MVW_BW_ORDRES.ORDRE, \
       MVW_BW_OPERATIONS_SM_PM.OPERATION_SM_PM, \
       MVW_BW_ORDRES.DESIGNATION, \
       MVW_BW_OPERATIONS_SM_PM.DESIGNATION_OPERATION_SM_PM, \
       MVW_BW_OPERATIONS_SM_PM.STATUTS_UTIL_COMPLET_SM_PM, \
       MVW_BW_OPERATIONS_SM_PM.STATUT_OP_COMPLET_SM_PM, \
       MVW_BW_OPERATIONS_SM_PM.DATE_STATUT_CONF_SM_PM, \
       MVW_BW_OPERATIONS_SM_PM.DATE_STATUT_LANC_SM_PM, \
       MVW_BW_ORDRES.DIVISION_GRPE_GESTION, \
       MVW_BW_ORDRES.DIVISION_POSTE_RESP, \
       MVW_BW_ORDRES.POSTERESP \
   FROM ODEMA.MVW_BW_ORDRES \
       INNER JOIN ODEMA.MVW_BW_OPERATIONS_SM_PM \
           ON (MVW_BW_ORDRES.ORDRE = MVW_BW_OPERATIONS_SM_PM.ORDRE_SM_PM) \
   WHERE(MVW_BW_ORDRES.CODE_NATURE = '443')"


geolocator = Nominatim(user_agent="Dash")
df443 = od.read_odema(sql=sql_req_443)


df=pd.read_csv(r'Territoire_vs_technicien.csv', sep=";",encoding = "ISO-8859-1" )

div=df.loc[:,'Division'].astype(str)
divv=[]
for row in div:
    a=row
    if len(a)==3:
        a='0'+a
        divv.append(a)
    else:
        divv.append(a)
df['Division']=divv
localisation= df.loc[:,'Désignation']
lon=[]
lat=[]
for row in localisation:
    location = geolocator.geocode(row,timeout=15)
    print(location.address)
    lat.append(location.latitude)
    lon.append(location.longitude)

df['longitude']=lon
df['latitude']=lat
df.index = df['Division']

df443['chk'] = df443['DESIGNATION_OPERATION_SM_PM'].fillna('').str.lower().str.replace('é','e')
df443['TYPE_CODE'] = df443['TYPE'] + '-' + df443['CODE_NATURE']
df443['TYPE_CODE'] = np.where(df443['chk'].fillna("").str.contains('diagnostic')
                           ,df443['TYPE_CODE'] + '-' + 'Diagnostic'
                           ,df443['TYPE_CODE'] + '-' + 'Autre'
                                               )

closed = df443[df443['DATE_STATUT_CONF_SM_PM'].notnull()].copy()
df443 = df443[df443['DATE_STATUT_LANC_SM_PM'].notnull()]     #pas supposé d'avoir aucun null mais quand même, juste pour être sûr
closed['date'] = closed['DATE_STATUT_CONF_SM_PM']
df443['date'] = df443['DATE_STATUT_LANC_SM_PM']
lst_champs = ['TYPE_CODE','TYPE','CODE_NATURE','ORDRE','DESIGNATION','OPERATION_SM_PM','DESIGNATION_OPERATION_SM_PM','date', 'DIVISION_GRPE_GESTION','DIVISION_POSTE_RESP']
closed = closed[lst_champs]
df443 = df443[lst_champs]
df443['TYP'] = df443['TYPE_CODE'] + '-lances'
closed['TYP'] = closed['TYPE_CODE'] + '-confirmes'
df443 = df443.append(closed)
df443['DIV'] = df443['DIVISION_POSTE_RESP']
df443["Technicien"] = df443["DIV"].map(df["Techniciens"]).fillna("non-assigne")
df443["Désignation"] = df443["DIV"].map(df["Désignation"]).fillna("non-assigne")
df443["Territoires"] = df443["DIV"].map(df["Territoires"]).fillna("non-assigne")
df443["longitude"] = df443["DIV"].map(df["latitude"]).fillna("non-assigne")
df443["latitude"] = df443["DIV"].map(df["longitude"]).fillna("non-assigne")
df443["TYP_STATUS"] = df443["TYP"]
df443['433'] = df443['CODE_NATURE'].fillna('').str.contains('433')
del closed


#tot=pd.concat([df443, test], ignore_index=True)

#tot.to_csv('tot.csv',sep=";")


