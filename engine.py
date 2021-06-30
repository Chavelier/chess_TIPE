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

        self.use_op = True
        self.book = "book.txt"

        self.transposition = {} #table des transpositions dictionnaire {id : (eval,profondeur)}
        self.use_table = True #utiliser ou non la table
        self.modultranspo = True #permet d'activer ou non la table en fonction du temps d'execution

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

    ####################################################################
    def play_bot(self,b):

        if(self.endgame) or self.is_nulle_rep(b): # on ne peut pas chercher si la partie est finie
            self.print_result(b)
            return

        coups = self.ouverture(b)
        if coups != [] and self.use_op:
            c = coups[random.randrange(0,len(coups))]
            print("Coup d'ouverture : "+c)
            b.domove(b.caseStr2Int(c[0:2]),b.caseStr2Int(c[2:4]),c[4:])

            self.add_nulle(b) #ajoute la position a la liste des coups joués
        else:
            self.search(b)



    def search(self,b):
        """cherche le meilleur coup du joueur qui joue dans l'échéquier 'b'"""
        self.time1 = time.time()
        self.clear_pv() # on efface l'ancien arbre des variations
        self.nodes=0
        b.ply=0

        print("Profondeur\tNoeuds\tScore\tPrincipale variation")

        for i in range(1,self.init_depth+1):

            score=self.alphabeta(i,-self.INFINITY,self.INFINITY,b)


            print("{}\t\t{}\t{}\t".format(i,self.nodes,score/100),end='')

            #Affichage des infos
            j=0
            while(self.pv[j][j]!=0):
                c=self.pv[j][j]
                pos1=b.caseInt2Str(c[0])
                pos2=b.caseInt2Str(c[1])
                print("{}{}{}".format(pos1,pos2,c[2]),end=' ')
                j+=1
            print()

            # Break si on trouve un mat
            if(score>self.INFINITY-100 or score<-self.INFINITY+100):
                break

        #le meilleur coup correspond au premier élement de la dernière variation
        best=self.pv[0][0]
        b.domove(best[0],best[1],best[2])
        self.add_nulle(b) #ajoute la position a la liste des coups joués
        self.print_result(b)
        exectime = time.time() - self.time1

        print("temps d'execution : %s s \n"%exectime)

        if exectime >= 20 and self.modultranspo:
            self.use_table = not self.use_table
            print("la transposition est desormais en position : %s"%self.use_table)

    ####################################################################

    def alphabeta(self,depth,alpha,beta,b):
        key = b.pos_id
        alatable = (key in self.transposition and self.use_table)

        if self.is_nulle_rep(b) or self.is_nulle_mat(b):
            return 0 #- b.evaluer()

        # Arrivée à la fin de la récursivité, la profondeur 0 correspond à une évaluation simple de la position
        if(depth==0):
            if alatable:
                val , Tdepth = self.transposition[key]
            else:
                val = b.evaluer()
                self.transposition[key] = (val,depth) #on remplace ou on crée l'instance dans la table
            return val
            #TODO : return quiesce(alpha,beta) pour eviter un effet d'horizon !

        if not alatable:
            self.nodes+=1
        self.pv_length[b.ply] = b.ply

        # Pour ne pas aller trop loin
        if(b.ply >= self.MAX_PLY-1):
            val = b.evaluer()
            self.transposition[key] = (val,depth) #on remplace ou on crée l'instance dans la table
            return val


        # Si le roi est en échec, on va plus loin dans l'analyse
        chk=b.in_check(b.side2move) # 'chk' used at the end of func too
        if(chk):
            depth+=1

        #TODO : sort moves : captures first

        # Génère tous les coups à jouer pour celui qui a le trait.
        # Ceux qui laissent le roi en échec seront traités avec domove()
        mList=b.gen_moves_list()
        # Ici, j'imagine qu'on randomise la liste des coups possibles pour ne pas avoir
        # de problème, mais ne pourrait-on pas faire quelque chose de plus utile ?
        # random.shuffle(mList)
        # mList=b.tri_move(mList)


        f=False # flag to know if at least one move will be done
        for i,m in enumerate(mList):

            # Fais le coup 'c'.
            # Si le roi est en échec, on revient en arrière et on l'ignore
            # Rappel : un coup est défini avec (case_depart,case_arrivee,promote)
            # Par ex : 'e7e8q' donne (12,4,'q')
            if(not b.domove(m[0],m[1],m[2])):
                continue # on ignore le coup s'il laisse le roi en echec

            f=True #Le coup est passé

            self.add_nulle(b) # pour que l'ordi prennent en compte l'idée de nulle
            Tdepth = -1
            if alatable:
                Teval , Tdepth = self.transposition[key]

            if Tdepth >= depth:
                score = Teval
                depth = Tdepth
            else:
                score=-self.alphabeta(depth-1,-beta,-alpha,b)
            # score=-self.alphabeta(depth-1,-beta,-alpha,b)
            #On fait machine arrière
            self.del_nulle(b)
            b.undomove()

            if(score>alpha):

                # TODO
                # this move caused a cutoff,
                # should be ordered higher for the next search

                if(score>=beta):
                    self.transposition[key] = (beta,depth)
                    return beta
                alpha = score

                # Updating the triangular PV-Table
                self.pv[b.ply][b.ply] = m
                j = b.ply + 1
                while(j<self.pv_length[b.ply+1]):
                    self.pv[b.ply][j] = self.pv[b.ply+1][j]
                    self.pv_length[b.ply] = self.pv_length[b.ply + 1]
                    j+=1

        # If no move has been done : it is DRAW or MAT
        if(not f):
            if(chk):
                self.transposition[key] = (-self.INFINITY + b.ply,depth)
                return -self.INFINITY + b.ply # MAT
            else:
                self.transposition[key] = (0,depth)
                return 0 # DRAW

        #TODO : 50 moves rule

        self.transposition[key] = (alpha,depth) #on remplace ou on crée l'instance dans la table
        return alpha




    ####################################################################
    #Pour simplifier l'écriture, il faut définir deux variables
    #La première : suite_coups est la suite de coup jouée pour le moment par l'ordinateur et par l'ordi sous forme de charactères
    #La seconde : ligne_partielle est la chaine de charactères de la longueur exactes des coups joués

    def ouverture(self,b):
        """renvoi la liste des coups jouables depuis la pos selon l'ouverture"""
        ligne_partielle = ""
        suite_coups = ""
        all_coups = [] #liste de tous les coups possibles
        nb_coup = len(b.history)
        with open(self.book,'rt') as ouvertures:
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



    def la_proba(self,b):
        var = []
        for i in range(1000):
            for j in range (50):
                mList=b.gen_moves_list()
                var += [len(mList)]
                random.shuffle(mList)
                c = mList[0]
                b.domove(c[0],c[1],c[2])
            self.newgame(b)
        return var

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

        if(d<1 or d>self.MAX_PLY):
            print('Depth must be between 1 and',self.MAX_PLY)
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
    # Compteur pour la lecture des parties et fonctions en ce même sens #
    #####################################################################

    #Fonctionne pour l'instant, cependant dans l'écriture d'un fichier, il faudra sauvegarder le meta_historique
    #de sorte que l'on puisse mettre un self.history = meta_historique ou un truc dans le genre
    #comme ça on peut revenir en arrière

    def compteur(self,val):
        self.val_compteur = self.val_compteur + val

    def lire(self,b,c):
        cmd = c.split()
        partie_in = False
        with open("saves.txt",'rt') as file:
            for ligne in file:

                if cmd[1] == ligne[0:len(cmd[1])] :

                    print("Partie trouvée !")
                    historique = ligne[len(cmd[1])+ 1:]
                    print("Historique de la partie : "  + historique)
                    self.historique_lire = historique
                    partie_in = True

            if partie_in == False:
                print("Pas de partie sous ce nom dans la base.")
    #####################################################################

    def lecture(self,b,val):
        for i in range(val+1):
            coup = self.historique_lire[5*i:5*i+4]
            # print(coup)
            self.userliremove(b,coup)

    #####################################################################


    # def play_bot(self,val,b):
    #     if(self.endgame): # on ne peut pas chercher si la partie est finie
    #         self.print_result(b)
    #         return
    #
    #     coups = self.ouverture(b)
    #     if coups != []:
    #         c = coups[random.randrange(0,len(coups))]
    #         print("Coup d'ouverture : "+c)
    #         b.domove(b.caseStr2Int(c[0:2]),b.caseStr2Int(c[2:4]),c[4:])
    #         return
    #
    #
    #     self.noeuds = 0
    #     self.engine_move_list = []
    #     self.variation = [("",0) for i in range(self.MAX_PLY)]
    #
    #     ta = time.time()
    #     # maxval = self.minimax(val,0,b.side2move,b)
    #     maxval = self.ab(val,0,-self.INFINITY,self.INFINITY,b)
    #     tb = time.time()
    #
    #     print("eval : %s"%(maxval/100))
    #     print("temps : %s"%(tb-ta))
    #     print("noeuds : %s"%self.noeuds)
    #
    #
    #     list = []
    #     i = 0
    #     while self.variation[i] != ("",0):
    #         list.append(self.variation[i])
    #         i+=1
    #     print("variation principale : %s \n"%str(list))
    #
    #     random.shuffle(self.engine_move_list)
    #     # print(self.engine_move_list)
    #     for m in self.engine_move_list:
    #         if m[3] == maxval:
    #             # print(b.caseInt2Str(m[0])+b.caseInt2Str(m[1]),m[3])
    #             b.domove(m[0],m[1],m[2])
    #             self.print_result(b)
    #             break





    def minimax(self,depth,pr,couleur,b):
        self.noeuds += 1
        if depth == 0 or self.endgame:
            return b.evaluer(couleur)

        mList = b.gen_moves_list()

        if couleur==b.side2move:
            max_eval = -self.INFINITY

            for i,m in enumerate(mList):
                if(not b.domove(m[0],m[1],m[2])): #en plus de tester fait le coup
                    continue #on passe le coup si il laisse le roi en echec
                f = True
                eval = self.minimax(depth-1,pr+1,couleur,b)
                max_eval = max(max_eval, eval)
                b.undomove()

                if pr == 0:
                    self.engine_move_list.append([m[0],m[1],m[2],eval])

            #si aucun coup joué alors c'est MAT ou EGALITE
            if(not f):
                if(chk):
                    return -self.INFINITY # MAT perdant
                else:
                    return 0 # DRAW

            return max_eval


        else:
            min_eval = self.INFINITY

            for i,m in enumerate(mList):
                if(not b.domove(m[0],m[1],m[2])):
                    continue #on passe le coup si il laisse le roi en echec
                f = True
                eval = self.minimax(depth-1,pr+1,couleur,b)
                min_eval = min(min_eval, eval)
                b.undomove()

                # if pr == 1:
                #     self.engine_move_list.append([m[0],m[1],m[2],eval])

            return min_eval




    def ab(self,depth,pr,alpha,beta,b):
        self.noeuds += 1
        if depth == 0 or self.endgame:
            if pr%2==0:
                return b.evaluer(b.side2move)
            else:
                return b.evaluer(b.oppColor(b.side2move))
        # # Si le roi est en échec, on va plus loin dans l'analyse
        chk=b.in_check(b.side2move) # 'chk' used at the end of func too
        if(chk):
            depth+=1

        f = False
        mList = b.gen_moves_list()
        mList = b.tri_move(mList) #ACCELERE ENORMEMENT LES CALCULS

        if pr%2==0:

            for i,m in enumerate(mList):
                if(not b.domove(m[0],m[1],m[2])): #en plus de tester fait le coup
                    continue #on passe le coup si il laisse le roi en echec
                f = True

                eval = self.ab(depth-1,pr+1,alpha,beta,b)

                b.undomove()

                alpha = max(alpha,eval)
                if beta <= alpha:
                    break

                if pr == 0:
                    self.engine_move_list.append([m[0],m[1],m[2],eval])
            #si aucun coup joué alors c'est MAT ou EGALITE
            if(not f):
                if(chk):
                    return -self.INFINITY # MAT perdant
                else:
                    return 0 # DRAW

            return alpha


        else:

            for i,m in enumerate(mList):
                if(not b.domove(m[0],m[1],m[2])):
                    continue #on passe le coup si il laisse le roi en echec
                f = True

                eval = self.ab(depth-1,pr+1,alpha,beta,b)
                b.undomove()

                beta = min(beta,eval)
                if beta <= alpha:
                    break


            #si aucun coup joué alors c'est MAT ou EGALITE
            if(not f):
                if(chk):
                    return self.INFINITY # MAT gagnant
                else:
                    return 0 # DRAW

            return beta




    def la_proba(self,b,nb1,nb2,n):
        var = []
        for i in range(nb1):
            for j in range (nb2):
                if j > n :
                    var += [len(mList)]
                mList=b.gen_moves_list()
                random.shuffle(mList)
                c = mList[0]
                b.domove(c[0],c[1],c[2])
            self.newgame(b)
        return var
