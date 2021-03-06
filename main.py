from board import *
from tkinter import *
from engine import *
import os
import numpy as np
import matplotlib.pyplot as plt

tk = Tk()
tk.title("Chess")
tk.resizable(width=False,height=False)
tk.maxsize(2000,1000)
# auto_play = False

canvas = Canvas(tk, width=720, height=720,bd=0, highlightthickness=0)
txt = StringVar()
tabl = Label(tk,textvariable=txt)

reverse_mode = False
black_mode = False
B = Board() #création échéquier
E = Engine() #creation engine

E.add_nulle(B) #ajoute la premiere position à la liste pour les nulles

txt.set(str(B.pos_id))

imglist = [] #liste des images à afficher (pièces)

imgfile2 = "pieces/z_case_indic.png"
imgitem2 = PhotoImage(file=imgfile2)


def affiche_position(l=[]):
    canvas.delete("all") # NECESSAIRE POUR L'OPTIMISATION ! (sinon les images s'enpiles au fur et à mesure)
    global imglist #besoin d'etre global sinon disparition des images
    imglist = []

    mrgx = 40
    mrgy = 40
    cell = 80

    folderName="pieces"
    liste=os.listdir(folderName) # =>recupere le nom de tous les fichiers d'un dossier
    for j in range(8):
        for i in range(8):
            if (i+j)%2 == 0: col = '#f6f6f6'
            else: col = '#5d8daa'

            if (reverse_mode and B.side2move == "noir") or black_mode:
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
                canvas.create_image(mrgx+(i+0.5)*cell, mrgy+(j+0.5)*cell, image=imglist[i+8*j])
                if ma_piece.nom == "ROI":
                    if ma_piece.couleur == "blanc" and B.in_check("blanc"):
                        canvas.create_rectangle(mrgx+i*cell,mrgy+j*cell,mrgx+(i+1)*cell,mrgy+(j+1)*cell,fill='#ff0000',stipple="gray50")
                    elif ma_piece.couleur == "noir" and B.in_check("noir"):
                        canvas.create_rectangle(mrgx+i*cell,mrgy+j*cell,mrgx+(i+1)*cell,mrgy+(j+1)*cell,fill='#ff0000',stipple="gray50")
            else:
                imglist += [""]
    if l != []: #gestion affichage coups possibles
        for pos in l:
            if (reverse_mode and B.side2move == "noir") or black_mode:
                posx = 7-B.COL(pos)
                posy = 7-B.ROW(pos)
            else:
                posx = B.COL(pos)
                posy = B.ROW(pos)
            canvas.create_image(mrgx+(posx+0.5)*cell, mrgy+(posy+0.5)*cell, image=imgitem2)

affiche_position()

def execute_cmd():
    cmd= cmd_bar.get()

    global reverse_mode
    global black_mode


    if cmd == "new":
        E.newgame(B)
        E.add_nulle(B)
    elif cmd == "quit":
        tk.quit()
    elif cmd == "undo":
        E.undomove(B)
    elif cmd == "eps":
        print(E.epsilon)
        for i in range(E.epsilon):
            d = 1
    # elif cmd == "auto":
    #     auto_play = not auto_play
    #     print("coups automatiques après le joueur : %s"%auto_play)
    elif cmd == "go":
        E.play_bot(B)
    # elif "gog" in cmd:
    #     E.play_bot(int(cmd.split()[1]),B)
    elif cmd == "droite" :
        E.compteur(1)
        E.lecture(B,E.val_compteur)
    elif cmd == "gauche" :
        E.compteur(-1)
        E.undomove(B)
    elif "setboard" in cmd:
        E.setboard(B,cmd)
    elif cmd == "getboard":
        print(E.getboard(B))
    elif cmd == "nulle_rep":
        print(E.listfen)
    elif cmd == "la_proba":
        show_proba(E)
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
    elif cmd == 'transpo':
        E.use_table = not E.use_table
        print("table de transposition : %s"%E.use_table)
    elif cmd == "black":
        reverse_mode = False
        black_mode = not black_mode
        print("Black mode : %s"%black_mode)
    elif cmd == "reverse":
        black_mode = False
        reverse_mode = not reverse_mode
        print("Reverse mode : %s"%reverse_mode)
    elif cmd == "dist_edge":
        print("distance du roi blanc au bord : %s"%B.dist_roi_bord("blanc"))
    elif "dist" in cmd:
        l = cmd.split()
        x = B.caseStr2Int(l[1])
        y = B.caseStr2Int(l[2])
        print("distance entre les cases {} et {} : {}".format(l[1],l[2],B.DIST(x,y)))
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
    #txt.set("Eval (côté blanc) : %s"%(B.evaluer("blanc")/100))
    txt.set(str(B.pos_id))
    cmd_bar.delete(0,"end")


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
    plt.show()



# gestion des touches ----------------------------------------------------------

def button_push(evt=""): #se déclanche lors de l'appui sur bouton
    execute_cmd()

def on_click(evt):
    casex = (evt.x-40)//80
    casey = (evt.y-40)//80
    if -1<casex<8 and -1<casey<8:
        # if len(cmd_bar.get()) >= 4:
        #     cmd_bar.delete(0,"end")
        if (reverse_mode and B.side2move == "noir") or black_mode:
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
                l = liste[i]
                if l[0] == B.caseStr2Int(cmd_bar.get()):
                    if not B.domove(l[0],l[1],l[2]):
                        continue
                    B.undomove()
                    l2 += [l[1]]
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


# gestion des touches ----------------------------------------------------------
tk.bind_all('<KeyPress-Return>', button_push)
tk.bind_all('<1>', on_click)
tk.bind_all('<3>',on_click2)
# tk.bind_all('<KeyPress-Control_L>', bot_play)
tk.bind_all('<Up>', bot_play)
tk.bind_all('<Right>', droite)
tk.bind_all('<Left>', gauche)

box = Frame(tk)
cmd_bar = Entry(box)
btn = Button(box, text='ENTRER', command=button_push)



#Pack()
box.pack(expand=YES)
cmd_bar.grid(row=0, column=0, sticky=W)
btn.grid(row=0, column=1, sticky=W)
canvas.pack()
tabl.pack()
#Pack()




tk.mainloop()
