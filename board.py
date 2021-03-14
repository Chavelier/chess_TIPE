from piece import *

import os
# from PIL import Image, ImageTk ## Importation des modules utiles dans PIL

# import tkFont
# my_font = tkFont.Font(family="Helvetica", size=36 ,weight="bold")

class Board:
    """Le plateau de jeu"""

    coords = [
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

    def move_piece(self,cmd):
        """controle le mvt des pieces. cmd = "e2e4" par ex"""
        start = cmd[0:2]
        end = cmd[2:4]
        piece_en_mvt = self.cases[Board.coords.index(start)]
        if piece_en_mvt != Piece():
            self.histo += [(cmd,self.cases[Board.coords.index(end)])] #on ajoute la ligne à l'historique
            self.cases[Board.coords.index(start)] = Piece() #remplace la position de départ par du vide
            self.cases[Board.coords.index(end)] = piece_en_mvt #remplace la position finale par la piece



    def undo_move(self):
        if self.histo == []:
            return
        start = self.histo[-1][0][2:4]
        end = self.histo[-1][0][0:2]
        piece_en_mvt = self.cases[Board.coords.index(start)]
        self.cases[Board.coords.index(start)] = self.histo[-1][1] #remplace la position de départ par la pièce mangée précedemment
        self.cases[Board.coords.index(end)] = piece_en_mvt #remplace la position finale par la piece
        del self.histo[-1]
