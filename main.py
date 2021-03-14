from board import *
from tkinter import *
import os
import time

tk = Tk()
tk.title("Chess")
tk.wm_attributes("-topmost", 1)
tk.resizable(width=False,height=False)
tk.maxsize(740,600)

canvas = Canvas(tk, width=576, height=576,bd=0, highlightthickness=0)


B = Board() #création échéquier

imglist = [] #liste des images à afficher (pièces)


def affiche_position():
    global imglist #besoin d'etre global sinon disparition des images
    imglist = []

    folderName="pieces"
    liste=os.listdir(folderName) # =>recupere le nom de tous les fichiers d'un dossier
    for j in range(8):
        for i in range(8):
            mrgx = 32
            mrgy = 32
            cell = 64

            if (i+j)%2 == 0: col = '#f6f6f6'
            else: col = '#45863d'

            canvas.create_text(mrgx//2,cell*(j+1),text=str(8-j))
            canvas.create_text(cell*(i+1),mrgy//2,text=chr(65+i))
            canvas.create_rectangle(mrgx+i*cell,mrgy+j*cell,mrgx+(i+1)*cell,mrgy+(j+1)*cell,fill=col)

            ma_piece = B.cases[i+8*j]
            # canvas.create_text(mrgx+(i+0.5)*cell, mrgy+(j+0.5)*cell, text=ma_piece.nom[0], fill=ma_col, font="Helvetica")

            if ma_piece.nom != ma_piece.nomPiece[0]:
                pos = ma_piece.nomPiece.index(ma_piece.nom)-1
                if ma_piece.couleur == "noir":
                    pos += 6
                imgfile = folderName +'/'+liste[pos] ## strchemin:str, chemin d'accès à l'image
                imglist += [PhotoImage(file=imgfile)]
                canvas.create_image(mrgx+(i+0.5)*cell, mrgy+(j+0.5)*cell, image=imglist[i+8*j])
            else:
                imglist += [""]
affiche_position()



def button_push(evt=""): #se déclanche lors de l'appui sur bouton
    cmd= cmd_bar.get()

    if cmd == "new":
        B.__init__()
    elif cmd == "quit":
        tk.quit()
    elif cmd == "undo":
        B.undo_move()
    elif len(cmd) == 4:
        B.move_piece(cmd)
    affiche_position()
    cmd_bar.delete(0,"end")

def on_click(evt):
    casex = (evt.x-32)//64
    casey = (evt.y-32)//64
    if casex>=0 and casey >=0:
        # if len(cmd_bar.get()) >= 4:
        #     cmd_bar.delete(0,"end")
        c = B.coords[casex+8*casey]
        cmd_bar.insert("end",c)
        if len(cmd_bar.get()) >= 4:
            button_push()
def on_click2(evt):
    if cmd_bar.get() == "":
        cmd_bar.insert("end","undo")
    button_push()

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
