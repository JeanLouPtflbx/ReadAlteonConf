#!/usr/bin/python3
'''
----------------------------------------------------
autheur : Jean-lou Schmidt
mail    : Jeanlou.schmidt@gmail.com

version : 0.3 le 06/03/2014
----------------------------------------------------

Changelog 0.3 :
    - Nouveau selecteur de fichier de conf

Changelog 0.3 :
    - Affiche les filtres en doublon trouver dasn le fichier de conf

Changelog 0.4 :
    - Selection des filtres par source et/ou destination

Changelog 0.5 :
    - Factorisation et Nettoyage du code

Changelog 0.6 :
    - Changement esthetique

----------------------------------------------------
This program is released under GPLv3 license
----------------------------------------------------
'''
from bottle import route, run, get, post, request, template
import os
import re
import sys

Bas2Page="<b>Lecteur de fichier de configuration alteon </b>-<i> version : 0.6 </i>"

debug="0"

# Fichier de conf
FileName = ""
FContent =""

# Données du fichiers
virts = {}
reals = {}
filts = {}
groups = {}
services = {}

# Données simplifier du fichier pour facilité les manipulations
realsIDIP = {}
realsIPID = {}
virtsIDIP = {}
virtsIPID = {}
filtsSAD = {}

# Listes du formulaire
SelectableFiltsSIP = []
SelectableFiltsDIP = []
SelectableReals = []
SelectableVips = []
SelectableFiles = []

# Doublons filtres
filtsDouble = []
ListeFiltresDoublons = []

# Liste des objets selectionnés dans le formulaire
SelectedReals = []
SelectedRealsID = []
SelectedVips = []
SelectedVipsID =[]
SelectedFilters = []
SelectedFiltersSIP = []
SelectedFiltersDIP = []
SelectedFile = []

# Données des objets selectionnés
ListeReals = {}
ListeServices = {}
ListeGroups = {}
ListeVips = {}
ListeFiltres = {}

@route('/')
def index():
    global Bas2Page
    return template('formulaire',
                     error=None,
                     footer=Bas2Page,
                     SFile=True,
                     Fdata=False,
                     DVips=False,
                     DFiltres=False,
                     FiltresDoublons=False,
                     SelectableFiles=SelectableFiles)

