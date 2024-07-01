#!/usr/bin/python3

# Auteur : JM-1000


from turtle import *
from random import randint

def trace_carre(pos,plein,couleur):
    up()
    goto(pos)
    down()
    if plein==True:
        fillcolor(couleur)
        begin_fill()
        for i in range(4):
            forward(T)
            left(90)
        end_fill()
    else:
        for i in range(4):
            forward(T)
            left(90)

def trace_barres_V(pos,taille,plein,couleur,n):
    if plein==True:
        color(couleur)
    for i in range(n):
        up()
        goto(pos[0]+i*50,pos[1])
        down()
        if i==0:
            left(90)
        forward(taille)

def trace_barres_H(pos,taille,plein,couleur,n):
    if plein==True:
        color(couleur)
    for i in range(n):
        up()
        goto(pos[0],pos[1]+i*50)
        down()
        forward(taille)

def en_tetes(L,C):
    up()
    goto(origine[0]-(T/2),origine[1]+(T/2))
    for i in L:
        if i=='0':
            i='10'
        write(i)
        forward(50)
    goto(origine[0]-(T/2),origine[1]-(T/2))
    right(90)
    for i in C:
        forward(50)
        write(i)

def trace_grille(taille,plein,couleur):
    speed(100)
    hideturtle()
    trace_barres_H(origine,taille,plein,couleur,ent_l.__len__()+1)
    trace_barres_V(origine,taille,plein,couleur,ent_c.__len__()+1)
    en_tetes(ent_l,ent_c)

def coordennees_joueur():
    while True:
        try:
            x=input("  Coordennées (ex : C1) : ")
            if x[1]=='1' and x[2]=='0' and x.__len__()==3:
                x=x[0]+'0'; x[3]
            else:
                x[2]; print("!",end="  ")
        except:
            if x.__len__()==2 and ent_c.__contains__(x[0]) and ent_l.__contains__(x[1]):
                return x[0], x[1]
            else:
                print("!",end="  ")

def fab_trad_positions():
    positions={}
    for x in ent_c:
        for y in ent_l:
            positions[(x,y)]=(origine[0]+ent_c.index(x)*T,origine[1]+ent_l.index(y)*T)
    return positions

def navire_par_cases(liste1,liste2,total_nav,cases):
    nav,coordennee=[],[]
    for i in range(len(liste1)-(cases-1)):
        temp=''
        for c in range(cases):
            temp+=liste1[i+c]
        coordennee.append(temp)
    for coord in liste2:
        for i in coordennee:
            temp=[]
            for l in i:
                for pos in total_nav:
                    if coord==pos[0] and l==pos[1]:
                       temp.append(pos)
                       break 
                    if coord==pos[1] and l==pos[0]:
                       temp.append(pos)
                       break 
            nav.append(temp)
    return nav

def fab_nav():
    nav5,nav4,nav3,nav2=[],[],[],[]
    navires,total_nav=[],[]
    for x in ent_c:
        for y in ent_l:
            total_nav.append((x,y))
    lx,ly=list(ent_c),list(ent_l)
    nav5=navire_par_cases(lx,ly,total_nav,5)
    nav5+=navire_par_cases(ly,lx,total_nav,5)

    nav4=navire_par_cases(lx,ly,total_nav,4)
    nav4+=navire_par_cases(ly,lx,total_nav,4)

    nav3=navire_par_cases(lx,ly,total_nav,3)
    nav3+=navire_par_cases(ly,lx,total_nav,3)

    nav2=navire_par_cases(lx,ly,total_nav,2)
    nav2+=navire_par_cases(ly,lx,total_nav,2)
    
    while len(navires)!=5:
        navires=[nav5[randint(0,len(nav5))]]
        for nav in [nav4,nav3,nav3,nav2]:
            navires=verif_nav(nav[randint(0,len(nav)-1)],navires)
    return navires

def verif_nav(nav,navires):
    result=True
    for i in range(len(nav)):
            for navire in navires:
                if navire.__contains__(nav[i])==True:
                    result=False
    if result:
        navires.append(nav)
    return navires

def fab_grille():
    navires=fab_nav()
    grille={}
    for nav in navires:
        for coord in nav:
            grille[coord]=True
    for x in ent_c:
        for y in ent_l:
            if grille.__contains__((x,y))==True:
                continue
            else:
                grille[(x,y)]=False
    return navires,grille

def annoncer_nav_coule(devinnees,navires):
    for nav in navires:
        if nav.__contains__(devinnees):
            navires.remove(nav)
            print("       %d Navires coulés."%(5-len(navires)))
            break
    return  navires



ent_c='ABCDEFGHIJ'
ent_l='1234567890'
origine=(-200,-200)
T=50

def jouer():
    compte=0
    trad_pos=fab_trad_positions()
    (navires_en_vie,grille)=fab_grille()
    print('***Bataille navale***\nLe but du jeu est de couler les bateaux adverses avec moins des tentatives possibles.\n')
    trace_grille(10*T,False,'white')
    devinnees={}
    while navires_en_vie!=[]:
        compte+=1
        (x,y)=coordennees_joueur()
        pos=trad_pos[(x,y)]
        if grille[(x,y)]:
            trace_carre(pos,True,'salmon4')
            devinnees[(x,y)]=True
            navires_en_vie=annoncer_nav_coule((x,y),navires_en_vie)
        else:
            trace_carre(pos,True,'azure')
    print("  Bravo! Tous les navires sont coulés au bout de %d tentatives."%compte)
    input()

jouer()