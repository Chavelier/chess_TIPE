from board import *
from tkinter import *
from tkinter import ttk
import tkinter as t
from engine import *
import os
import numpy as np
import matplotlib.pyplot as plt

############## CREATION DE LECHEQUIER ET INITIALISATION ######################

tk = Tk() #Création de la fenêtre du jeu
tk.title("Chess")
<<<<<<< Updated upstream
<<<<<<< Updated upstream
tk.resizable(width=False,height=False)
tk.maxsize(2000,1000)

canvas = Canvas(tk, width=720, height=720,bd=0, highlightthickness=0)
txt = StringVar()
txt.set("Eval (côté blanc) : 0.0")
tabl = Label(tk,textvariable=txt)
=======
tk.geometry("900x750")
tk.iconbitmap("logo.ico")

canvas = Canvas(tk, width=720, height=720,bd=0, highlightthickness=0)
txt = StringVar()
>>>>>>> Stashed changes

reverse_mode = False
=======
tk.geometry("900x750")
tk.iconbitmap("logo.ico")

canvas = Canvas(tk, width=720, height=720,bd=0, highlightthickness=0)
txt = StringVar()

reverse_mode = False
black_mode = False

<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
B = Board() #création échéquier
E = Engine() #creation engine

imglist = [] #liste des images à afficher (pièces)
imgfile2 = "pieces/z_case_indic.png"
imgitem2 = PhotoImage(file=imgfile2)
fleche_x = (0,0) #Repère des flèches à afficher

