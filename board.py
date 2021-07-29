from piece import *

# import os
# from PIL import Image, ImageTk ## Importation des modules utiles dans PIL

# import tkFont
# my_font = tkFont.Font(family="Helvetica", size=36 ,weight="bold")

class Board:
    """Le plateau de jeu"""

    coord = [
    'a8','b8','c8','d8','e8','f8','g8','h8',
    'a7','b7','c7','d7','e7','f7','g7','h7',
    'a6','b6','c6','d6','e6','f6','g6','h6',
    'a5','b5','c5','d5','e5','f5','g5','h5',
    'a4','b4','c4','d4','e4','f4','g4','h4',
    'a3','b3','c3','d3','e3','f3','g3','h3',
    'a2','b2','c2','d2','e2','f2','g2','h2',
    'a1','b1','c1','d1','e1','f1','g1','h1'
    ]

    def __init__(self):
        self.init()


    def init(self):

        #initialisation de l'échéquier
        self.cases = [
        Piece('TOUR','noir'), Piece('CAVALIER','noir'), Piece('FOU','noir'), Piece('DAME','noir'), Piece('ROI','noir'), Piece('FOU','noir'), Piece('CAVALIER','noir'), Piece('TOUR','noir'),
        Piece('PION','noir'), Piece('PION','noir'), Piece('PION','noir'), Piece('PION','noir'), Piece('PION','noir'), Piece('PION','noir'), Piece('PION','noir'), Piece('PION','noir'),
        Piece('VIDE'), Piece('VIDE'), Piece('VIDE'), Piece('VIDE'), Piece('VIDE'), Piece('VIDE'), Piece('VIDE'), Piece('VIDE'), Piece('VIDE'), Piece('VIDE'), Piece('VIDE'), Piece('VIDE'), Piece('VIDE'), Piece('VIDE'), Piece('VIDE'), Piece('VIDE'),
        Piece('VIDE'), Piece('VIDE'), Piece('VIDE'), Piece('VIDE'), Piece('VIDE'), Piece('VIDE'), Piece('VIDE'), Piece('VIDE'), Piece('VIDE'), Piece('VIDE'), Piece('VIDE'), Piece('VIDE'), Piece('VIDE'), Piece('VIDE'), Piece('VIDE'), Piece('VIDE'),
        Piece('PION','blanc'), Piece('PION','blanc'), Piece('PION','blanc'), Piece('PION','blanc'), Piece('PION','blanc'), Piece('PION','blanc'), Piece('PION','blanc'), Piece('PION','blanc'),
        Piece('TOUR','blanc'), Piece('CAVALIER','blanc'), Piece('FOU','blanc'), Piece('DAME','blanc'), Piece('ROI','blanc'), Piece('FOU','blanc'), Piece('CAVALIER','blanc'), Piece('TOUR','blanc')
        ]

        self.histo = [] #historique des coups

        self.side2move='blanc'
        self.ep=-1 # la case ou l'on peut prendre en passant
        self.history=[] # historique des coups
        self.ply=0 # nb de coups ('e2e4' 'e7e5' = 1 coup)

        # position des ROI, utile pour les test d'echec
        self.pos_roi_b = 60
        self.pos_roi_n = 4


        # droit de roque
        self.white_can_castle_56=True
        self.white_can_castle_63=True
        self.black_can_castle_0=True
        self.black_can_castle_7=True
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
        self.val_cases_roi_blanc = [
        4,3,2,0,0,2,4,4,
        4,3,2,0,0,2,4,4,
        8,4,2,0,0,2,4,8,
        8,4,2,0,0,2,4,8,
        12,10,10,8,8,10,10,12,
        12,10,10,10,10,10,10,12,
        15,12,10,10,10,10,12,15,
        16,20,12,10,10,12,20,16
        ]
        self.val_cases_roi_noir = [
        16, 20, 12, 10, 10, 12, 20, 16,
        15,12, 10, 10, 10, 10, 12, 15,
        12, 10, 10, 10, 10, 10, 10, 12,
        12, 10, 10, 8, 8, 10, 10, 12,
        8, 4, 2, 0, 0, 2, 4, 8,
        8, 4, 2, 0, 0, 2, 4, 8,
        4, 4, 2, 0, 0, 2, 3, 4,
        4, 4, 2, 0, 0, 2, 3, 4]
        self.val_cases_cavalier_blanc = [
        0,4,6,6,6,6,4,0,
        4,7,10,10,10,10,7,4,
        6,10,12,15,15,12,10,6,
        6,10,15,20,20,15,10,6,
        6,10,15,20,20,15,10,6,
        6,10,12,15,15,12,10,6,
        4,6,10,10,10,10,6,4,
        0,4,6,6,6,6,4,0
        ]
        self.val_cases_cavalier_noir = [
        0, 4, 6, 6, 6, 6, 4, 0,
        4, 6, 10, 10, 10, 10, 6, 4,
        6, 10, 12, 15, 15, 12, 10, 6,
        6, 10, 15, 20, 20, 15, 10, 6,
        6, 10, 15, 20, 20, 15, 10, 6,
        6, 10, 12, 15, 15, 12, 10, 6,
        4, 7, 10, 10, 10, 10, 7, 4,
        0, 4, 6, 6, 6, 6, 4, 0]
        self.val_cases_dame_blanc = [
        0,4,4,8,8,4,4,0,
        4,10,10,10,10,10,10,4,
        4,10,12,14,14,12,10,4,
        4,12,16,18,18,16,12,4,
        4,10,20,18,18,20,10,4,
        4,14,20,14,14,20,14,4,
        4,10,10,10,10,10,10,4,
        0,4,4,8,8,4,4,0
        ]
        self.val_cases_dame_noir = [
        0, 4, 4, 8, 8, 4, 4, 0,
        4, 10, 10, 10, 10, 10, 10, 4,
        4, 14, 20, 14, 14, 20, 14, 4,
        4, 10, 20, 18, 18, 20, 10, 4,
        4, 12, 16, 18, 18, 16, 12, 4,
        4, 10, 12, 14, 14, 12, 10, 4,
        4, 10, 10, 10, 10, 10, 10, 4,
        0, 4, 4, 8, 8, 4, 4, 0
        ]
        self.val_cases_pion_blanc = [
        20,20,20,20,20,20,20,20,
        20,20,20,20,20,20,20,20,
        4,10,12,14,14,12,10,4,
        4,10,10,12,12,10,10,4,
        4,10,16,20,20,16,10,4,
        4,12,18,14,14,18,12,4,
        0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0
        ]
        self.val_cases_pion_noir = [
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0,
        4, 12, 18, 14, 14, 18, 12, 4,
        4, 10, 16, 20, 20, 16, 10, 4,
        4, 10, 10, 12, 12, 10, 10, 4,
        4, 10, 12, 14, 14, 12, 10, 4,
        20, 20, 20, 20, 20, 20, 20, 20,
        20, 20, 20, 20, 20, 20, 20, 20
        ]
        self.val_cases_fou_blanc = [
        0,4,4,4,4,4,4,0,
        4,8,8,8,8,8,8,4,
        4,10,12,14,14,12,10,4,
        4,12,12,14,14,12,12,4,
        4,10,18,14,14,18,10,4,
        4,14,14,14,14,14,14,4,
        4,18,10,8,8,10,18,4,
        8,2,2,2,2,2,2,8
        ]
        self.val_cases_fou_noir = [
        8, 2, 2, 2, 2, 2, 2, 8,
        4, 18, 10, 8, 8, 10, 18, 4,
        4, 14, 14, 14, 14, 14, 14, 4,
        4, 10, 18, 14, 14, 18, 10, 4,
        4, 12, 12, 14, 14, 12, 12, 4,
        4, 10, 12, 14, 14, 12, 10, 4,
        4, 8, 8, 8, 8, 8, 8, 4,
        0, 4, 4, 4, 4, 4, 4, 0
        ]
        self.val_cases_tour_blanc = [
        10,10,10,10,10,10,10,10,
        13,20,20,20,20,20,20,13,
        0,6,6,6,6,6,6,0,
        0,6,6,6,6,6,6,0,
        0,6,6,6,6,6,6,0,
        0,6,6,6,6,6,6,0,
        0,6,6,6,6,6,6,0,
        6,6,10,13,13,10,6,6
        ]
        self.val_cases_tour_noir = [
        6, 6, 10, 13, 13, 10, 6, 6,
        0, 6, 6, 6, 6, 6, 6, 0,
        0, 6, 6, 6, 6, 6, 6, 0,
        0, 6, 6, 6, 6, 6, 6, 0,
        0, 6, 6, 6, 6, 6, 6, 0,
        0, 6, 6, 6, 6, 6, 6, 0,
        13, 20, 20, 20, 20, 20, 20, 13,
        10, 10, 10, 10, 10, 10, 10, 10
        ]
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes


    # def move_piece(self,cmd):
    #     """controle le mvt des pieces. cmd = "e2e4" par ex"""
    #     start = cmd[0:2]
    #     end = cmd[2:4]
    #     piece_en_mvt = self.cases[Board.coords.index(start)]
    #     if piece_en_mvt != Piece('VIDE'):
    #         self.histo += [(cmd,self.cases[Board.coords.index(end)].nom,self.cases[Board.coords.index(end)].couleur)] #on ajoute la ligne à l'historique
    #         self.cases[Board.coords.index(start)] = Piece('VIDE') #remplace la position de départ par du vide
    #         self.cases[Board.coords.index(end)] = piece_en_mvt #remplace la position finale par la piece
    #
    #
    # def undo_move(self):
    #     if self.histo == []:
    #         return
    #     start = self.histo[-1][0][2:4]
    #     end = self.histo[-1][0][0:2]
    #     piece_en_mvt = self.cases[Board.coords.index(start)]
    #     self.cases[Board.coords.index(start)] = Piece(self.histo[-1][1],self.histo[-1][2]) #remplace la position de départ par la pièce mangée précedemment
    #     self.cases[Board.coords.index(end)] = piece_en_mvt #remplace la position finale par la piece
    #     del self.histo[-1]

