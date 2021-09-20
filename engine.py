from piece import *
import random
import time


class Engine:
    """l'intelligence artificielle"""


    def __init__(self):

        self.MAX_PLY=32
        self.pv_length=[0 for x in range(self.MAX_PLY)]
        self.INFINITY=320000
        self.init()

    def init(self):
        self.endgame=False
        self.init_depth=4 # profondeur de recherche fixe
        self.nodes=0 # nb de noeuds
        self.clear_pv() #arbre de variation
        # self.in_op = True #drapeau pour tester l'ouverture
        self.val_compteur = 0 #valeur du compteur pour la lecture d'une partie
        self.historique_lire = "" #historique littérale des coups pour la lecture d'une partie

        self.transposition = {} #table des transpositions dictionnaire {id : (eval,profondeur)}
        self.use_table = True

        self.drawpos = {} #dictionnaire contenant les pos et le nombre de fois qu'une pos a été joué

        self.epsilon = []

        self.noeuds = 0
        self.engine_move_list = [] #coups jouables par l'ordi au prochain move
        self.variation = []
        #self.time1 = time.time()



    ####################################################################

    def usermove(self,b,c):
        """Deplace une piece avec 'c' une cmd de la forme 'e2e4' ou 'd7d8q'.
        L'argument 'b' est l'echequier.
        """

        if(self.endgame) or self.is_nulle_rep(b) or self.is_nulle_mat(b):
            self.print_result(b)
            return

        # on sort de la fonction si 'c' n'est pas une bonne cmd.
        chk=self.chkCmd(c)
        if(chk!=''):
            print(chk)
            return

        # on convertit les cases en id (int)
        pos1=b.caseStr2Int(c[0]+c[1])
        pos2=b.caseStr2Int(c[2]+c[3])

        # On demande une promotion ?
        promote=''
        if(len(c)>4):
            promote=c[4]
            if(promote=='q'):
                promote='q'
            elif(promote=='r'):
                promote='r'
            elif(promote=='n'):
                promote='n'
            elif(promote=='b'):
                promote='b'

        # On génère la liste des coups possibles pour celui qui a le trait
        mList=b.gen_moves_list()

        # Le déplacement est dans la liste ? Ou il laisse le roi en échec ?

        if(((pos1,pos2,promote) not in mList) or \
        (b.domove(pos1,pos2,promote)==False)):
            print("\n"+'Le coup '+c+' ''n\'est pas possible, ou laisse le roi en échec.'+"\n")
            return
        self.add_nulle(b)
        self.print_result(b)

        # Let the engine play
        #self.search(b)

    ####################################################################


    def userliremove(self,b,c):
        """Deplace une piece avec 'c' une cmd de la forme 'e2e4' ou 'd7d8q'.
        L'argument 'b' est l'echequier.
        """

        if(self.endgame):
            self.print_result(b)
            return

        # on sort de la fonction si 'c' n'est pas une bonne cmd.
        chk=self.chkCmd(c)
        if(chk!=''):
            print(chk)
            return

        # on convertit les cases en id (int)
        pos1=b.caseStr2Int(c[0]+c[1])
        pos2=b.caseStr2Int(c[2]+c[3])

        # On demande une promotion ?
        promote=''
        if(len(c)>4):
            promote=c[4]
            if(promote=='q'):
                promote='q'
            elif(promote=='r'):
                promote='r'
            elif(promote=='n'):
                promote='n'
            elif(promote=='b'):
                promote='b'

        # On génère la liste des coups possibles pour celui qui a le trait
        mList=b.gen_moves_list()

        # Le déplacement est dans la liste ? Ou il laisse le roi en échec ?
        if(((pos1,pos2,promote) not in mList) or \
        (b.domove(pos1,pos2,promote)==False)):
            return

        self.print_result(b)

        # Let the engine play
        #self.search(b)


    ####################################################################

    def chkCmd(self,c):

        """Vérifie si la commande 'c' proposée par l'utilisateur,
        est bien de la forme correcte pour un coup, comme 'e2e4','b7b8n'...
        Retourne '' si c'est correct.
        Retourne un string erreur sinon.
        """

        err=(
        "Le coup doit etre de la forme 'e2e4' ou 'a8a9q'...",
        'Coup incorrect'
        )
        letters=('a','b','c','d','e','f','g','h')
        numbers=('1','2','3','4','5','6','7','8')

        if(len(c)<4 or len(c)>5):
            return err[0]

        if(c[0] not in letters):
            return err[1]

        if(c[1] not in numbers):
            return err[1]

        if(c[2] not in letters):
            return err[1]

        if(c[3] not in numbers):
            return err[1]

        return ''

    #################################################################### gestion de l'ia





    #################################################################### gestion de l'ia
    #Pour simplifier l'écriture, il faut définir deux variables
    #La première : suite_coups est la suite de coup jouée pour le moment par l'ordinateur et par l'ordi sous forme de charactères
    #La seconde : ligne_partielle est la chaine de charactères de la longueur exactes des coups joués

    def ouverture(self,b):
        """renvoi la liste des coups jouables depuis la pos selon l'ouverture"""
        ligne_partielle = ""
        suite_coups = ""
        all_coups = [] #liste de tous les coups possibles
        nb_coup = len(b.history)
        with open("book.txt",'rt') as ouvertures:
            for i in range(nb_coup):
                suite_coups += b.caseInt2Str(b.history[i][0]) + b.caseInt2Str(b.history[i][1]) + " "
            for ligne in ouvertures:
                ligne_partielle = ligne[0 : 5*nb_coup]
                if suite_coups == ligne_partielle:
                    all_coups += [ligne[5*nb_coup : 5*nb_coup + 4]]

                else :
                    ligne_partielle = ""
        return all_coups

    ###################################################################

    def print_result(self,b):
        "Test si la partie est finie et affiche le resultat"

        # Y a t'il un coup possible ?
        f=False
        for pos1,pos2,promote in b.gen_moves_list():
            if(b.domove(pos1,pos2,promote)):
                b.undomove()
                f=True # yes, a move can be done
                break

        # No legal move left, print result
        if(not f):
            if(b.in_check(b.side2move)):
                if(b.side2move=='blanc'):
                    print("0-1 - Victoire des Noirs")
                else:
                    print("1-0 - Victoire des Blancs")
            else:
                print("1/2-1/2 - Nulle par Pat")
            self.endgame=True

        if self.is_nulle_rep(b):
            self.endgame=True
            print("1/2-1/2 - Nulle par répétition")
        if self.is_nulle_mat(b):
            self.endgame=True
            print("1/2-1/2 - Nulle par manque de materiel")

        # TODO
        # 50 moves rule

    ####################################################################

    def clear_pv(self):
        "Nettoie la 'table triangulaire' des principales variations contenant"
        "la ligne des meilleurs coups calculés"
        "Cette ligne correpond-elle à l'équilibre de Nash des depth-ième sous jeux"
        "en théorie des jeux?"

        self.pv=[[0 for x in range(self.MAX_PLY)] for x in range(self.MAX_PLY)]

    ####################################################################

    def setboard(self,b,c):

        """Set the chessboard to the FEN position given by user with
        the command line 'setboard ...'.
        'c' in argument is for example :
        'setboard 8/5k2/5P2/8/8/5K2/8/8 w - - 0 0'
        """

        cmd=c.split() # split command with spaces
        cmd.pop(0) # drop the word 'setboard' written by user

        # set the FEN position on board
        if(b.setboard(' '.join(cmd))):
            self.endgame=False # success, so no endgame


    ###############################################################
    def add_nulle(self,b):
        p = b.pos_id
        if p in self.drawpos:
            self.drawpos[p] += 1
        else:
            self.drawpos[p] = 1
    def del_nulle(self,b):
        p = b.pos_id
        if p in self.drawpos:
            self.drawpos[p] -= 1

    def is_nulle_rep(self,b):
        p = b.pos_id
        if p in self.drawpos:
            if self.drawpos[p] >= 3:
                return True
        return False
    def is_nulle_mat(self,b):
        return b.nulle_mat()

    ####################################################################

    def setDepth(self,c):

        """'c' is the user command line, i.e. 'sd [x]'
        to set the search depth.
        """

        # Checking the requested value
        cmd=c.split()
        #cmd[0]='sd'
        #cmd[1] should be an integer

        try:
            d=int(cmd[1])
        except ValueError:
            print('Depth isn\'t an integer. Please type i.e. : sd 5')
            return

        if(d<2 or d>self.MAX_PLY):
            print('Depth must be between 2 and',self.MAX_PLY)
            return

        # Things seems to be all right
        self.init_depth=d
        print('Depth set to',d)

    ####################################################################

    def perft(self,c,b):

        """PERFformance Test :
        This is a debugging function through the move generation tree
        for the current board until depth [x].
        'c' is the command line written by user : perft [x]
        """

        # Checking the requested depth
        cmd=c.split()
        #cmd[0]='perft'

        try:
            d=int(cmd[1])
        except ValueError:
            print('Please type an integer as depth i.e. : perft 5')
            return

        if(d<1 or d>self.MAX_PLY):
            print('Depth must be between 1 and',self.MAX_PLY)
            return

        print("Depth\tNodes\tCaptures\tE.p.\tCastles\tPromotions\tChecks\tCheckmates")

        time1 = self.get_ms()
        for i in range(1,d+1):
            total=self.perftoption(0,i-1,b)
            print("{}\t{}".format(i,total))
        time2 = self.get_ms()
        timeDiff = round((time2-time1)/1000,2)
        print('Done in',timeDiff,'s')

    def perftoption(self,prof,limit,b):
        cpt=0

        if(prof>limit):
            return 0

        l=b.gen_moves_list()

        for i,m in enumerate(l):

            if(not b.domove(m[0],m[1],m[2])):
                continue

            cpt+=self.perftoption(prof+1,limit,b)

            if(limit==prof):
                cpt+=1

            b.undomove()

        return cpt

    ####################################################################

    def legalmoves(self,b):

        "Show legal moves for side to move"

        mList=b.gen_moves_list()

        cpt=1
        for m in mList:
            if(not b.domove(m[0],m[1],m[2])):
                continue
            print('move #',cpt,':',b.caseInt2Str(m[0])+b.caseInt2Str(m[1])+m[2])
            b.undomove()
            cpt+=1

    def nbmoves(self,b,depth):
        if depth == 0:
            return 0
        cpt = 0
        mList = b.gen_moves_list()
        for m in mList:
            if(not b.domove(m[0],m[1],m[2])):
                continue
            cpt += 1+self.nbmoves(b,depth-1)
            b.undomove()
        return cpt
    ####################################################################

    def getboard(self,b,for_nulle=False):

        """The user requests the current FEN position
        with the command 'getboard'"""
        return b.getboard(for_nulle)

    ####################################################################

    def newgame(self,b):

        self.init()
        b.init()

    ####################################################################

    def bench(self,b):

        """Test to calculate the number of nodes a second.
        The position used is the 17th move of the game :
        Bobby Fischer vs. J. Sherwin, New Jersey State
        Open Championship, 9/2/1957 :
        1rb2rk1/p4ppp/1p1qp1n1/3n2N1/2pP4/2P3P1/PPQ2PBP/R1B1R1K1 w - - 0 1
        The engine searches to a given depth, 3 following times.
        The kilonodes/s is calculated with the best time.
        """

        oldDepth=self.init_depth
        self.init_depth=4
        timeDiff=[]

        # testing 3 times
        for i in range(3):

            print('Searching to depth',self.init_depth,'...')

            if(not b.setboard('1rb2rk1/p4ppp/1p1qp1n1/3n2N1/2pP4/2P3P1/PPQ2PBP/R1B1R1K1 w - - 0 1')):
                print('Could not set board ???!#!')
                return

            start_time=self.get_ms()
            self.play_bot(b)
            stop_time=self.get_ms()
            timeDiff.append(stop_time-start_time)
            print('Time:',timeDiff[i],'ms\n')

        if(timeDiff[1] < timeDiff[0]):
            timeDiff[0] = timeDiff[1]
        if(timeDiff[2] < timeDiff[0]):
            timeDiff[0] = timeDiff[2]

        print('Best time:',timeDiff[0],'ms')
        print('Nodes:',self.nodes)
        # print('Nodes per second:',round(self.nodes/timeDiff[0],2),'kn/s')

        # Restoring changed values
        self.init_depth=oldDepth

    ####################################################################

    def undomove(self,b):
        "The user requested a 'undomove' in command line"

        self.del_nulle(b)
        b.undomove()
        self.endgame=False

    ####################################################################

    def get_ms(self):
        return int(round(time.time() * 1000))

    ####################################################################


    def save(self,b,c):
            cmd=c.split()

            if cmd[0] != "save":
                print('Commande incorrecte')
                return

            historique = ""
            nb_coup = len(b.history)

            for i in range(nb_coup):
                historique += b.caseInt2Str(b.history[i][0]) + b.caseInt2Str(b.history[i][1]) + " "
            print("saving : "+historique)
            with open("saves.txt",'a') as file:
                file.write(' '.join(cmd[1:])+' ')
                file.write(historique)
                file.write("\n")


    ####################################################################

    def create_op(self,b):
        historique = ""

        nb_coup = len(b.history)

        for i in range(nb_coup):
            historique += b.caseInt2Str(b.history[i][0]) + b.caseInt2Str(b.history[i][1]) + " "
        print("ouverture enregistrée : "+historique)
        with open("book.txt",'a') as file:
            file.write(historique)
            file.write("\n")


    #####################################################################
