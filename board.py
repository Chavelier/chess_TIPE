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
        Piece('TOUR','noir'), Piece('CAVALIER','noir'), Piece('FOU','noir'), Piece('REINE','noir'), Piece('ROI','noir'), Piece('FOU','noir'), Piece('CAVALIER','noir'), Piece('TOUR','noir'),
        Piece('PION','noir'), Piece('PION','noir'), Piece('PION','noir'), Piece('PION','noir'), Piece('PION','noir'), Piece('PION','noir'), Piece('PION','noir'), Piece('PION','noir'),
        Piece(), Piece(), Piece(), Piece(), Piece(), Piece(), Piece(), Piece(), Piece(), Piece(), Piece(), Piece(), Piece(), Piece(), Piece(), Piece(),
        Piece(), Piece(), Piece(), Piece(), Piece(), Piece(), Piece(), Piece(), Piece(), Piece(), Piece(), Piece(), Piece(), Piece(), Piece(), Piece(),
        Piece('PION','blanc'), Piece('PION','blanc'), Piece('PION','blanc'), Piece('PION','blanc'), Piece('PION','blanc'), Piece('PION','blanc'), Piece('PION','blanc'), Piece('PION','blanc'),
        Piece('TOUR','blanc'), Piece('CAVALIER','blanc'), Piece('FOU','blanc'), Piece('REINE','blanc'), Piece('ROI','blanc'), Piece('FOU','blanc'), Piece('CAVALIER','blanc'), Piece('TOUR','blanc')
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


    # def move_piece(self,cmd):
    #     """controle le mvt des pieces. cmd = "e2e4" par ex"""
    #     start = cmd[0:2]
    #     end = cmd[2:4]
    #     piece_en_mvt = self.cases[Board.coords.index(start)]
    #     if piece_en_mvt != Piece():
    #         self.histo += [(cmd,self.cases[Board.coords.index(end)].nom,self.cases[Board.coords.index(end)].couleur)] #on ajoute la ligne à l'historique
    #         self.cases[Board.coords.index(start)] = Piece() #remplace la position de départ par du vide
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

            elif(piece.nom=='REINE'): # REINE = TOUR + FOU
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
        self.cases[depart]=Piece()

        self.ply+=1

        # PION deplacé -------------------------------------
        if(pieceDeplacee.nom=='PION'):

            # PION blanc
            if(pieceDeplacee.couleur=='blanc'):

                # Si le coup est en passant
                if(self.ep==arrivee):
                    piecePrise=self.cases[arrivee+8] # on prend le PION noir
                    self.cases[arrivee+8]=Piece()
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
                    self.cases[arrivee-8]=Piece()
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
                        self.cases[56]=Piece()
                        self.cases[59]=Piece('TOUR','blanc')

                    elif(arrivee==62):
                        self.cases[63]=Piece()
                        self.cases[61]=Piece('TOUR','blanc')

            # ROI noir
            else:
                self.pos_roi_n = arrivee
                if(depart==4):
                    self.black_can_castle_0=False
                    self.black_can_castle_7=False

                    if(arrivee==6):
                        self.cases[7]=Piece()
                        self.cases[5]=Piece('TOUR','noir')

                    elif(arrivee==2):
                        self.cases[0]=Piece()
                        self.cases[3]=Piece('TOUR','noir')

        # fin du problème de certaines pièces-----------------------------------------------

        # N'importe quel coup annule la case de prise en passant
        if(flagViderEp==True):
            self.ep=-1

        # Promotion : le PION est changé en n'importe qu'elle piece
        if(promote!=''):
            if(promote=='q'):
                self.cases[arrivee]=Piece('REINE',self.side2move)
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
                self.cases[pos2]=Piece()
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
                        self.cases[59]=Piece()
                    elif(pos2==62):
                        self.cases[63]=Piece('TOUR','blanc')
                        self.cases[61]=Piece()
            # ROI noir
            else:
                self.pos_roi_n = pos1
                if(pos1==4):
                    if(pos2==2):
                        self.cases[0]=Piece('TOUR','noir')
                        self.cases[3]=Piece()
                    elif(pos2==6):
                        self.cases[7]=Piece('TOUR','noir')
                        self.cases[5]=Piece()

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

    def evaluer(self):
        """Fonction d'évaluation d'une position"""

        WhiteScore=0
        BlackScore=0

        fou_b = 0
        fou_n = 0

        #structures des pions sur les colonnes
        struct_pion_b = [0,0,0,0,0,0,0,0]
        struct_pion_n = [0,0,0,0,0,0,0,0]
        pos_tour_b = [] #colonne tour
        pos_tour_n = [] #colonne tour

        # Parsing the board squares from 0 to 63
        for pos1,piece in enumerate(self.cases):

            # case_c = int(self.is_attacked(pos1,'blanc')) - int(self.is_attacked(pos1,'noir'))
            # WhiteScore += 5*case_c
            # Material score
            if(piece.couleur=='blanc'):
                if piece.nom == "TOUR":
                    pos_tour_b.append(self.COL(pos1))
                if piece.nom == "FOU":
                    fou_b += 1
                WhiteScore+=piece.valeur
                if piece.nom == 'PION':
                    struct_pion_b[self.COL(pos1)] += 1
            else:
                if piece.nom == "TOUR":
                    pos_tour_n.append(self.COL(pos1))
                if piece.nom == "FOU":
                    fou_n += 1
                if piece.nom == 'PION':
                    struct_pion_n[self.COL(pos1)] += 1
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

        if(self.side2move=='blanc'):
            return WhiteScore-BlackScore
        else:
            return BlackScore-WhiteScore


    ####################################################################

    @staticmethod #fonction attaché à la classe ne pouvant pas utiliser les variables self dépendant de l'objet créé
    def ROW(x):
        """Renvoi le numéro de ligne (0 à 7) de la case 'x'"""
        return (x >> 3) # x >> y Renvoie x avec les bits décalés vers la droite de y places.

    @staticmethod
    def COL(x):
        """Renvoi le numéro de colonne (0 à 7) de la case 'x'"""
        return (x & 7) # x & y Fait un "et au niveau du bit". Chaque bit de sortie est 1 si le bit correspondant de x ET de y est 1, sinon il est 0.
