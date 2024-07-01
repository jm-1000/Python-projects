#!/usr/bin/python3

# Auteur : JM-1000

import os

def liste_fileCSV(file_csv):        # Cette function crée une liste où chaque élément corresponde à une ligne du jeux de données
    x=[]
    file=open(file_csv,'r',encoding='utf-8')    # Le paramètre encoding='utf-8' c'est pour résoudre une érreur lorsqu'on éxecute le script sur Windows.
    line=file.readline();line=file.readline()
    while line !='':
        line=line.replace("\n","")
        line=line.replace("/VODAFONE"," (VODAFONE)")
        liste_temp=[]
        for colonne in [1,3,4,7,20,21]:                  #  On utilise les colonnes : nom du opérateur (c. 2), type de technologie (c. 4), date de création (c. 5),
            liste_temp.append(line.split(";")[colonne])  #génération (c. 8), coordonnées (c. 21) et statut de l’installation (c. 22).
        x.append(liste_temp)
        line=file.readline()
    file.close
    return x

def liste_codeHTML(file_html):      #  Cela crée une liste des listes où chaque section du code html est une liste.
    x=[[]]                          #  La position 0 corresponde aux lignes du <head>.
    file=open(file_html,'r',encoding='utf-8')
    line=file.readline();
    section,i=["index","bilan","operateur","annee","donnees",""],0
    while line !='':
        if line.__contains__('class="{0}"'.format(section[i]))==True:
            x.append([])
            i+=1
        x[i].append(line)
        line=file.readline()
    file.close
    return x


print("\nIl faut que le script et le dossier 'doc' soient dans votre dossier courant!")
print("\nLecture du jeu des données et les code html\n...")    
liste_globale=liste_fileCSV('doc/telecom.csv')
html=liste_codeHTML('doc/code.html') 


def indexHTML():                    # cette procédure crée la page index. 
    index=open('Index.html','w',encoding='utf-8')
    for code in html[0]:            # Les lignes des codes du <head>.
        if code.__contains__("/body")==False:
            code=code.replace("../doc","doc")
            index.write(code)
    for code in html[1]:                         # Les lignes de la section Index.
            index.write(code)
    index.write(find("/body",html[0]))           # Fermature du <body> et <html>
    index.close


def find(mot,html,replaceMot=None):         # Cette fonction cherche la ligne du code html où il y a une référence et la remplace. 
    for code in html:
        if code.__contains__(mot):
            if replaceMot==None:
                return code
            else:
                return code.replace(mot,replaceMot)


 
def bilanHTML():                                 # Création de la page bilan.
    try:
        os.mkdir("pages")
    except:
        print("...")
    bilan=open('pages/bilan.html','w',encoding='utf-8')
    for code in html[0]:
        if code.__contains__("/body")==False:
            bilan.write(code)
    for code in html[2]:                        # Les codes de la section Bilan.
        if code.__contains__("xcat"):           # xcat est une référence dans le code html pour étre remplacer (pareil pour tous les autres commeçant pour 'x').
            bilan.write(find("xtype",html[2],"Total des Antenne-relais")+find("xvaleur",html[2],str(len(liste_globale))))
            categorie,i=["Technologie","Système","Statut"],0
            for posCateg in [3,1,5]:         # On travaille avec les colonnes : génération, type de technologie et statut de l’installation respectivement.
                bilan.write(code.replace("xcat",categorie[i]))
                for liste in filtre_par_categorie(posCateg):
                    bilan.write(find("xtype",html[2],liste[0])+find("xvaleur",html[2],str(len(liste)))) 
                i+=1
        elif code.__contains__("xlien"):     # On travaille avec la colonne nom du opérateur.
                print("Générer les pages operateur, donnees et annees\n...")
                bilan.write(find("xcat",html[2]).replace("xcat","Opérateur"))
                for liste in filtre_par_categorie(0):
                    bilan.write(find("xlien",html[2],liste[0]+".html").replace("xtype",liste[0])+find("xvaleur",html[2],str(len(liste))))
                    liste.remove(liste[0])
                    #Création de une page por chaque opérateur :
                    operateurHTML(liste)     
                    donneesHTML(liste)
                    anneesHTML(liste)
        elif (code.__contains__("xtype") or code.__contains__("xvaleur"))==False:
            code=code.replace("xtitle","Bilan du jeux des données")
            bilan.write(code)
    bilan.write(find("/body",html[0]))
    bilan.close