<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes

>>>>>>> Stashed changes
    ####################################################################


    def changeTrait(self):
        "Change le tour de jeu"
        if(self.side2move=='blanc'):
            self.side2move='noir'
        else:
            self.side2move='blanc'


    def oppColor(self,c):
        "Renvoi la couleur opposée à 'c'"
        if(c=='blanc'):
            return 'noir'
        else:
            return 'blanc'


    def gen_moves_list(self,color='',dontCallIsAttacked=False):
        """Renvoi tous les coups possibles pour la couleur choisie.
        Si la couleur n'est pas donnée c'est le côté qui joue.
        dontCallIsAttacked empèche les boucles infinies,
        à cause de la fonction is_attacked() qui appelle cette fonction.
        Un coup est défini avec :
        - l'id de la case de départ (pos1)
        - l'id de la case d'arrivée (pos2)
        - le nom de la pièce pour les promotions '','q','r','b','n'
          (queen, rook, bishop, knight)
        """

        if(color==''):
            color=self.side2move
        mList=[]

        # For each 'piece' on the board (pos1 = 0 to 63)
        for pos1,piece in enumerate(self.cases):

            # on passe si la couleur de la pièce n'est pas celle du trait
            if piece.couleur!=color:
                continue

            if(piece.nom=='ROI'):
                mList+=piece.pos2_roi(pos1,self.oppColor(color),self,dontCallIsAttacked)
                continue

            elif(piece.nom=='DAME'): # DAME = TOUR + FOU
                mList+=piece.pos2_tour(pos1,self.oppColor(color),self)
                mList+=piece.pos2_fou(pos1,self.oppColor(color),self)
                continue

            elif(piece.nom=='TOUR'):
                mList+=piece.pos2_tour(pos1,self.oppColor(color),self)
                continue

            elif(piece.nom=='CAVALIER'):
                mList+=piece.pos2_cavalier(pos1,self.oppColor(color),self)
                continue

            elif(piece.nom=='FOU'):
                mList+=piece.pos2_fou(pos1,self.oppColor(color),self)
                continue

            if(piece.nom=='PION'):
                mList+=piece.pos2_pion(pos1,piece.couleur,self)
                continue

        return mList

    ####################################################################
    def tri_move(self,ma_list):
        """Renvoi la liste des coups trié avec les prises d'abord"""
        list_fin = []
        for (pos1,pos2,p) in ma_list:
            if self.cases[pos2].isEmpty():
                # print("case vide")
                list_fin.append((pos1,pos2,p))
            else:
                # print(str(pos2) + " " + self.caseInt2Str(pos2))
                list_fin.insert(0,(pos1,pos2,p))
        # if list_fin != ma_list: print(list_fin)
        return list_fin
    ####################################################################

    def domove(self,depart,arrivee,promote):
        """Déplace la pièce sur l'échéquier de la position
        'depart' à 'arrivee' (0..63) respectant les coups :
        - prise en passant
        - promotion
        - droits au roque
        Renvoi :
        - TRUE si le ROI n'est pas en échec après ce coup
        - FALSE sinon, le coup est alors annulé
        """

        # Debugging tests
        #if(self.cases[depart].isEmpty()):
        #    print('domove() ERROR : asked for an empty square move : ',depart,arrivee,promote)
        #    return
        #if(int(depart)<0 or int(depart)>63):
        #    print('domove() ERROR : incorrect FROM square number : ',depart)
        #    return
        #if(int(arrivee)<0 or int(arrivee)>63):
        #    print('domove() ERROR : incorrect TO square number : ',arrivee)
        #    return
        #if(not(promote=='' or promote=='q' or promote=='r' or promote=='n' or promote=='b')):
        #    print('domove() ERROR : incorrect promote : ',promote)
        #    return

		# Informations à sauvegarder dans l'historique
        pieceDeplacee=self.cases[depart]
        piecePrise=self.cases[arrivee]
        isEp=False # utilisé pour annuler prise en passant
        histEp=self.ep # sauvegarde l'actuelle case de prise en passant
        hist_roque_56=self.white_can_castle_56
        hist_roque_63=self.white_can_castle_63
        hist_roque_0=self.black_can_castle_0
        hist_roque_7=self.black_can_castle_7
        flagViderEp=True # booléen pour effacer ou non la case de prise en passant

        # deplacement de la pièce
        self.cases[arrivee]=self.cases[depart]
        self.cases[depart]=Piece('VIDE')

        self.ply+=1

        # PION deplacé -------------------------------------
        if(pieceDeplacee.nom=='PION'):

            # PION blanc
            if(pieceDeplacee.couleur=='blanc'):

                # Si le coup est en passant
                if(self.ep==arrivee):
                    piecePrise=self.cases[arrivee+8] # on prend le PION noir
                    self.cases[arrivee+8]=Piece('VIDE')
                    isEp=True

                # Le PION blanc avance de 2 cases
                # alors le PION noir peut prendre en passant au prochain coup
                elif(self.ROW(depart)==6 and self.ROW(arrivee)==4):
                    self.ep=arrivee+8
                    flagViderEp=False

            # PION noir
            else:

                if(self.ep==arrivee):
                    piecePrise=self.cases[arrivee-8]
                    self.cases[arrivee-8]=Piece('VIDE')
                    isEp=True

                elif(self.ROW(depart)==1 and self.ROW(arrivee)==3):
                    self.ep=arrivee-8
                    flagViderEp=False

        # une TOUR bouge--------------------------------------
        # on actualise les droits au roque

        elif(pieceDeplacee.nom=='TOUR'):

            # TOUR blanche
            if(pieceDeplacee.couleur=='blanc'):
                if(depart==56):
                    self.white_can_castle_56=False
                elif(depart==63):
                    self.white_can_castle_63=False

            # TOUR noire
            else:
                if(depart==0):
                    self.black_can_castle_0=False
                elif(depart==7):
                    self.black_can_castle_7=False

        # le ROI bouge-----------------------------------------

        elif(pieceDeplacee.nom=='ROI'):

            # ROI blanc
            if(pieceDeplacee.couleur=='blanc'):
                self.pos_roi_b = arrivee
                # on bouge de la case de départ
                if(depart==60):
                    # alors on interdit tous les roques quelque soit le mouvement
                    self.white_can_castle_56=False
                    self.white_can_castle_63=False

                    # si on avait fait un mouvement de roque alors on bouge la TOUR
                    if(arrivee==58):
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
                        self.cases[56]=Piece()
                        self.cases[59]=Piece('TOUR','blanc')

                    elif(arrivee==62):
                        self.cases[63]=Piece()