@route('/', method='POST')
def DFile():
    global FContent
    global FileName
    global SelectableFiltsSIP
    global SelectableFiltsDIP
    global SelectableReals
    global SelectableVips
    global SelectedReals
    global SelectedRealsID
    global SelectedVips
    global SelectedVipsID
    global SelectedFiltersSIP
    global SelectedFiltersDIP
    global ListeVips
    global ListeServices
    global ListeGroups
    global ListeReals
    global ListeFiltres
    global realsIPID
    global virtsIPID
    global Bas2Page
    global filtsDouble
    global ListeFiltresDoublons
    global SelectableFiles
    
    SelectedRealsID = []
    SelectedReals = []
    SelectedVips = []
    SelectedVipsID = []
    SelectedFilters = []
    SelectedFiltersSIP = []
    SelectedFiltersDIP = []
    ListeReals = {}
    ListeVips = {}
    ListeServices = {}
    ListeGroups = {}
    ListeFiltres = {}
    RemoveFile =""
    DVips=False
    DFiltres=False
    
    # Chargement d'un nouveau fichier
    if request.forms.get('ListeFichiers') :
        FileName = request.forms.get('ListeFichiers')
        print(" = Chager un fichier : " + FileName)
        ProcessingFile("configfile/"+FileName)
    # Ou Ajouter et charger un nouveau fichier
    elif request.files.get('datafile1') :
        df1=request.files.get('datafile1')
        FileName = df1.filename
        print(" = Ajouter un fichier : " + FileName)
        if not os.path.exists("configfile/"+FileName):
            df1.save("configfile/.")
            ProcessingFile("configfile/"+FileName)
            ListConfigFiles()
    # Ou Supprimer un fichier
    elif request.forms.get('DelFile') :
        RemoveFile = request.forms.get('DelFile')
        print(" = Supprimer un fichier : " + RemoveFile)
        os.remove("configfile/"+RemoveFile)
        ListConfigFiles()
        return template('formulaire',
                     error=None,
                     footer=Bas2Page,
                     SFile=True,
                     Fdata=False,
                     DVips=False,
                     DFiltres=False,
                     FiltresDoublons=False,
                     SelectableFiles=SelectableFiles)
    
    # Reals de selectionnés ?
    if request.forms.get('ListeReals'):
        DVips=True
        SelectedReals = request.params.getall('ListeReals')
        [ SelectedRealsID.append(realsIPID[IP]) for IP in SelectedReals ]
        [ GetVipListFromRealID(RID) for RID in SelectedRealsID ]
    
    # Vips selectionnées ?
    if request.forms.get('ListeVips'):
        DVips=True
        SelectedVips = request.params.getall('ListeVips')
        SelectedVips = [ VIP.split(":")[0] for VIP in SelectedVips ]
        SelectedVips = Uniq(SelectedVips)
        for IP in SelectedVips :
            if virtsIPID[IP] not in SelectedVipsID:
                SelectedVipsID.append(virtsIPID[IP])
    
    # Affichage des Variables VIPS
    if DVips==True : 
        print(" = SelectedVipsID : ", end = " " )
        print(SelectedVipsID)
        print(" = SelectedVips : ", end = " " )
        print(SelectedVips)
        [ GetParamsFromVirtID(VID) for VID in SelectedVipsID ]
        print(" = ListeVips : ", end = " " )
        print( ListeVips )
        print(" = ListeServices : ", end = " " )
        print( ListeServices )
        print(" = ListeGroups : ", end = " " )
        print( ListeGroups )
        print(" = ListeReals : ", end = " " )
        print( ListeReals )
    
    # IP sources de Filts Selectionnés ?
    if request.forms.get('ListeFiltresSIP'):
        DFiltres=True
        SelectedFiltersSIP = request.params.getall('ListeFiltresSIP')
        [ GetFiltresListeFromSIP(SIP) for SIP in SelectedFiltersSIP ]
        print(" = SelectedFiltersSIP : ", end = " " )
        print( SelectedFiltersSIP)
    
    # IP dest de Filts Selectionnés ?
    if request.forms.get('ListeFiltresDIP'):
        DFiltres=True
        SelectedFiltersDIP = request.params.getall('ListeFiltresDIP')
        [ GetFiltresListeFromDIP(DIP) for DIP in SelectedFiltersDIP ]
        print(" = SelectedFiltersDIP : ", end = " " )
        print( SelectedFiltersDIP)

    # Afficher les Variables Filtres
    if DFiltres==True : 
        CheckListeFiltres()
        print(" = ListeFiltres : ", end = " " )
        print( ListeFiltres )
    
    # Si Action sur les fichier de Configuration
    if FileName and not ( SelectedReals or SelectedVips or SelectedFiltersSIP or SelectedFiltersDIP):
        return template('formulaire',
                    error=None,
                    footer=Bas2Page,
                    SFile=True,
                    Fdata=True,
                    DVips=False,
                    DFiltres=False,
                    ConfigFileName=FileName,
                    FileContent=FContent,
                    SelectableReals=SelectableReals,
                    SelectableVips=SelectableVips,
                    SelectableFiltsSIP=SelectableFiltsSIP,
                    SelectableFiltsDIP=SelectableFiltsDIP,
                    SelectableFiles=SelectableFiles,
                    LstReals=SelectedReals,
                    LstVips=SelectedVips,
                    LstFiltresSIP=SelectedFiltersSIP,
                    LstFiltresDIP=SelectedFiltersDIP,
                    LstFiltres=SelectedFilters,
                    ListeVips=ListeVips,
                    FiltresDoublons=False,
                    ListeFiltresDoublons=ListeFiltresDoublons)
    
    # Si Selection de Reals ou de Vips
    elif FileName and ( SelectedReals or SelectedVips ) and not ( SelectedFiltersSIP or SelectedFiltersDIP):
        return template('formulaire',
                    error=None,
                    footer=Bas2Page,
                    SFile=True,
                    Fdata=True,
                    DVips=True,
                    DFiltres=False,
                    ConfigFileName=FileName,
                    FileContent=FContent,
                    SelectableVips=SelectableVips,
                    SelectableReals=SelectableReals,
                    SelectableFiltsSIP=SelectableFiltsSIP,
                    SelectableFiltsDIP=SelectableFiltsDIP,
                    SelectableFiles=SelectableFiles,
                    LstReals=SelectedReals,
                    LstVips=SelectedVips,
                    ListeVips=ListeVips,
                    ListeServices=ListeServices,
                    ListeGroups=ListeGroups,
                    ListeReals=ListeReals,
                    FiltresDoublons=False)
    
    # Si Selection de Filtres
    elif FileName and not( SelectedReals or SelectedVips ) and ( SelectedFiltersSIP or SelectedFiltersDIP):
        return template('formulaire',
                    error=None,
                    footer=Bas2Page,
                    SFile=True,
                    Fdata=True,
                    DVips=False,
                    DFiltres=True,
                    ConfigFileName=FileName,
                    FileContent=FContent,
                    SelectableVips=SelectableVips,
                    SelectableReals=SelectableReals,
                    SelectableFiltsSIP=SelectableFiltsSIP,
                    SelectableFiltsDIP=SelectableFiltsDIP,
                    SelectableFiles=SelectableFiles,
                    LstFiltres=SelectedFilters,
                    LstFiltresSIP=SelectedFiltersSIP,
                    LstFiltresDIP=SelectedFiltersDIP,
                    ListeFiltres=ListeFiltres,
                    FiltresDoublons=True,
                    ListeFiltresDoublons=ListeFiltresDoublons)
    
    # Si selection de Reals Vips ou Filtres 
    elif FileName and ( SelectedReals or SelectedVips or SelectedFiltersSIP or SelectedFiltersDIP):
        return template('formulaire',
                    error=None,
                    footer=Bas2Page,
                    SFile=True,
                    Fdata=True,
                    DVips=True,
                    DFiltres=True,
                    ConfigFileName=FileName,
                    FileContent=FContent,
                    SelectableVips=SelectableVips,
                    SelectableReals=SelectableReals,
                    SelectableFiltsSIP=SelectableFiltsSIP,
                    SelectableFiltsDIP=SelectableFiltsDIP,
                    SelectableFiles=SelectableFiles,
                    LstReals=SelectedReals,
                    LstVips=SelectedVips,
                    LstFiltres=SelectedFilters,
                    LstFiltresSIP=SelectedFiltersSIP,
                    LstFiltresDIP=SelectedFiltersDIP,
                    ListeVips=ListeVips,
                    ListeServices=ListeServices,
                    ListeGroups=ListeGroups,
                    ListeReals=ListeReals,
                    ListeFiltres=ListeFiltres,
                    FiltresDoublons=True,
                    ListeFiltresDoublons=ListeFiltresDoublons)
    
