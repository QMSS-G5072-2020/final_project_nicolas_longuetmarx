import os
import numpy as np
import pandas as pd
import requests
import json
import codecs
import matplotlib.pyplot as plt
from legcop import LegiScan
import nltk 
import base64
from bs4 import BeautifulSoup
from collections import Counter
from matplotlib.ticker import FormatStrFormatter
import re

api_key = "c394a6d24d2362d97056c55d0c0d0c58"
legis = LegiScan(api_key)

### create text documents
def import_text(num, path):
    mylink2="https://api.legiscan.com/?key="+api_key+"&op=getBillText&id="+num
    r = requests.get(mylink2)
    json_response=r.json()
    json_response
    mydataframe=pd.DataFrame(json_response)
    mynew=mydataframe['text']
    mynew.to_frame()
    base64_message = mynew['doc']
    mydecoded = base64.b64decode(base64_message)
    html = mydecoded
    soup = BeautifulSoup(html, features="html.parser")
    #base64_bytes = base64_message.encode('ascii')
    #message_bytes = base64.b64decode(base64_bytes)
    #message = message_bytes.decode('ascii')
    raw = soup.get_text()  
    output_file = open(path+'\Output_'+num+'.txt', 'w', encoding="utf-8")
    output_file.write(raw)
    output_file.close()

# get the list of datasets available
def get_session_list(state):
    mylink2='https://api.legiscan.com/?key=c394a6d24d2362d97056c55d0c0d0c58&op=getDatasetList&state='+state
    r = requests.get(mylink2)
    json_response=r.json()
    json_response
    global mylist
    mylist=pd.DataFrame.from_dict(json_response['datasetlist'])
    #print(mylist)

    
def get_bill_list(session_num):
    mylink2="https://api.legiscan.com/?key=c394a6d24d2362d97056c55d0c0d0c58&op=getMasterList&id="+session_num
    r = requests.get(mylink2)
    json_response=r.json()
    mydata=pd.DataFrame.from_dict(json_response['masterlist'])
    mynewdata=mydata.loc[  'title' ,:]
    global mytitlelist
    mytitlelist=mynewdata.to_frame()
    mytitlelist=mytitlelist.dropna(subset=['title'])
    session_id=mydata.loc['session_id', 'session']
    session_name=mydata.loc['session_name', 'session']
    mydata.loc['session_id', :]=session_id
    mydata.loc['session_name', :]=session_name
    global mydatanew
    mydatanew=mydata.transpose()
    mydatanew=mydatanew.drop(['session'])
    mydatanew=mydatanew.dropna(subset=['title'])

mydico = {
    "environment" : ".environment|energy|tree|river|forest|animal|insect|fertilizer|dam|agricult|water|land|water|owner|control|site|air|solid|gas|tenant|oil|park|airport|coal|plant|prevent|underground|power|soil|portion|landlord|condition.",
    "courts" : ".court|judgment|attorney|case|appeal|civil|petition|sheriff|trial|circuit court|district court|such_person|complaint|counsel|brought|circuit|warrant|paid",
    "pensions": ".paid|benefit|rate|payment|equal|death|age|credit|pay|total|life|pension|premium|calendar year|loss|account|case|per cent|event|membership|excess|maximum.",
    "local_projects": ".development|local|project|budget|government|cost|grant|research|center|local government|data|transfer|governor|is the intent|develop|urban|review|biennium.",
    "procurement":".director|contract|work|review|civil|labor|contractor|attorney general|bureau|final|perform|audit|receipt|status|exempt|panel|government|firm|bid|prepared.",
    "elections":".district|town|petition|charter|special|ballot|mayor|voter|township|precinct|cast|referendum|census|elector|case|town council|said district|such district.",
    "banking":".loan|trust|bank|agent|partnership|institution|foreign|stock|mortgage|deposit|surplus|interest|merger|credit union|partner|case|credit|gift|branch|transact.",
    "licensing":".license|fee|dealer|sale|food|sold|holder|sell|valid|fish|agent|distributor|milk|liquor|product|such license|livestock|game|card|retail|misdemeanor|fine.",
    "real_estate":".real|interest|sale|owner|contract|claim|lien|payment|transfer|instrument|seller|holder|issuer|debtor|claimant|buyer|pay|broker|settlement|receipt|money.",
    "bonds":".interest|bond|payment|commonwealth|cost|sale|paid|pay|project|power|thereon|sold|debt|pledge|local law|event|hereof|proper|said board|real|port|sell|therefrom.",
    "expenditures":".fund|account|money|paid|special|pay|tile|payment|transfer|for the fiscal year|excess|trust fund|so much thereof|deposit|state general fund|auditor|tie.",
    "bureaucracy":".governor|council|government|chief|fire|appoint|personnel|compact|conflict|perform|shall consist|invalid|parish|successor|volunteer|membership|head|travel.",
    "healthcare":".health|care|treatment|health care|physician|home|human|patient|mental|mental health|drug|social|condition|public health|medicaid|dental|client|review|institution.",
    "child_custody":".child|court|minor|children|parent|age|probation|crime|victim|parole|guardian|adult|petition|placement|youth|case|social|legal|child support|obligor|home.",
    "taxes":".tax|paid|gross|credit|return|net|rate|exempt|assessor|case|refund|equal|sale|total|calendar year|payment|fuel|portion|sold|price|retail|zone|pay|such tax.",
    "education":".school|school district|state board|district|student|institution|higher|teacher|special|aid|pupil|children|school year|tuition|high school|school board.",
    "traffic1":".motor|highway|driver|owner|traffic|plate|test|vessel|accident|weight|special|sect|trailer|railroad|state highway|stricken|feet|fine|alcohol|aircraft|carrier.",
    "traffic2":".street|road|feet|island|river|run|tract|team|great|highway|township|cent."
    }
type_to_id = {key : value for key,value in enumerate(mydico.keys())}


# regex classifcation
def classification(data):
    i=0
    for key, value in mydico.items():
        data.loc[data.title.str.contains(value), 'type']=key
        i=i+1
        data.loc[data.title.str.contains(value), 'typenum']=i
#mylistofcat=[ environment_list,courts_list , pensions_list,local_projects_list,elections_list, banking_list, licensing_list, real_estate_list, bonds_list, expenditures_list 
    # graph de classification
    fig, ax = plt.subplots()
    label=mydico.keys()
    counts, mybins, patches = ax.hist(data.typenum, facecolor='red', edgecolor='gray' , bins=17)
    # Set the ticks to be at the edges of the bins.
    ax = plt.hist(mybins, bins=17)
    plt.xticks(mybins , mydico.keys(), rotation='vertical')
    plt.title('Number of laws per categories')
    plt.show()

def overall_request(state, download=False,  **kwargs):
    #kwargs are here year and path
    #here I would like to put something like: if year is not specified
    get_session_list(state)
    #myyear=kwargs['year']
    if 'year' in kwargs:
        if (type(kwargs['year'])==int):
            myyear=str(kwargs['year'])
        if re.search(r'\d\d\d\d', myyear):
            global mylist
            mylist=mylist[mylist.year_start==int(myyear)]         
    mysessionlist=mylist['session_id']
    for i in mysessionlist:
        if (type(i)== int):
            i=str(i)
        get_bill_list(i)
        if download == True:
            print('hello')
            for j in mydatanew.bill_id: 
                if (type(j)==int):
                    j=str(j)
                import_text(j, kwargs['path'])
                
    classification(mytitlelist)
        
    
    