=======
                        self.roqueB = True
                        self.cases[56]=Piece('VIDE')
                        self.cases[59]=Piece('TOUR','blanc')

                    elif(arrivee==62):
                        self.roqueB = True
                        self.cases[63]=Piece('VIDE')
>>>>>>> Stashed changes
=======
                        self.roqueB = True
                        self.cases[56]=Piece('VIDE')
                        self.cases[59]=Piece('TOUR','blanc')

                    elif(arrivee==62):
                        self.roqueB = True
                        self.cases[63]=Piece('VIDE')
>>>>>>> Stashed changes
=======
                        self.roqueB = True
                        self.cases[56]=Piece('VIDE')
                        self.cases[59]=Piece('TOUR','blanc')

                    elif(arrivee==62):
                        self.roqueB = True
                        self.cases[63]=Piece('VIDE')
>>>>>>> Stashed changes
                        self.cases[61]=Piece('TOUR','blanc')

            # ROI noir
            else:
                self.pos_roi_n = arrivee
                if(depart==4):
                    self.black_can_castle_0=False
                    self.black_can_castle_7=False

                    if(arrivee==6):
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
                        self.cases[7]=Piece()
                        self.cases[5]=Piece('TOUR','noir')

                    elif(arrivee==2):
                        self.cases[0]=Piece()
