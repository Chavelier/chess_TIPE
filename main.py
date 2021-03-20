from board import *
from tkinter import *
from engine import *
import os

tk = Tk()
tk.title("Chess")
tk.wm_attributes("-topmost", 1)
tk.resizable(width=False,height=False)
tk.maxsize(740,600)

canvas = Canvas(tk, width=576, height=576,bd=0, highlightthickness=0)


B = Board() #création échéquier
E = Engine() #creation engine

imglist = [] #liste des images à afficher (pièces)

imgfile2 = "pieces/z_case_indic.png"
imgitem2 = PhotoImage(file=imgfile2)

def affiche_position(l=[]):
    global imglist #besoin d'etre global sinon disparition des images
    imglist = []

    mrgx = 32
    mrgy = 32
    cell = 64

    folderName="pieces"
    liste=os.listdir(folderName) # =>recupere le nom de tous les fichiers d'un dossier
    for j in range(8):
        for i in range(8):
            if (i+j)%2 == 0: col = '#f6f6f6'
            else: col = '#45863d'

            canvas.create_text(mrgx//2,cell*(j+1),text=str(8-j))
            canvas.create_text(cell*(i+1),mrgy//2,text=chr(65+i))
            canvas.create_rectangle(mrgx+i*cell,mrgy+j*cell,mrgx+(i+1)*cell,mrgy+(j+1)*cell,fill=col)

            ma_piece = B.cases[i+8*j]
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
            canvas.create_image(mrgx+(B.COL(pos)+0.5)*cell, mrgy+(B.ROW(pos)+0.5)*cell, image=imgitem2)

affiche_position()

def execute_cmd():
    cmd= cmd_bar.get()

    if cmd == "new":
        E.newgame(B)
    elif cmd == "quit":
        tk.quit()
    elif cmd == "undo":
        E.undomove(B)
    # elif cmd == "go":
    #     E
    elif len(cmd) >= 4:
        E.usermove(B,cmd)
    affiche_position()
    cmd_bar.delete(0,"end")



# gestion des touches ----------------------------------------------------------

def button_push(evt=""): #se déclanche lors de l'appui sur bouton
    execute_cmd()

def on_click(evt):
    casex = (evt.x-32)//64
    casey = (evt.y-32)//64
    if casex>=0 and casey >=0:
        # if len(cmd_bar.get()) >= 4:
        #     cmd_bar.delete(0,"end")
        c = B.coord[casex+8*casey]
        cmd_bar.insert("end",c)
        taille_texte = len(cmd_bar.get())
        if taille_texte == 2:
            liste = B.gen_moves_list()
            l2=[]
            for i in range(len(liste)):
                if liste[i][0] == B.caseStr2Int(cmd_bar.get()):
                    l2 += [liste[i][1]]
            affiche_position(l2)
        elif taille_texte >= 4:
            execute_cmd()
def on_click2(evt):
    if cmd_bar.get() == "":
        cmd_bar.insert("end","undo")
    execute_cmd()



# gestion des touches ----------------------------------------------------------
tk.bind_all('<KeyPress-Return>', button_push)
tk.bind_all('<1>', on_click)
tk.bind_all('<3>',on_click2)

box = Frame(tk)
cmd_bar = Entry(box)
btn = Button(box, text='ENTRER', command=button_push)



#Pack()
box.pack(expand=YES)
cmd_bar.grid(row=0, column=0, sticky=W)
btn.grid(row=0, column=1, sticky=W)
canvas.pack()
#Pack()




tk.mainloop()