def affiche_position(l=[]):

    canvas.delete("all") # NECESSAIRE POUR L'OPTIMISATION ! (sinon les images s'enpiles au fur et à mesure)
    global imglist #besoin d'etre global sinon disparition des images
    imglist = []
    val = 0 #compteur nécessaire pour numéroter les tags des différentes images

    mrgx = 40
    mrgy = 40
    cell = 80

    folderName="pieces"
    liste=os.listdir(folderName) # =>recupere le nom de tous les fichiers d'un dossier
    for j in range(8):
        for i in range(8):
            if (i+j)%2 == 0: col = '#f6f6f6'
            else: col = '#5d8daa'

            if reverse_mode and B.side2move == "noir":
                nb_id = j+1
                ltr_id = 72-i
                case_id = 63-(i+8*j)
            else:
                nb_id = 8-j
                ltr_id = 65+i
                case_id = i+8*j

            canvas.create_text(mrgx//2,cell*(j+1),text=str(nb_id))
            canvas.create_text(cell*(i+1),mrgy//2,text=chr(ltr_id))
            canvas.create_rectangle(mrgx+i*cell,mrgy+j*cell,mrgx+(i+1)*cell,mrgy+(j+1)*cell,fill=col)

            if B.history != []:
                if B.history[-1][0] == case_id or B.history[-1][1] == case_id:
                    canvas.create_rectangle(mrgx+i*cell,mrgy+j*cell,mrgx+(i+1)*cell,mrgy+(j+1)*cell,fill='orange',stipple="gray50")

            ma_piece = B.cases[case_id]
            if ma_piece.nom != ma_piece.nomPiece[0]:
                pos = ma_piece.nomPiece.index(ma_piece.nom)-1
                if ma_piece.couleur == "noir":
                    pos += 6
                imgfile = folderName +'/'+liste[pos] ## strchemin:str, chemin d'accès à l'image
                imglist += [PhotoImage(file=imgfile)]
                canvas.create_image(mrgx+(i+0.5)*cell, mrgy+(j+0.5)*cell, image=imglist[i+8*j],tag='img'+str(val))
                tag = canvas.gettags('img'+str(val))
                val += 1
                if ma_piece.nom == "ROI":

                    if ma_piece.couleur == "blanc" and B.in_check("blanc"):
                        canvas.create_rectangle(mrgx+i*cell,mrgy+j*cell,mrgx+(i+1)*cell,mrgy+(j+1)*cell,fill='#ff0000',stipple="gray50")
                    elif ma_piece.couleur == "noir" and B.in_check("noir"):
                        canvas.create_rectangle(mrgx+i*cell,mrgy+j*cell,mrgx+(i+1)*cell,mrgy+(j+1)*cell,fill='#ff0000',stipple="gray50")
            else:

                imglist += [""]

    if l != []: #gestion affichage coups possibles
        for pos in l:
            if reverse_mode and B.side2move == "noir":
                posx = 7-B.COL(pos)
                posy = 7-B.ROW(pos)
            else:
                posx = B.COL(pos)
                posy = B.ROW(pos)
            canvas.create_image(mrgx+(posx+0.5)*cell, mrgy+(posy+0.5)*cell, image=imgitem2)

affiche_position()

################## FONCTIONS AUXILIAIRES (ETUDE DES PERF ETC) ####################

def show_proba(E):
    L1 = E.la_proba(B,1000,100,7)
    y_list1 = []
    #L2 = E.la_proba(B,1000,30)
    #y_list2 = []
    L3 = E.la_proba(B,1000,50,7)
    y_list3 = []
    for i in range(100):
        y_list1 += [(L1.count(i))/(1000*100)]
    #for i in range(100):
        #y_list2 += [(L2.count(i))/(1000*30)]
    for i in range(100):
        y_list3 += [(L3.count(i))/(1000*50)]
    plt.plot(np.array(list(range(100))), np.array(y_list1),label="1000 parties, 100 coups")
    plt.plot(np.array(list(range(100))), np.array(y_list3),label="1000 parties, 50 coups")
    #plt.plot(np.array(list(range(100))), np.array(y_list2),label="1000 parties, 30 coups")
    plt.title("Distribution de probabilité")
    plt.xlabel("Nombre de coups possibles")
    plt.ylabel("Probabilité")
    plt.legend()
    plt.show()#Disparité des coups possibles par position

def comparaison(n,c,p):
    l1_final = []
    l2_final = []
    y1 = 0
    y2 = 0
    for i in range(n):
        E.setDepth('sd ' + str(p))
        (a,b) = E.komparaison(c,p,B)
        l1_final += a
        l2_final += b
        E.newgame(B)
    for i in range(len(l1_final)):
        y1 += l1_final[i]
        y2 += l2_final[i]
    print('Valeur moyenne pour',n,'parties de',c,'coups joués à la profondeur',p)
    print('Gog :', y1/(n*c))
    print('Elagage :', y2/(n*c))#Comparaison de minmax et alphabeta (n=nombre de parties, c=nombre de coups par parties après ouverture,p=profondeur)

def creation_puzz(E):
    print("Génération d'un problème en cours")
    #E.crea_puzz(B)

def mlire(event): #Se délenche après avoir cliquer sur le nom d'une des partie
    partie = cBox.get()
    E.lire(B,'read '+partie)
    E.mode_lecture = True
    win.destroy()

def nom_ligne(ligne): #Nécessaire pour simplifier la fonction qui suit
    nom = ''
    for i in range(len(ligne)):
        c = ligne[i]
        if c == ' ':
            return(nom)
        nom += ligne[i]

def mlecture(): #Se déclenche au moment de l'appui sur le bouton des lectures de parties
    global cBox
    global win
    win = Toplevel(tk)
    win.iconbitmap("logo.ico")
    label_parties = Label(win, text="Choix de la partie")
    label_parties.pack()
    liste_parties = []
    with open("saves.txt",'rt') as file:
        for ligne in file:
            liste_parties += [nom_ligne(ligne)]
    cBox = ttk.Combobox(win,values=liste_parties)
    cBox.current(0)
    cBox.bind("<<ComboboxSelected>>",mlire)
    cBox.pack()
    win.mainloop()


################## ESSAI DU MENU ##################

v = t.IntVar()

def newg():
    E.newgame(B)
    affiche_position()
    print("Nouvelle partie !")


box2 = Frame(tk) #### Création d'un cadre pour un menu avec des boutons ronds plus efficaces
b1 = Radiobutton(box2, variable = v, value = 0,text='Nouvelle partie',command=newg)
b2 = Radiobutton(box2, variable = v,value = 1,text='Résolution de problèmes',command=creation_puzz)
b3 = Radiobutton(box2, variable = v,value = 2,text='Lecture de parties',command=mlecture)

box2.pack(expand=YES,side=RIGHT)
b1.grid(row=0, column=0, sticky=W)
b2.grid(row=1, column=0, sticky=W)
b3.grid(row=2, column=0, sticky=W)


################## FONCTION D'EXECUTION DES COMMANDES ####################

def execute_cmd():
    cmd= cmd_bar.get()

<<<<<<< Updated upstream
=======
    global reverse_mode
    global black_mode

<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
    if cmd == "new":
        E.newgame(B)
    elif cmd == "quit":
        tk.quit()
    elif cmd == "undo":
        E.undomove(B)
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    elif cmd == "eps":
        print(E.epsilon)
        for i in range(E.epsilon):
            d = 1

    elif cmd == "ieps":
        print(B.cases)
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
    elif cmd == "go":
        E.play_bot(B)
    elif "gog" in cmd:
        E.play_bot2(int(cmd.split()[1]),B)
    elif cmd == "droite" :
        if E.mode_lecture:
            E.compteur(1)
            E.lecture(B,E.val_compteur)
    elif cmd == "gauche" :
<<<<<<< Updated upstream
<<<<<<< Updated upstream
        E.compteur(-1)
        E.undomove(B)
=======
=======
>>>>>>> Stashed changes
        if E.mode_lecture:
            E.compteur(-1)
            E.undomove(B)
    elif "setboard" in cmd:
        E.setboard(B,cmd)
>>>>>>> Stashed changes
    elif cmd == "getboard":
        E.getboard(B)
    elif cmd == "nulle_rep":
        print(E.listfen)
    elif cmd == "proba":
        #show_proba(E)
        print(B.lastprise())
        print(B.cases)
    elif "comp" in cmd:
        l = cmd.split()
        comparaison(int(l[1]),int(l[2]),int(l[3]))
    elif cmd == "eval" :
        print("evaluation (pour blancs) : " + str(B.evaluer("blanc")/100))
    elif cmd == "op" :
        print(E.ouverture(B))
    elif cmd == "histo" :
        print(B.history)
    elif cmd == 'save_op':
        E.create_op(B)
    elif 'save' in cmd :
        E.save(B,cmd)
    elif 'read' in cmd :
        E.lire(B,cmd)
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
=======
>>>>>>> Stashed changes
        E.mode_lecture = True
    elif cmd == "black":
        reverse_mode = False
        black_mode = not black_mode
        print("Black mode : %s"%black_mode)
>>>>>>> Stashed changes
    elif cmd == "reverse":
        global reverse_mode
        reverse_mode = not reverse_mode
        print("Reverse mode : %s"%reverse_mode)

    elif 'sd' in cmd:
        E.setDepth(cmd)
    elif 'perft' in cmd:
        E.perft(cmd,B)
    elif cmd == "d_rpos":
        print("ROI blanc : "+B.caseInt2Str(B.pos_roi_b))
        print("ROI noir : "+B.caseInt2Str(B.pos_roi_n))
    elif len(cmd) >= 4:
        E.usermove(B,cmd)
    affiche_position()
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    txt.set("Eval (côté blanc) : %s"%(B.evaluer("blanc")/100))
    cmd_bar.delete(0,"end")


def show_proba(E):
    L1 = E.la_proba(B,1000,100)
    y_list1 = []
    #L2 = E.la_proba(B,1000,30)
    #y_list2 = []
    L3 = E.la_proba(B,1000,50)
    y_list3 = []
    for i in range(100):
        y_list1 += [(L1.count(i))/(1000*100)]
    #for i in range(100):
        #y_list2 += [(L2.count(i))/(1000*30)]
    for i in range(100):
        y_list3 += [(L3.count(i))/(1000*50)]
    plt.plot(np.array(list(range(100))), np.array(y_list1),label="1000 parties, 100 coups")
    plt.plot(np.array(list(range(100))), np.array(y_list3),label="1000 parties, 50 coups")
    #plt.plot(np.array(list(range(100))), np.array(y_list2),label="1000 parties, 30 coups")
    plt.title("Distribution de probabilité")
    plt.xlabel("Nombre de coups possibles")
    plt.ylabel("Probabilité")
    plt.legend()
    plt.show()



# gestion des touches ----------------------------------------------------------
=======
    #txt.set("Eval (côté blanc) : %s"%(B.evaluer("blanc")/100))
    cmd_bar.delete(0,"end")

#################### GESTION DES TOUCHEs ######################
>>>>>>> Stashed changes
=======
    #txt.set("Eval (côté blanc) : %s"%(B.evaluer("blanc")/100))
    cmd_bar.delete(0,"end")

#################### GESTION DES TOUCHEs ######################
>>>>>>> Stashed changes

def button_push(evt=""): #se déclanche lors de l'appui sur bouton
    execute_cmd()

def on_click(evt):
    casex = (evt.x-40)//80
    casey = (evt.y-40)//80
    if -1<casex<8 and -1<casey<8:
<<<<<<< Updated upstream
<<<<<<< Updated upstream
        # if len(cmd_bar.get()) >= 4:
        #     cmd_bar.delete(0,"end")
        if reverse_mode and B.side2move == "noir":
=======
=======
>>>>>>> Stashed changes
        if (reverse_mode and B.side2move == "noir") or black_mode:
>>>>>>> Stashed changes
            coord2case = 63-(casex+8*casey)
        else:
            coord2case = casex+8*casey

        c = B.coord[coord2case]
        cmd_bar.insert("end",c)
        taille_texte = len(cmd_bar.get())
        if taille_texte == 2:
            liste = B.gen_moves_list()
            l2=[]
            for i in range(len(liste)):
                if liste[i][0] == B.caseStr2Int(cmd_bar.get()):
                    l2 += [liste[i][1]]
            if l2 != []:
                affiche_position(l2)
            else:
                cmd_bar.delete(0,"end")
        elif taille_texte >= 4:
            execute_cmd()

def on_click2(evt):
    if cmd_bar.get() == "":
        cmd_bar.insert("end","undo")
    execute_cmd()
def bot_play(evt):
    cmd_bar.delete(0,"end")
    cmd_bar.insert("end","go")
    execute_cmd()

def droite(evt):
    cmd_bar.delete(0,"end")
    cmd_bar.insert("end","droite")
    execute_cmd()
def gauche(evt):
    cmd_bar.delete(0,"end")
    cmd_bar.insert("end","gauche")
    execute_cmd()

def val1(evt): #Pour la création des flèches
    global fleche_x
    fleche_x = (evt.x,evt.y)

def val2(evt): #S'active au moment où le clique gauche est relaché, si le clique est rapide (sur la même case), on supprime toutes les flèches
    fleche_y = (evt.x,evt.y)
    if fleche_x == fleche_y:
        affiche_position()
    else:
        list = [fleche_x[0],fleche_x[1],fleche_y[0],fleche_y[1]]
        for i in range(len(list)): #On arrondi toutes les valeurs des clicks pour centrer les flèches!
            if list[i] < 120:
                list[i] = 80
            elif 120 < list[i] < 200:
                list[i] = 160
            elif 200 < list[i] < 280:
                list[i] = 240
            elif 280 < list[i] < 360:
                list[i] = 320
            elif 360 < list[i] < 440:
                list[i] = 400
            elif 440 < list[i] < 520:
                list[i] = 480
            elif 520 < list[i] < 600:
                list[i] = 560
            elif 600 < list[i] < 680:
                list[i] = 640
        canvas.create_line(list[0], list[1], list[2], list[3], width=10, arrow='last', arrowshape=(15,25,10),fill ='orange')


tk.bind_all('<KeyPress-Return>', button_push)
<<<<<<< Updated upstream
<<<<<<< Updated upstream
tk.bind_all('<1>', on_click)
tk.bind_all('<3>',on_click2)
tk.bind_all('<KeyPress-Control_L>', bot_play)
=======
=======
>>>>>>> Stashed changes
tk.bind_all('<Button-1>',on_click)
#tk.bind_all('<ButtonRelease-1>',animation)
tk.bind_all('<d>',on_click2) #undo
tk.bind_all('<Button-3>',val1)
tk.bind_all('<ButtonRelease-3>',val2)
# tk.bind_all('<KeyPress-Control_L>', bot_play)
tk.bind_all('<Up>', bot_play)
>>>>>>> Stashed changes
tk.bind_all('<Right>', droite)
tk.bind_all('<Left>', gauche)

box = Frame(tk)
cmd_bar = Entry(box)
btn = Button(box, text='ENTRER', command=button_push)

#Pack()
box.pack(expand=YES)
btn.grid(row=0, column=1, sticky=W)
cmd_bar.grid(row=0, column=0, sticky=W)
canvas.pack(expand=YES,side=RIGHT)
#Pack()




tk.mainloop()