# Charger la preview du fichier
def LoadFile(ConfigFileName):
    global FContent
    print(" = Chargement du fichier : " + ConfigFileName )
    ConfigFile = open(ConfigFileName,'r',encoding='utf-8', errors='ignore')
    FContent=ConfigFile.read()
    ConfigFile.close()

# Charger le dossier des fichiers de config
def ListConfigFiles():
    global SelectableFiles
    SelectableFiles = []
    SelectableFiles.append("")
    SelectableFiles.extend(os.listdir("configfile/."))

# Lecture du fichier de conf
def ReadConfigFile(ConfigFileName):
    global debug
    global reals
    global virts
    global groups
    global filts
    global services
    
    reals = {}
    virts = {}
    groups = {}
    filts = {}
    services = {}
    
    print(" = Lecture du fichier : " + ConfigFileName )
    ConfigFile = open(ConfigFileName,'r',encoding='utf-8', errors='ignore')
    # on parcours le fichier ligne par ligne
    CurrentLine = ConfigFile.readline()
    while True:
        if re.search("/real ", CurrentLine) :
            RID = CurrentLine.split("/")[3].split()[1]
            if not RID in reals: reals[RID] = []
            if (debug == "1") : print(" = DEBUG = Traitement de real " + RID) 
            reals[RID].append(CurrentLine.replace("\n",""))
            CurrentLine = ConfigFile.readline()
            while re.search("^[ \t].+", CurrentLine):
                reals[RID].append("  " + CurrentLine.strip())
                CurrentLine = ConfigFile.readline()
        elif re.search("/group ", CurrentLine):
            GID = CurrentLine.split("/")[3].split()[1]
            if not GID in groups: groups[GID] = []
            if (debug == "1") : print(" = DEBUG = Traitement de group " + GID) 
            groups[GID].append(CurrentLine.replace("\n",""))
            CurrentLine = ConfigFile.readline()
            while re.search("^[ \t].+", CurrentLine):
                groups[GID].append("  " + CurrentLine.strip())
                CurrentLine = ConfigFile.readline()
        elif re.search("/virt", CurrentLine) and not re.search("/service ", CurrentLine) :
            VID = CurrentLine.split("/")[3].split()[1]
            if not VID in virts: virts[VID] = []
            if (debug == "1") : print(" = DEBUG = Traitement de virt " + VID) 
            virts[VID].append(CurrentLine.replace("\n",""))
            CurrentLine = ConfigFile.readline()
            while re.search("^[ \t].+", CurrentLine):
                virts[VID].append("  " + CurrentLine.strip())
                CurrentLine = ConfigFile.readline()
        elif re.search("/virt ", CurrentLine) and re.search("/service ", CurrentLine) :
            VID = CurrentLine.split("/")[3].split()[1]
            SID = CurrentLine.split("/")[4].split()[1]
            if VID not in services: services[VID] = {}
            if SID not in services[VID]: services[VID][SID] = []
            if (debug == "1") : print(" = DEBUG = Traitement de service " + SID + " de la vip " + VID) 
            services[VID][SID].append(CurrentLine.replace("\n",""))
            CurrentLine = ConfigFile.readline()
            while re.search("^[ \t].+", CurrentLine):
                services[VID][SID].append("  " + CurrentLine.strip())
                CurrentLine = ConfigFile.readline()
        elif re.search("/filt", CurrentLine):
            FID = CurrentLine.split("/")[3].split()[1]
            if not FID in filts: filts[FID] = []
            if (debug == "1") : print(" = DEBUG = Traitement de filt " + FID) 
            filts[FID].append(CurrentLine.replace("\n",""))
            CurrentLine = ConfigFile.readline()
            while re.search("^[ \t].+", CurrentLine):
                filts[FID].append("  " + CurrentLine.strip())
                CurrentLine = ConfigFile.readline()
        else:
            CurrentLine = ConfigFile.readline()
            if not CurrentLine : 
                ConfigFile.close()
                break