def operateurHTML(listeOp):
    operateur=open("pages/"+listeOp[0][0]+".html","w",encoding='utf-8')
    for code in html[0]:
        if code.__contains__("/body")==False:
            operateur.write(code) 
    for code in html[3]:        # Section operateur.
        if code.__contains__("xcat"):
            operateur.write(find("xtype",html[2],"Total des Antenne-relais")+find("xvaleur",html[2],str(len(listeOp))))
            categorie,i=["Technologie","Système","Statut"],0
            for posCateg in [3,1,5]:
                operateur.write(code.replace("xcat",categorie[i]))
                for liste in filtre_par_categorie(posCateg,listeOp):
                    operateur.write(find("xtype",html[2]).replace("xtype",liste[0])+find("xvaleur",html[2],str(len(liste)))) 
                i+=1
        elif (code.__contains__("xtype") or code.__contains__("xvaleur"))==False:
            code=code.replace("xtitle","Présentation de données d'opérateur "+listeOp[0][0])
            code=code.replace("xannees",listeOp[0][0]+"_annees.html")
            code=code.replace("xop",listeOp[0][0])
            code=code.replace("xdonnees",listeOp[0][0]+"_donnees.html")
            operateur.write(code)
    operateur.write(find("/body",html[0]))
    operateur.close

def anneesHTML(listeOp):
    annee_liste=annee_par_operateur(listeOp)
    annees=open("pages/"+listeOp[0][0]+"_annees.html",'w',encoding='utf-8')
    for code in html[0]:
        if code.__contains__("/body")==False:
            annees.write(code)
    for code in html[4]:        #Section annee.
        if code.__contains__("xannee"):
            for i in range(len(annee_liste)):
                annees.write(code.replace("xannee",str(annee_liste[i][0])))
        elif code.__contains__("xtype"):
            for i1 in range(1,len(annee_liste[0])):
                annees.write(code.replace("xtype",annee_liste[0][i1][0]))
                for i2 in range(len(annee_liste)):
                    annees.write(find("xvaleur",html[4],str(annee_liste[i2][i1][1])))
        elif code.__contains__("xvaleur")==False:
            annees.write(code)
    annees.write(find("/body",html[0]))
    annees.close

def donneesHTML(listeOp):
    donnees=open('pages/'+listeOp[0][0]+'_donnees.html','w',encoding='utf-8')
    for code in html[0]:
        if code.__contains__("/body")==False:
            donnees.write(code)
    for code in html[5]:        #Section donnees
        if code.__contains__("xtype"):
            for liste in listeOp:
                donnees.write(find("xtype",html[5],liste[3]))
                for colonne in [1,2,4,5]:               #On travaille avec les colonnes : type de technologie, génération, date de création et statut de l’installation
                    donnees.write(find("xvaleur",html[5],liste[colonne]))
        elif (code.__contains__("xtype") or code.__contains__("xvaleur"))==False:
            donnees.write(code)
    donnees.write(find("/body",html[0]))
    donnees.close

def categorie_liste(colonne,liste2D=liste_globale):     # Cette fonction crée une liste des éléments differents d'une colonne du jeux des données.  
    x=[]
    for liste in liste2D:
            try:
                if x.__contains__(liste[colonne])!=True :
                    x.append(liste[colonne])
            except :
                continue
    x.sort()
    return x

def filtre_par_categorie(colonne,liste2D=liste_globale):        # Cela filtre chaque ligne du jeux des données selon un élément dans la liste créée par la foction categorie_liste.
    x=[]
    for liste in categorie_liste(colonne,liste2D):
        x.append([liste])
    for liste in liste2D:
            for i in range(len(x)):
                if liste[colonne]==x[i][0] :
                    x[i].append(liste)
                    break
    return x       # Retourne une liste où chaque èlèment est une liste dont le premier corresponde à la référence de la liste. Les autres éléments sont une liste d'une ligne du jeux des données.

def annee_par_operateur(Operateur_liste,colonne=1):         #Cela agroupe et calcule les nombre des antennes-relais instalées selon l'année et la catégorie.
        x=[[]]
        Operateur_liste.remove(Operateur_liste[0])
        for liste in Operateur_liste:           #Création d'une liste sur le format : [[année,[élément 1 de la categorie, quantité],(...)],[(...)],...]
            try:
                if x[0].__contains__(liste[2][:4])==False:
                    if liste[2][:4].isdigit():
                        x[0].append(liste[2][:4])
                        x.append([liste[2][:4]])
                        for categorie in categorie_liste(colonne,Operateur_liste):
                            x[len(x)-1].append([categorie,0])
            except:
                continue
        x.remove(x[0]);x.sort()

        for liste in Operateur_liste:
           x=categorie_par_annees(x,liste,colonne) 
        return x

def categorie_par_annees( liste2D,liste,colonne):  #Faire la comptage des antennes-relais selon les itéms au-dessus.
    for annee in liste2D:
        if(liste[2][:4]==annee[0]):
            for pos in range(len(annee)):
                if (liste[colonne]==annee[pos][0]):
                    annee[pos][1]+=1
                    break
            break                
    return liste2D



print("Générer les pages Index et bilan\n...")
indexHTML() 
bilanHTML()
print("\nSuccès! Aller sur Index.html")
