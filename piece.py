class Piece:
    """Pieces du jeu d'échec"""

    VIDE = '.'
    nomPiece=(VIDE,'ROI','REINE','TOUR','CAVALIER','FOU','PION') #nom des pièces enregistrées

    valeurPiece=(0,0,900,500,300,300,100) #valeurs des pieces dont l'id correspond



    def __init__(self,nom=VIDE,couleur=''):
        """créé la piece avec ses caracteristiques : nom, couleur, et valeur"""
        self.nom = nom
        self.couleur = couleur
        self.valeur = self.valeurPiece[self.nomPiece.index(nom)]