# Creation des Dicos virtsIDIP et virtsIPID et SelectableVips
def virtsENV():
    global virts
    global virtsIDIP
    global virtsIPID
    global SelectableVips
    global groups
    global services
    
    virtsIDIP = {}
    virtsIPID = {}
    SelectableVips = []
    
    for ID in virts :
        for item in virts[ID]:
            if re.search("vip ",item) :
                IP=item.split()[1]
                virtsIDIP[ID]=IP
                virtsIPID[IP]=ID
    virt = {}
    IPsort = []
    [ IPsort.append(LongIP(IP)) for IP in virtsIPID.keys()]
    IPsort = sorted(IPsort)
    for IP in IPsort:
        virt['ID'] = virtsIPID[ShortIP(IP)]
        virt['IP'] = ShortIP(IP)
        for SID in services[virt['ID']] :
            virt['SID']= SID
            for item in services[virt['ID']][SID] :
                if re.search("group",item) :
                    GID = item.split()[1]
                    if GID in groups :
                        for item in groups[GID] :
                            if re.search("name",item) :
                                virt['name'] = item.split()[1].replace("\"","").strip()
                                SelectableVips.append(virt['IP'] + ":" + SID + " - " + virt['name'])

# Creation des Dicos realsIDIP et realsIPID et SelectableReals
def realsENV():
    global reals
    global realsIDIP
    global realsIPID
    global SelectableReals
    
    realsIDIP = {}
    realsIPID = {}
    SelectableReals = []
    
    for ID in reals :
        for item in reals[ID]:
            if re.search("rip ",item) :
                IP=item.split()[1]
                #print("Reals - ID: " + ID +" " + "IP: " + IP)
                realsIDIP[ID]=IP
                realsIPID[IP]=ID
    real = {}
    IPsort = []
    [ IPsort.append(LongIP(IP)) for IP in realsIPID.keys()]
    IPsort = sorted(IPsort)
    for IP in IPsort:
        real['ID'] = realsIPID[ShortIP(IP)]
        real['IP'] = ShortIP(IP)
        for item in reals[real['ID']] :
            if re.search("name ",item):
                real['name']=item.replace("name ","").replace("\"","").strip()
        SelectableReals.append(real['IP'] + " " + real['name'])