=======
                        self.roqueN = True
                        self.cases[7]=Piece('VIDE')
                        self.cases[5]=Piece('TOUR','noir')

                    elif(arrivee==2):
                        self.roqueN = True
                        self.cases[0]=Piece('VIDE')
>>>>>>> Stashed changes
=======
                        self.roqueN = True
                        self.cases[7]=Piece('VIDE')
                        self.cases[5]=Piece('TOUR','noir')

                    elif(arrivee==2):
                        self.roqueN = True
                        self.cases[0]=Piece('VIDE')
>>>>>>> Stashed changes
=======
                        self.roqueN = True
                        self.cases[7]=Piece('VIDE')
                        self.cases[5]=Piece('TOUR','noir')

                    elif(arrivee==2):
                        self.roqueN = True
                        self.cases[0]=Piece('VIDE')
>>>>>>> Stashed changes
                        self.cases[3]=Piece('TOUR','noir')

        # fin du problème de certaines pièces-----------------------------------------------

        # N'importe quel coup annule la case de prise en passant
        if(flagViderEp==True):
            self.ep=-1

        # Promotion : le PION est changé en n'importe quelle pièce
        if(promote!=''):
            if(promote=='q'):
                self.cases[arrivee]=Piece('DAME',self.side2move)
            elif(promote=='r'):
                self.cases[arrivee]=Piece('TOUR',self.side2move)
            elif(promote=='n'):
                self.cases[arrivee]=Piece('CAVALIER',self.side2move)
            elif(promote=='b'):
                self.cases[arrivee]=Piece('FOU',self.side2move)

        # on change le côté de jeu
        self.changeTrait()

        # et on sauvegarde le coup dans l'historique
        self.history.append((depart,\
        arrivee,\
        pieceDeplacee,\
        piecePrise,\
        isEp,\
        histEp,\
        promote,\
        hist_roque_56,\
        hist_roque_63,\
        hist_roque_0,\
        hist_roque_7))

        # Si le roi est en échec on annule le coup et on retourne FALSE
        if(self.in_check(self.oppColor(self.side2move))):
            self.undomove()
            return False
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
        return True

    ####################################################################

    def undomove(self):
        """annule le dernier coup dans l'historique"""

        if(len(self.history)==0): # on évite le cas de la liste vide
            print('No move played')
            return

        # dernier coup de l'historique est : self.historique[-1]
        lastmove=self.history[-1]

        pos1=lastmove[0]
        pos2=lastmove[1]
        piece_deplacee=lastmove[2]
        piece_prise=lastmove[3]
        isEp=lastmove[4]
        ep=lastmove[5]
        promote=lastmove[6]
        self.white_can_castle_56=lastmove[7]
        self.white_can_castle_63=lastmove[8]
        self.black_can_castle_0=lastmove[9]
        self.black_can_castle_7 =lastmove[10]

        self.ply-=1

        # on change le cote qui joue
        self.changeTrait()

        # on replace la pièce sur la case 'pos1'
        self.cases[pos1]=self.cases[pos2]

        # case sur laquelle on peut prendre en passant
        self.ep=ep

        # si on annule une promotion la pièce était un PION
        if(promote!=''):
            self.cases[pos1]=Piece('PION',self.side2move)

        # on replace la pièce capturée sur 'pos2'
        self.cases[pos2]=piece_prise

        # si c'est un PION il faut gérer la prise en passant-------------------
        if(self.cases[pos1].nom=='PION'):
            if(isEp):
                self.cases[pos2]=Piece('VIDE')
                if(self.cases[pos1].couleur=='noir'):
                    self.cases[pos2-8]=Piece('PION','blanc')
                else:
                    self.cases[pos2+8]=Piece('PION','noir')

        # replacer le ROI -----------------------------------------------
        elif(self.cases[pos1].nom=='ROI'):

            # ROI blanc
            if(self.cases[pos1].couleur=='blanc'):
                # on regarde si la pos originale était sa position initiale
                self.pos_roi_b = pos1
                if(pos1==60):
                    # si c'était un roque on replace la TOUR
                    if(pos2==58):
                        self.cases[56]=Piece('TOUR','blanc')
                        self.cases[59]=Piece('VIDE')
                    elif(pos2==62):
                        self.cases[63]=Piece('TOUR','blanc')
                        self.cases[61]=Piece('VIDE')
            # ROI noir
            else:
                self.pos_roi_n = pos1
                if(pos1==4):
                    if(pos2==2):
                        self.cases[0]=Piece('TOUR','noir')
                        self.cases[3]=Piece('VIDE')
                    elif(pos2==6):
                        self.cases[7]=Piece('TOUR','noir')
                        self.cases[5]=Piece('VIDE')

        # on supprime le dernier coup de l'historique
        self.history.pop()

    ####################################################################

    def in_check(self,couleur):
        """Renvoi TRUE ou FALSE
        si le ROI de 'couleur' passée en argument est en échec"""

        # on cherche la case du ROI
        # TODO: faire un test d'échec plus optimisé
        # for i in range(0,64):
        #     if(self.cases[i].nom=='ROI' and self.cases[i].couleur==couleur):
        #         pos=i
        #         break
        if couleur == "blanc":
            pos = self.pos_roi_b
        else:
            pos = self.pos_roi_n

        return self.is_attacked(pos,self.oppColor(couleur))


    def is_attacked(self,pos,couleur):
        """Renvoi TRUE ou FALSE si la 'pos' est une case de destination
        pour une pièce de la couleur 'couleur'.
        Si c'est le cas on peut dire que la case est attaquée par la 'couleur'.
        Cette fonction est utile pour 'in_check' et le roque."""

        mList=self.gen_moves_list(couleur,True) #on ne rappelle pas la fonction is_attacked

        for pos1,pos2,promote in mList:
            if(pos2==pos):
                return True
        return False

    ####################################################################

    def caseStr2Int(self,c):
        """'c' given in argument is a square name like 'e2'
        "This functino returns a square number like 52"""

        err=(
        'The square name must be 2 caracters i.e. e2,e4,b1...',
        'Incorrect square name. Please enter i.e. e2,e4,b1...'
        )
        letters=('a','b','c','d','e','f','g','h')
        numbers=('1','2','3','4','5','6','7','8')

        if(len(c)!=2):
            print(err[0])
            return -1

        if(c[0] not in letters):
            print(err[1])
            return -1

        if(c[1] not in numbers):
            print(err[1])
            return -1

        return self.coord.index(c)

    def caseInt2Str(self,i):
        """Given in argument : an integer between 0 and 63
        Returns a string like 'e2'"""

        err=(
        'Square number must be in 0 to 63',
        )
        letters=('a','b','c','d','e','f','g','h')
        numbers=('1','2','3','4','5','6','7','8')

        if(i<0 or i>63):
            print(err[0])
            return

        return self.coord[i]

    ####################################################################

    def evaluer(self,couleur=''):
        """Fonction d'évaluation d'une position"""

        if couleur == '':
            couleur = self.side2move
         #### QUAND REVERSE????
            #self.val_cases_fou.reverse()
            #self.val_cases_dame.reverse()
            #self.val_cases_roi.reverse()
            #self.val_cases_pion.reverse()
            #self.val_cases_cavalier.reverse()
            #self.val_cases_tour.reverse()





        WhiteScore=0
        BlackScore=0

        fou_b = 0
        fou_n = 0

        #structures des pions sur les colonnes
        struct_pion_b = [0,0,0,0,0,0,0,0]
        struct_pion_n = [0,0,0,0,0,0,0,0]
        pos_tour_b = [] #colonne tour
        pos_tour_n = [] #colonne tour
        coeff = (((-0.5)/30)*self.ply + 1) #Coeff d'incidence pour le controle du centre (plus la partie avance moins on le prend en compte)
        # on regarde chaque cases de l'échequier
        for pos1,piece in enumerate(self.cases):

            # case_c = int(self.is_attacked(pos1,'blanc')) - int(self.is_attacked(pos1,'noir'))
            # WhiteScore += 5*case_c
            # Material score
            if(piece.couleur=='blanc'):
                if piece.nom == "TOUR":
                    pos_tour_b.append(self.COL(pos1))
                    WhiteScore += coeff*self.val_cases_tour_blanc[pos1]
                if piece.nom == "FOU":
                    fou_b += 1
                    WhiteScore += coeff*self.val_cases_fou_blanc[pos1]
                if piece.nom == 'PION':
                    struct_pion_b[self.COL(pos1)] += 1
                    WhiteScore += coeff*self.val_cases_pion_blanc[pos1]
                if piece.nom == 'ROI':
                    WhiteScore += coeff*self.val_cases_roi_blanc[pos1]
                if piece.nom == 'CAVALIER':
                    WhiteScore += coeff*self.val_cases_cavalier_blanc[pos1]
                if piece.nom == 'DAME':
                    WhiteScore += coeff*self.val_cases_dame_blanc[pos1]
                WhiteScore+=piece.valeur
            elif (piece.couleur=='noir'):
                if piece.nom == "TOUR":
                    pos_tour_n.append(self.COL(pos1))
                    BlackScore += coeff*self.val_cases_tour_noir[pos1]
                if piece.nom == "FOU":
                    fou_n += 1
                    BlackScore += coeff*self.val_cases_fou_noir[pos1]
                if piece.nom == 'PION':
                    struct_pion_n[self.COL(pos1)] += 1
                    BlackScore += coeff*self.val_cases_pion_noir[pos1]
                if piece.nom == 'ROI':
                    BlackScore += coeff*self.val_cases_roi_noir[pos1]
                if piece.nom == 'CAVALIER':
                    BlackScore += coeff*self.val_cases_cavalier_noir[pos1]
                if piece.nom == 'DAME':
                    BlackScore += coeff*self.val_cases_dame_noir[pos1]
                # NB : here is for black piece or empty square
                BlackScore+=piece.valeur

        #tours sur colonne ouvertes
        for col in pos_tour_b:
            if struct_pion_b[col] == 0:
                WhiteScore += 30
        for col in pos_tour_n:
            if struct_pion_n[col] == 0:
                BlackScore += 30


        #pions isolés
        sep1 = [-1]
        sep2 = [-1]
        for i in range(8):
            if struct_pion_b[i] == 0:
                sep1.append(i)
            if struct_pion_n[i] == 0:
                sep2.append(i)
        for i in range(1,len(sep1)):
            if len(struct_pion_b[sep1[i-1]+1 : sep1[i]]) == 1:
                WhiteScore -= 40
        for i in range(1,len(sep2)):
            if len(struct_pion_n[sep2[i-1]+1 : sep2[i]]) == 1:
                BlackScore -= 40



        if fou_b >= 2:
            WhiteScore += 30
        if fou_n >= 2:
            BlackScore += 30

        if(couleur=='blanc'):
            return WhiteScore-BlackScore
        else:
            return BlackScore-WhiteScore


    ####################################################################

    def setboard(self,fen):

        """Set the board to the FEN position given. i.e. :
        rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - - 0
        Returns TRUE or FALSE if done or not.
        If not : print errors.
        """

        f=fen.split()
        err=""

        if(len(f)!=6):
            err+="Wrong FEN notation. It should be :\n"
            err+="[pieces] [side to move] [castle rights] [ep] [plys] [move number]\n"
            err+="i.e. : rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1\n"
            print(err)
            return False

        self.init()
        self.white_can_castle_56=False
        self.white_can_castle_63=False
        self.black_can_castle_0=False
        self.black_can_castle_7=False

        fen =   f[0] # rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR
        trait = f[1] # b ou w (black,white)
        roque = f[2] # KQkq
        ep =    f[3] # e3
        rule50= f[4] # 0 (half-moves since start of game for 50 moves rule)
        num =   f[5] # move number

        # Setting pieces
        i=0
        for c in fen:
            if(c=='k'):
                self.cases[i]=Piece('ROI','noir')
                i=i+1
            elif(c=='q'):
                self.cases[i]=Piece('DAME','noir')
                i=i+1
            elif(c=='r'):
                self.cases[i]=Piece('TOUR','noir')
                i=i+1
            elif(c=='n'):
                self.cases[i]=Piece('CAVALIER','noir')
                i=i+1
            elif(c=='b'):
                self.cases[i]=Piece('FOU','noir')
                i=i+1
            elif(c=='p'):
                self.cases[i]=Piece('PION','noir')
                i=i+1
            elif(c=='K'):
               self.cases[i]=Piece('ROI','blanc')
               i=i+1
            elif(c=='Q'):
               self.cases[i]=Piece('DAME','blanc')
               i=i+1
            elif(c=='R'):
                self.cases[i]=Piece('TOUR','blanc')
                i=i+1
            elif(c=='N'):
                self.cases[i]=Piece('CAVALIER','blanc')
                i=i+1
            elif(c=='B'):
                self.cases[i]=Piece('FOU','blanc')
                i=i+1
            elif(c=='P'):
                self.cases[i]=Piece('PION','blanc')
                i=i+1
            elif(c=='/'):
                pass
            else: # a number of empty squares is given
                try:
                    nb=int(c)
                except ValueError:
                    print('Error : wrong FEN. Integer expected.')
                    return
                cpt=0
                while(cpt<nb):
                    self.cases[i]=Piece('VIDE')
                    cpt=cpt+1
                    i=i+1

        # Checking number of squares
        if(i!=64):
            print('Error : wrong FEN.')
            self.init()
            return False

        # Site to move
        if(trait=='b'):
            self.side2move='noir'
        else:
            self.side2move='blanc'

        # Castle rights
        if(roque!='-'):
            if('K' in roque):
                self.white_can_castle_63=True
            if('Q' in roque):
                self.white_can_castle_56=True
            if('k' in roque):
                self.black_can_castle_7=True
            if('q' in roque):
                self.black_can_castle_0=True

        # Prise "en passant"
        if(ep not in self.coord):
            self.ep=-1
        else:
            self.ep=self.coord.index(ep)

        # TODO
        # half-moves since start of game for 50 moves rule

        # TODO
        # move number

        return True

    ####################################################################

    def getboard(self,for_nulle=False):

        """Returns the FEN notation of the current board. i.e. :
        rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - - 0
        """

        emptySq=0 # couting empty squares
        s='' # constructring the FEN string

        # Parsing each board square (i = 0 to 63)
        for i,piece in enumerate(self.cases):

            p=piece.nom
            c=piece.couleur

            if(emptySq==8):
                s+='8'
                emptySq=0

            if(i and i%8==0):
                if(emptySq>0):
                    s+=str(emptySq)
                    emptySq=0
                s+='/'

            if(piece.isEmpty()):
                emptySq+=1

            elif(p=='ROI'):
                if(emptySq>0):
                    s+=str(emptySq)
                    emptySq=0
                if(c=='noir'):
                    s+='k'
                else:
                    s+='K'

            elif(p=='DAME'):
                if(emptySq>0):
                    s+=str(emptySq)
                    emptySq=0
                if(c=='noir'):
                    s+='q'
                else:
                    s+='Q'

            elif(p=='TOUR'):
                if(emptySq>0):
                    s+=str(emptySq)
                    emptySq=0
                if(c=='noir'):
                    s+='r'
                else:
                    s+='R'

            elif(p=='CAVALIER'):
                if(emptySq>0):
                    s+=str(emptySq)
                    emptySq=0
                if(c=='noir'):
                    s+='n'
                else:
                    s+='N'

            elif(p=='FOU'):
                if(emptySq>0):
                    s+=str(emptySq)
                    emptySq=0
                if(c=='noir'):
                    s+='b'
                else:
                    s+='B'

            elif(p=='PION'):
                if(emptySq>0):
                    s+=str(emptySq)
                    emptySq=0
                if(c=='noir'):
                    s+='p'
                else:
                    s+='P'

        if(emptySq>0):
            s+=str(emptySq)

        if for_nulle:
            return s

        # b or w (black,white)
        if(self.side2move=='blanc'):
            s+=' w '
        else:
            s+=' b '

        # Castle rights (KQkq)
        no_castle_right=True
        if(self.white_can_castle_63):
            s+='K'
            no_castle_right=False
        if(self.white_can_castle_56):
            s+='Q'
            no_castle_right=False
        if(self.black_can_castle_7):
            s+='k'
            no_castle_right=False
        if(self.black_can_castle_0):
            s+='q'
            no_castle_right=False
        if(no_castle_right):
            s+='-'

        # prise en passant e3
        if(self.ep!=-1):
            s+=' '+self.coord[self.ep]
        else:
            s+=' -'

        # TODO
        # number of half-moves for 50 moves rule
        s+=' -'

        # numéro du coup
        s+=' '+str(int(len(self.history)/2))

        return s

