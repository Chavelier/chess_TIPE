class Piece:
    """Pieces du jeu d'échec"""

    VIDE = '.'
    nomPiece=(VIDE,'ROI','REINE','TOUR','CAVALIER','FOU','PION') #nom des pièces enregistrées

    valeurPiece=(0,0,900,500,300,300,100) #valeurs des pieces dont l'id correspond


    tab120 = (
	-1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
	-1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
	-1,  0,  1,  2,  3,  4,  5,  6,  7, -1,
	-1,  8,  9, 10, 11, 12, 13, 14, 15, -1,
	-1, 16, 17, 18, 19, 20, 21, 22, 23, -1,
	-1, 24, 25, 26, 27, 28, 29, 30, 31, -1,
	-1, 32, 33, 34, 35, 36, 37, 38, 39, -1,
	-1, 40, 41, 42, 43, 44, 45, 46, 47, -1,
	-1, 48, 49, 50, 51, 52, 53, 54, 55, -1,
	-1, 56, 57, 58, 59, 60, 61, 62, 63, -1,
	-1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
	-1, -1, -1, -1, -1, -1, -1, -1, -1, -1
	)
    tab64 = (
	21, 22, 23, 24, 25, 26, 27, 28,
	31, 32, 33, 34, 35, 36, 37, 38,
	41, 42, 43, 44, 45, 46, 47, 48,
	51, 52, 53, 54, 55, 56, 57, 58,
	61, 62, 63, 64, 65, 66, 67, 68,
	71, 72, 73, 74, 75, 76, 77, 78,
	81, 82, 83, 84, 85, 86, 87, 88,
	91, 92, 93, 94, 95, 96, 97, 98
	)

    #mouvements par rapport a tab64
    deplacements_tour=(-10,10,-1,1)
    deplacements_fou=(-11,-9,11,9)
    deplacements_cavalier=(-12,-21,-19,-8,12,21,19,8)
    #REINE = TOUR+FOU
    #ROI = REINE mais 1 case


    def __init__(self,nom=VIDE,couleur=''):
        """créé la piece avec ses caracteristiques : nom, couleur, et valeur"""
        self.nom = nom
        self.couleur = couleur
        self.valeur = self.valeurPiece[self.nomPiece.index(nom)]

    ######################################################################

    def isEmpty(self):
        """Renvoi vrai si la case est vide"""

        return (self.nom==self.VIDE)

    ####################################################################

    def pos2_roi(self,pos1,cAd,echiquier,dontCallIsAttacked=False):
        """
        Renvoi la liste des coups du ROI :
        - qui est à la position 'pos1'
        - dont la couleur des adversaire est 'cAd'
        - dontCallIsAttacked est défini pour éviter les appels récursifs
         entre is_attacked () et gen_moves_list ().
        """

        liste=[]

        for i in (self.deplacements_tour+self.deplacements_fou):
            n=self.tab120[self.tab64[pos1]+i]
            if(n!=-1):
                if(echiquier.cases[n].isEmpty() or echiquier.cases[n].couleur==cAd):
                    liste.append((pos1,n,''))

        if(dontCallIsAttacked):
            return liste # pour éviter de calculer le roque comme légal si attaqué

        # le côté qui joue est l'opposé de la couleur adverse
        c=echiquier.oppColor(cAd)

        # Castle moves
        if(c=='blanc'):
            if(echiquier.white_can_castle_63):
                # si la tour est sur la 63e case
                # et si les cases entre roi et tour son vide
                # et si cases entre non attaquées
                # et si le roi n'est pas en échec
                # alors on ajoute le roque
                if(echiquier.cases[63].nom=='TOUR' and \
                echiquier.cases[63].couleur=='blanc' and \
                echiquier.cases[61].isEmpty() and \
                echiquier.cases[62].isEmpty() and \
                echiquier.is_attacked(61,'noir')==False and \
                echiquier.is_attacked(62,'noir')==False and \
                echiquier.is_attacked(pos1,'noir')==False):
                    liste.append((pos1,62,''))
            if(echiquier.white_can_castle_56):
                # S'il y a une tour en 56, etc...
                if(echiquier.cases[56].nom=='TOUR' and \
                echiquier.cases[56].couleur=='blanc' and \
                echiquier.cases[57].isEmpty() and \
                echiquier.cases[58].isEmpty() and \
                echiquier.cases[59].isEmpty() and \
                echiquier.is_attacked(58,cAd)==False and \
                echiquier.is_attacked(59,cAd)==False and \
                echiquier.is_attacked(pos1,cAd)==False):
                    liste.append((pos1,58,''))
        elif(c=='noir'):
            if(echiquier.black_can_castle_7):
                if(echiquier.cases[7].nom=='TOUR' and \
                echiquier.cases[7].couleur=='noir' and \
                echiquier.cases[5].isEmpty() and \
                echiquier.cases[6].isEmpty() and \
                echiquier.is_attacked(5,cAd)==False and \
                echiquier.is_attacked(6,cAd)==False and \
                echiquier.is_attacked(pos1,cAd)==False):
                    liste.append((pos1,6,''))
            if(echiquier.black_can_castle_0):
                if(echiquier.cases[0].nom=='TOUR' and \
                echiquier.cases[0].couleur=='noir' and \
                echiquier.cases[1].isEmpty() and \
                echiquier.cases[2].isEmpty() and \
                echiquier.cases[3].isEmpty() and \
                echiquier.is_attacked(2,cAd)==False and \
                echiquier.is_attacked(3,cAd)==False and \
                echiquier.is_attacked(pos1,cAd)==False):
                    liste.append((pos1,2,''))
        return liste

    ####################################################################

    def pos2_tour(self,pos1,cAd,echiquier):
        """Renvoi la liste des coups de la TOUR :
        - à la position 'pos1' (0 à 63)
        - la couleur adverse est cAd (blanc,noir)"""

        liste=[]

        for k in self.deplacements_tour:
            j=1
            while(True):
                n=self.tab120[self.tab64[pos1] + (k * j)]
                if(n!=-1): # tant qu'on est pas en dehors de l'échéquier
                    if(echiquier.cases[n].isEmpty() or echiquier.cases[n].couleur==cAd):
                        liste.append((pos1,n,'')) # ajoute le coup si case vide ou adverse
                else:
                    break # stop si en dehors du plateau
                if(not echiquier.cases[n].isEmpty()):
                    break # permet d'empécher tour de passer à travers les pièces
                j=j+1
        return liste

    ####################################################################

    def pos2_cavalier(self,pos1,cAd,echiquier):
        """Renvoi la liste des coups du CAVALIER :
        - à la position 'pos1' (0 à 63)
        - la couleur adverse est cAd (blanc,noir)"""

        liste=[]

        for i in self.deplacements_cavalier:
            n=self.tab120[self.tab64[pos1]+i]
            if(n!=-1):
                if(echiquier.cases[n].isEmpty() or echiquier.cases[n].couleur==cAd):
                    liste.append((pos1,n,'')) # simple car peut sauter au dessus des pièces
        return liste

    ####################################################################

    def pos2_fou(self,pos1,cAd,echiquier):
        """Renvoi la liste des coups du FOU :
        - à la position 'pos1' (0 à 63)
        - la couleur adverse est cAd (blanc,noir)"""

        liste=[]

        for k in self.deplacements_fou:
            j=1
            while(True):
                n=self.tab120[self.tab64[pos1] + (k * j)]
                if(n!=-1): # tant qu'on est pas en dehors de l'échéquier
                    if(echiquier.cases[n].isEmpty() or echiquier.cases[n].couleur==cAd):
                        liste.append((pos1,n,'')) # ajoute le coup si case vide ou adverse
                else:
                    break # stop si en dehors du plateau
                if(not echiquier.cases[n].isEmpty()):
                    break # permet d'empécher fou de passer à travers les pièces
                j=j+1

        return liste

    ####################################################################

    def pos2_pion(self,pos1,couleur,echiquier):
        """Renvoi la liste des coups du PION :
        - à la position 'pos1' (0 à 63)
        - la couleur du PION est 'couleur' (blanc,noir)"""

        liste=[]

        # PION blanc ---------------------------------------------------
        if(couleur=='blanc'):

            # case du dessus
            n=self.tab120[self.tab64[pos1]-10]
            if(n!=-1):
                if(echiquier.cases[n].isEmpty()):
                    # Si le PION est arrivé à la dernière rangée
                    if(n<8):
                        # promotion
                        liste.append((pos1,n,'q'))
                        liste.append((pos1,n,'r'))
                        liste.append((pos1,n,'n'))
                        liste.append((pos1,n,'b'))
                    else:
                        liste.append((pos1,n,''))

            # 2e case si le PION n'a pas bougé
            if(echiquier.ROW(pos1)==6):
                # si les 2 cases du dessus sont vide
                if(echiquier.cases[pos1-8].isEmpty() and echiquier.cases[pos1-16].isEmpty()):
                    liste.append((pos1,pos1-16,''))

            # Capture haut gauche
            n=self.tab120[self.tab64[pos1]-11]
            if(n!=-1):
                if(echiquier.cases[n].couleur=='noir' or echiquier.ep==n):
                    if(n<8): # Capture + promotion
                        liste.append((pos1,n,'q'))
                        liste.append((pos1,n,'r'))
                        liste.append((pos1,n,'n'))
                        liste.append((pos1,n,'b'))
                    else:
                        liste.append((pos1,n,''))

            # Capture haut droite
            n=self.tab120[self.tab64[pos1]-9]
            if(n!=-1):
                if(echiquier.cases[n].couleur=='noir' or echiquier.ep==n):
                    if(n<8):
                        liste.append((pos1,n,'q'))
                        liste.append((pos1,n,'r'))
                        liste.append((pos1,n,'n'))
                        liste.append((pos1,n,'b'))
                    else:
                        liste.append((pos1,n,''))

        # PION noir ---------------------------------------------------
        else:

            # case du dessus
            n=self.tab120[self.tab64[pos1]+10]
            if(n!=-1):
                if(echiquier.cases[n].isEmpty()):
                    # PION arrivé à la 8e rangée (cases 56 à 63),
                    # promotion
                    if(n>55):
                        liste.append((pos1,n,'q'))
                        liste.append((pos1,n,'r'))
                        liste.append((pos1,n,'n'))
                        liste.append((pos1,n,'b'))
                    else:
                        liste.append((pos1,n,''))

            # 2e case si le PION n'a pas bougé
            if(echiquier.ROW(pos1)==1):
                # si les 2 cases du dessus sont vide
                if(echiquier.cases[pos1+8].isEmpty() and echiquier.cases[pos1+16].isEmpty()):
                    liste.append((pos1,pos1+16,''))

        # Capture bas gauche
            n=self.tab120[self.tab64[pos1]+9]
            if(n!=-1):
                if(echiquier.cases[n].couleur=='blanc' or echiquier.ep==n):
                    if(n>55):
                        liste.append((pos1,n,'q'))
                        liste.append((pos1,n,'r'))
                        liste.append((pos1,n,'n'))
                        liste.append((pos1,n,'b'))
                    else:
                        liste.append((pos1,n,''))

            # Capture bas droite
            n=self.tab120[self.tab64[pos1]+11]
            if(n!=-1):
                if(echiquier.cases[n].couleur=='blanc' or echiquier.ep==n):
                    if(n>55):
                        liste.append((pos1,n,'q'))
                        liste.append((pos1,n,'r'))
                        liste.append((pos1,n,'n'))
                        liste.append((pos1,n,'b'))
                    else:
                        liste.append((pos1,n,''))

        return liste

    ####################################################################