# Creation du dico FiltresSAD et SelectableFiltsSIP
def filtsENV():
    global filts
    global filtsSAD
    global SelectableFiltsSIP
    global SelectableFiltsDIP
    
    filtsSAD = {}
    SelectableFiltsSIP = []
    SelectableFiltsDIP = []
    
    for FID in filts:
        NFilt = {}
        for item in filts[FID]:
            if re.search("dip ",item): NFilt['dip']=item.split()[1]
            if re.search("action ",item): NFilt['action']=item.split()[1]
            if re.search("sip ",item): NFilt['sip']=item.split()[1]
            if re.search("name ",item): NFilt['name']=item.replace("name ","").replace("\"","").strip()
        filtsSAD[FID] = {}
        filtsSAD[FID] = NFilt
    for FID in filts:
        for item in filts[FID]:
            if re.search("sip ",item): 
                sip=LongIP(item.split()[1])
                if sip not in SelectableFiltsSIP: SelectableFiltsSIP.append(sip)
            if re.search("dip ",item): 
                dip=LongIP(item.split()[1])
                if dip not in SelectableFiltsDIP: SelectableFiltsDIP.append(dip)
    SelectableFiltsSIP=sorted(SelectableFiltsSIP)
    SelectableFiltsSIP= [ ShortIP(IP) for IP in SelectableFiltsSIP ]
    SelectableFiltsDIP=sorted(SelectableFiltsDIP)
    SelectableFiltsDIP= [ ShortIP(IP) for IP in SelectableFiltsDIP ]

# Population du dico ListeFiltres depuis Source IP
def GetFiltresListeFromSIP(IP) :
    global filtsSAD
    global ListeFiltres
    global SelectedFiltersSIP
    global SelectedFilters
    print (" = GetFiltresListeFromSIP : " + IP)
    for SIP in SelectedFiltersSIP :
        for FID in filtsSAD :
            if re.search(SIP,filtsSAD[FID]['sip']) :
                ListeFiltres[FID] = {}
                ListeFiltres[FID] = filtsSAD[FID]

# Population du dico ListeFiltres depuis Destination IP
def GetFiltresListeFromDIP(IP) :
    global filtsSAD
    global ListeFiltres
    global SelectedFiltersDIP
    global SelectedFilters
    print (" = GetFiltresListeFromDIP : " + IP )
    for DIP in SelectedFiltersDIP :
        for FID in filtsSAD :
            if re.search(DIP,filtsSAD[FID]['dip']) :
                ListeFiltres[FID] = {}
                ListeFiltres[FID] = filtsSAD[FID]

# Vérification de ListeFiltres
def CheckListeFiltres():
    global ListeFiltres
    print (" = CheckListeFiltres ", end =":" )
    for FID in ListeFiltres :
        if 'name' not in ListeFiltres[FID] :
            print( FID +" Name=NULL", end =", ")
            ListeFiltres[FID]['name'] = "NULL"
    print("")

# Trouver les filtres en doublons
def GetDoubleFilters():
    global filts
    global filtsSAD
    global filtsDouble
    global ListeFiltresDoublons
    filtsDouble = []
    ListeFiltresDoublons = []
    
    for FID1 in filtsSAD :
        for FID2 in filtsSAD :
            if ( FID1 != FID2 ) and ((filtsSAD[FID1]['sip'] == filtsSAD[FID2]['sip']) and (filtsSAD[FID1]['dip'] == filtsSAD[FID2]['dip'] ) and (filtsSAD[FID1]['action'] == filtsSAD[FID2]['action'])):
                if FID1 not in filtsDouble:
                    filtsDouble.append(FID1)
                if FID2 not in filtsDouble:
                    filtsDouble.append(FID2)
    for FID in filtsDouble :
        if FID not in ListeFiltresDoublons:
            ListeFiltresDoublons.append(filtsSAD[FID]['name'] + ";"+ FID + ";" + filtsSAD[FID]['sip'] + ";" + filtsSAD[FID]['action'] + ";" + filtsSAD[FID]['dip'])
            ListeFiltresDoublons = sorted(ListeFiltresDoublons)

