import math
import sys

class Grille:
    def __init__(self):
        self.cellules = [' '] * 9

    def afficher(self):
        print()
        for i in range(3):
            print(' ' + ' | '.join(self.cellules[i*3:(i+1)*3]))
            if i < 2:
                print('---+---+---')
        print()

    def jouer_coup(self, position, symbole):
        if 0 <= position < 9 and self.cellules[position] == ' ':
            self.cellules[position] = symbole
            return True
        return False

    def coups_disponibles(self):
        return [i for i, v in enumerate(self.cellules) if v == ' ']

    def est_pleine(self):
        return all(c != ' ' for c in self.cellules)

    def gagnant(self):
        lignes = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        for a,b,c in lignes:
            if self.cellules[a] == self.cellules[b] == self.cellules[c] and self.cellules[a] != ' ':
                return self.cellules[a]
        return None

class Entree:
    def demander(self, invite):
        return input(invite)

class EntreeSimulee:
    def __init__(self, reponses):
        self.reponses = list(reponses)

    def demander(self, invite):
        if self.reponses:
            return self.reponses.pop(0)
        return '1'

class Joueur:
    def __init__(self, symbole):
        self.symbole = symbole

    def obtenir_coup(self, grille):
        raise NotImplementedError

class JoueurHumain(Joueur):
    def __init__(self, symbole, entree, nom='Joueur'):
        super().__init__(symbole)
        self.nom = nom
        self.entree = entree

    def obtenir_coup(self, grille):
        coups = grille.coups_disponibles()
        while True:
            choix = self.entree.demander(f"{self.nom} ({self.symbole}) - position (1-9): ")
            try:
                pos = int(choix) - 1
                if pos in coups:
                    return pos
            except:
                pass
            if coups:
                return coups[0]

class JoueurOrdinateur(Joueur):
    def __init__(self, symbole):
        super().__init__(symbole)
        self.adversaire = 'O' if symbole == 'X' else 'X'

    def obtenir_coup(self, grille):
        meilleur_score = -math.inf
        meilleur_coup = None
        for coup in grille.coups_disponibles():
            grille.cellules[coup] = self.symbole
            score = self.minimax(grille, False)
            grille.cellules[coup] = ' '
            if score > meilleur_score:
                meilleur_score = score
                meilleur_coup = coup
        return meilleur_coup

    def minimax(self, grille, maximisant):
        gagnant = grille.gagnant()
        if gagnant == self.symbole:
            return 1
        if gagnant == self.adversaire:
            return -1
        if grille.est_pleine():
            return 0
        if maximisant:
            meilleur = -math.inf
            for coup in grille.coups_disponibles():
                grille.cellules[coup] = self.symbole
                val = self.minimax(grille, False)
                grille.cellules[coup] = ' '
                meilleur = max(meilleur, val)
            return meilleur
        else:
            meilleur = math.inf
            for coup in grille.coups_disponibles():
                grille.cellules[coup] = self.adversaire
                val = self.minimax(grille, True)
                grille.cellules[coup] = ' '
                meilleur = min(meilleur, val)
            return meilleur

class Jeu:
    def __init__(self, entree=None):
        self.entree = entree if entree else Entree()
        self.grille = Grille()
        self.joueurs = []

    def choisir_mode(self):
        print('Modes:')
        print('1) Joueur vs Joueur')
        print('2) Joueur vs Ordinateur')
        print('3) Ordinateur vs Ordinateur')
        while True:
            choix = self.entree.demander('Choisis un mode (1-3): ')
            if choix in ('1','2','3'):
                return int(choix)

    def configurer_joueurs(self, mode):
        if mode == 1:
            j1 = JoueurHumain('X', self.entree, 'Joueur 1')
            j2 = JoueurHumain('O', self.entree, 'Joueur 2')
        elif mode == 2:
            premier = self.entree.demander('Qui commence ? (1 toi, 2 ordi): ')
            if premier == '2':
                j1 = JoueurOrdinateur('X')
                j2 = JoueurHumain('O', self.entree)
            else:
                j1 = JoueurHumain('X', self.entree)
                j2 = JoueurOrdinateur('O')
        else:
            j1 = JoueurOrdinateur('X')
            j2 = JoueurOrdinateur('O')
        self.joueurs = [j1, j2]

    def jouer_une_partie(self):
        self.grille = Grille()
        courant = 0
        while True:
            self.grille.afficher()
            joueur = self.joueurs[courant]
            coup = joueur.obtenir_coup(self.grille)
            self.grille.jouer_coup(coup, joueur.symbole)
            gagnant = self.grille.gagnant()
            if gagnant:
                self.grille.afficher()
                print(f'Le gagnant est {gagnant}!')
                return gagnant
            if self.grille.est_pleine():
                self.grille.afficher()
                print('Match nul!')
                return None
            courant = 1 - courant

    def jouer(self):
        mode = self.choisir_mode()
        self.configurer_joueurs(mode)
        return self.jouer_une_partie()

if __name__ == '__main__':
    jeu = Jeu()
    jeu.jouer()
