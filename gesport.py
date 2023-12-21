import argparse
from datetime import datetime
import bourse
import portefeuille 
from exceptions import ErreurQuantité, LiquiditéInsuffisante, ErreurDate
def analyse_commande():

    parser = argparse.ArgumentParser(description="Gestionnaire de portefeuille d'actions")
    
    parser.add_argument("-h", "--help", help="show this help message and exit")
    parser.add_argument("-d Date", "--date", help="Date effective(par defaut, date du jour)", default=datetime.now().strftime("%Y-%m-%d"))
    parser.add_argument("-q INT","--quantite", help="Quantite desiree(par defaut: 1)", type=int, default=1)
    parser.add_argument("-t [STRING [STRING...]]", "--titres [STRINGS[STRINGS ...]]", help="Le ou les titres a considerer(par defaut, tous les titres du portefeuille sont consideres)",nargs="*", default=[])
    parser.add_argument("-r FLOAT","--rendement FLOAT", help="rendement annuel global(par defaut, 0)",type=float, default=0)
    parser.add_argument("-v FLOat", "--volabilite FLOAT", type=float,default=0, help="indice de volabilite global sur le rendement annuel(par defaut, 0)")
    parser.add_argument("-g BOOL", "--graphique BOOL", action="strore_true", default='false', help="Affichage graphique(par defaut, pas d'affichage graphique)")
    parser.add_argument("-p String", "--portefeuille STRING", help="Nom de portefeuille(par defaut, utiliser folio)", default='folio')


if __name__ =="__main__":
    analyse_commande()