# Formatage des adresses IP
# IP courte --> IP longue
def LongIP(IP):
    try :
        return '%s.%s.%s.%s' % tuple([s.zfill(3) for s in IP.split('.')])
    except :
        return IP
# IP longue --> IP courte
def ShortIP(IP):
    try:
        return '%s.%s.%s.%s' % tuple([int(s) for s in IP.split('.')])
    except :
        return IP

# Supprimer les doublons d'une liste
def Uniq(seq, idfun=None): 
   # order preserving
   if idfun is None:
       def idfun(x): return x
   seen = {}
   result = []
   for item in seq:
       marker = idfun(item)
       # in old Python versions:
       # if seen.has_key(marker)
       # but in new ones:
       if marker in seen: continue
       seen[marker] = 1
       result.append(item)
   return result

# Récuperer les données utiles d'un real
def GetRealParams(RealID):
    global reals
    # print(" = GetRealParams " + RealID)
    if re.match("r",RealID) :
        backup = "true"
        RealID = RealID.replace("r","")
    else:
        backup = "false"
    Real = {}
    Real['inter'] = "2"
    Real['retry'] = "4"
    if RealID not in reals:
        print(" = ERROR = L'objet real " + RealID + " n'existe pas !")
    else :
        for item in reals[RealID]:
            if re.search("name ",item): Real['name'] = item.strip().split()[1].replace('"',"")
            if re.search("rip ",item): Real['rip'] = item.strip().split()[1]
            if re.search("inter ",item): Real['inter'] = item.strip().split()[1]
            if re.search("retry ",item): Real['retry'] = item.strip().split()[1]
        if backup == "false" : 
            Real['role']="Actif"
        else:
            Real['role'] = "Backup"
    return Real

# Récuperer les données utiles d'un group
def GetGroupParams(GroupID):
    global groups
    #print(" = GetGroupParams " + GroupID)
    Group = {}
    Group['name'] = ""
    Group['reals'] = ""
    Group['content'] =""
    Group['health'] = "tcp"
    Group['metric'] = ""
    if GroupID not in groups:
        print(" = ERROR = L'objet group " + GroupID +" n'existe pas !")
        Group['name']='NotDefined'
        groups[GroupID]=Group
    else :
        for item in groups[GroupID]:
            if re.search("health ",item) : Group['health'] = item.strip().split()[1]
            if re.search("add",item) or re.search("backup",item) : 
                rid = item.strip().split()[1]
                if rid not in Group['reals'].split(" ") :
                    Group['reals'] = Group['reals'] + " " + rid
            if re.search("metric ",item) : Group['metric'] = item.strip().split()[1]
            if re.search("content ",item) : Group['content'] = item.strip().split()[1].replace('"',"")
            if re.search("name ",item) : Group['name'] = item.strip().split()[1].replace('"',"")
    return Group

# Récuperer les données utiles d'une vip
def GetVirtParams(VirtID):
    global virts
    #print(" = GetVirtParams "+VirtID)
    Virt = {}
    Virt['dname'] =""
    if VirtID not in virts:
        print(" = ERROR = L'objet virt " + VirtID + " n'existe pas !")
        Virt['dname'] ="NotDefined"
        virts[VirtID]=Virt
    else:
        for item in virts[VirtID]:
            if re.search("vip ",item) : Virt['vip'] = item.strip().split()[1]
            if re.search("dname ",item) : Virt['dname'] = item.strip().split()[1].replace('"',"")
    return Virt