<<<<<<< Updated upstream
=======
    ####################################################################

    def dist_roi(self):
        return DIST(pos_roi_b,pos_roi_n)

    def dist_roi_centre(self,col):
        if col == "blanc":
            pos = self.pos_roi_b
        else:
            pos = self.pos_roi_n

        liste = [27,28,35,36]

        return min(self.DIST(pos,27),self.DIST(pos,28),self.DIST(pos,35),self.DIST(pos,36))



    def dist_roi_bord(self,col):
        # edge_list = [0,1,2,3,4,5,6,7,8,15,16,23,24,31,32,39,40,47,48,55,56,57,60,61,62,63]
        if col == "blanc":
            d = self.pos_roi_b
        else:
            d = self.pos_roi_n
        row = self.ROW(d) ; col = self.COL(d)
        cnorm = min(col,7-col) ; rnorm = min(row,7-row)

        return min(cnorm,rnorm)

    ####################################################################

    def evaluer(self,couleur=''):
        """Fonction d'évaluation d'une position"""

        if couleur == '':
            couleur = self.side2move

        modifval = (((-0.5)/30)*self.ply + 1)

        val_restB = 0 # pieces restantes blanches
        val_restN = 0 # pieces restantes noires

        WhiteScore=0
        BlackScore=0

        fou_b = 0
        fou_n = 0

        #structures des pions sur les colonnes
        struct_pion_b = [0,0,0,0,0,0,0,0]
        struct_pion_n = [0,0,0,0,0,0,0,0]
        pos_tour_b = [] #colonne tour
        pos_tour_n = [] #colonne tour

        # on regarde chaque cases de l'échequier
        for pos1,piece in enumerate(self.cases):

            if(piece.couleur=='blanc'):
                if piece.nom == "TOUR":
                    pos_tour_b.append(self.COL(pos1))
                    WhiteScore += modifval*self.rookmap[pos1]
                elif piece.nom == "FOU":
                    fou_b += 1
                    if pos1 != 58 and pos1 != 61: #developpement
                        WhiteScore += 20
                    WhiteScore += modifval*self.bishopmap[pos1]
                elif piece.nom == "CAVALIER":
                    if pos1 != 57 and pos1 != 62: #developpement
                        WhiteScore += 20
                    WhiteScore += modifval*self.knightmap[pos1]
                elif piece.nom == "DAME":
                    WhiteScore += modifval*self.queenmap[pos1]
                elif piece.nom == "ROI":
                    WhiteScore += modifval*self.kingmap[pos1]
                elif piece.nom == "PION":
                    struct_pion_b[self.COL(pos1)] += 1
                    WhiteScore += modifval*self.pawnmap[pos1]
                WhiteScore+=piece.valeur
                if piece.nom != "PION":
                    val_restB += piece.valeur
            elif (piece.couleur=='noir'):
                if piece.nom == "TOUR":
                    pos_tour_n.append(self.COL(pos1))
                    BlackScore += modifval*self.rookmap[-1-pos1]
                elif piece.nom == "FOU":
                    fou_n += 1
                    if pos1 != 2 and pos1 != 5: #developpement
                        BlackScore += 20
                    BlackScore += modifval*self.bishopmap[-1-pos1]
                elif piece.nom == "CAVALIER":
                    if pos1 != 1 and pos1 != 6: #developpement
                        BlackScore += 20
                    BlackScore += modifval*self.knightmap[-1-pos1]
                elif piece.nom == "DAME":
                    BlackScore += modifval*self.queenmap[-1-pos1]
                elif piece.nom == "ROI":
                    BlackScore += modifval*self.kingmap[-1-pos1]
                elif piece.nom == "PION":
                    struct_pion_n[self.COL(pos1)] += 1
                    BlackScore += modifval*self.pawnmap[-1-pos1]
                # NB : here is for black piece or empty square
                BlackScore+=piece.valeur
                if piece.nom != "PION":
                    val_restN += piece.valeur

        #tours sur colonne ouvertes
        for col in pos_tour_b:
            if struct_pion_b[col] == 0:
                WhiteScore += 50
        for col in pos_tour_n:
            if struct_pion_n[col] == 0:
                BlackScore += 50

        #roi sur colonne ouverte
        if struct_pion_b[self.COL(self.pos_roi_b)] == 0:
            WhiteScore -= 150
        if struct_pion_n[self.COL(self.pos_roi_n)] == 0:
            BlackScore -= 150

        #pions isolés
        sep1 = [-1]
        sep2 = [-1]
        for i in range(8):
            if struct_pion_b[i] == 0:
                sep1.append(i)
            if struct_pion_n[i] == 0:
                sep2.append(i)
        for i in range(1,len(sep1)):
            ilot = struct_pion_b[sep1[i-1]+1 : sep1[i]]
            if len(ilot) == 1:
                WhiteScore -= 40*ilot[0]
        for i in range(1,len(sep2)):
            ilot = struct_pion_n[sep2[i-1]+1 : sep2[i]]
            if len(ilot) == 1:
                BlackScore -= 40*ilot[0]

        if self.roqueB:
            WhiteScore += 160
        if self.roqueN:
            BlackScore += 160

        if fou_b >= 2:
            WhiteScore += 60
        if fou_n >= 2:
            BlackScore += 60

        #finale
        if val_restN >= 20:
            finalmultB = 0
        else:
            finalmultB = 20 - val_restN
        if val_restB >= 20:
            finalmultN = 0
        else:
            finalmultN = 20 - val_restB
        WhiteScore += (20*(4-self.dist_roi_centre("blanc")) + 40 * (4-self.dist_roi_bord("noir")))* finalmultB
        BlackScore += (20*(4-self.dist_roi_centre("noir")) + 40 * (4-self.dist_roi_bord("blanc"))) * finalmultN
        #finale


        if(couleur=='blanc'):
            return WhiteScore-BlackScore
        else:
            return BlackScore-WhiteScore

    def lastprise(self): #test si le dernier coup est une prise
        return not(self.history[-1][3].nom == 'VIDE')
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes

##########################################################################

    @staticmethod #fonction attaché à la classe ne pouvant pas utiliser les variables self dépendant de l'objet créé
    def ROW(x):
        """Renvoi le numéro de ligne (0 à 7) de la case 'x'"""
        return (x >> 3) # x >> y Renvoie x avec les bits décalés vers la droite de y places.

    @staticmethod
    def COL(x):
        """Renvoi le numéro de colonne (0 à 7) de la case 'x'"""
        return (x & 7) # x & y Fait un "et au niveau du bit". Chaque bit de sortie est 1 si le bit correspondant de x ET de y est 1, sinon il est 0.