# Récuperer les données utiles d'un service
def GetServiceParams(VirtID,ServiceID):
    global services
    global ListeServices
    #print(" = GetServiceParams VirtID=" + VirtID + " - ServiceID=" + ServiceID)
    Serv = {}
    Serv['rport'] = ServiceID
    Serv['tmout'] = "10"
    Serv['ptmout'] = "10"
    Serv['pbind'] = "Disable"
    Serv['cookie'] = ""
    if ServiceID not in services[VirtID]:
        print(" = ERROR = L'objet service " + ServiceID + " n'existe pas !")
    else :
        for item in services[VirtID][ServiceID]:
            if re.search("service ",item) and not re.search("cookie",item) : Serv['service'] = item.strip().split("/")[4]
            elif re.search("service ",item) and re.search("cookie",item) : 
                Serv['cookie'] = item.strip().split("/")[5].replace("pbind cookie passive ","")
                Serv['pbind'] = "cookie"
            elif re.search("group ",item) : Serv['group'] = item.strip().split()[1]
            elif re.search("rport ",item) : Serv['rport'] = item.strip().split()[1]
            elif re.search("pbind ",item) : Serv['pbind'] = item.strip().split()[1]
            elif re.search(" tmout ",item) : Serv['tmout'] = item.strip().split()[1]
            elif re.search("ptmout ",item) : Serv['ptmout'] = item.strip().split()[1]
    return Serv

# Données Vip+Service+group+Real à partir d'un VIPID
def GetParamsFromVirtID(VirtID):
    global reals
    global virts
    global services
    global groups
    global ListeVips
    global ListeServices
    global ListeGroups
    global ListeReals
    #print(" = GetParamsFromVirtID : " + VirtID )
    if VirtID not in ListeVips : 
        ListeVips[VirtID] = {}
        ListeVips[VirtID] = GetVirtParams(VirtID)
    if VirtID not in ListeServices : 
        ListeServices[VirtID] = {}
    for SID in services[VirtID] :
        GetServiceParams(VirtID,SID)
        if SID not in ListeServices[VirtID] :
            ListeServices[VirtID][SID] = {}
            ListeServices[VirtID][SID] = GetServiceParams(VirtID,SID)
        for item in services[VirtID][SID]:
            if re.search("group ",item) :
                GID=item.strip().split()[1]
                if GID not in ListeGroups :
                    ListeGroups[GID] = {}
                    ListeGroups[GID] = GetGroupParams(GID)
                for item in groups[GID]:
                    if re.search("add ",item) or re.search("backup ",item):
                        RID=item.strip().split()[1]
                        if RID not in ListeReals :
                            ListeReals[RID] = {}
                            ListeReals[RID] = GetRealParams(RID)

# Liste des Vips à partir d'un Real
def GetVipListFromRealID(RealID):
    global virts
    global reals
    global groups
    global filts
    global realsIDIP
    global ListeVips
    global SelectedVipsID
    
    LocalGroups = []
    LocalReals = []
    LocalVIPs = []
    #print(" = GetVipListFromRealID "+ RealID)
    # On cherche le RealID correspondant a l'IP :
    if RealID not in realsIDIP :
        print("\n  le real " + RealID + " n'est pas connu !\n")
    else:
        LocalReals.append(RealID)
        #print(LocalReals)
        # On cherche les groups qui contiennent les real
        for RID in LocalReals:
            for GID in groups:
                for item in groups[GID]:
                    if (re.search("add "+RID+"$",item) or re.search("backup r"+RID+"$",item)):
                        LocalGroups.append(GID)
        #print(LocalGroups)
        # On cherche les service/VIP associes aux groupes
        for GID in LocalGroups:
            for VID in virts :
                for SID in services[VID]:
                    for item in services[VID][SID]:
                        if (re.search("group "+GID+"$",item)):
                            if VID not in LocalVIPs:
                                LocalVIPs.append(VID)
        #print(LocalVIPs)
        for VID in LocalVIPs:
            if virtsIDIP[VID] not in SelectedVips :
                SelectedVips.append(virtsIDIP[VID])
            if VID not in SelectedVipsID:
                SelectedVipsID.append(VID)

# Lecture du fichier de Conf
def ProcessingFile(File):
    global realsIDIP
    global realsIPID
    global virtsIDIP
    global virtsIPID
    
    realsIDIP = {}
    realsIPID = {}
    virtsIDIP = {}
    virtsIPID = {}
    
    ReadConfigFile(File)
    LoadFile(File)
    virtsENV()
    realsENV()
    filtsENV()
    GetDoubleFilters()


ListConfigFiles()

run(host='0.0.0.0', port=9090, debug=True, reloader=True)
