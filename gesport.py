# gesport.py

import argparse
from Bourse import Bourse
from Portefeuille import Portefeuille, PortefeuilleGraphique
from exceptions import ErreurQuantite, LiquiditeInsuffisante, ErreurDate

def analyser_commande():
    parser = argparse.ArgumentParser(description="Gestionnaire de portefeuille d'actions")

    parser.add_argument('action', choices=['deposer', 'acheter', 'vendre', 'lister', 'projeter'],
                        help='Action à effectuer')

    parser.add_argument('-d DATE', '--date DATE', help='Date spécifiée (par défaut, date du jour)')
    parser.add_argument('-q INT', '--quantite INT', type=int, default=1, help='Quantité désirée (par défaut 1)')
    parser.add_argument('-t  STRING [STRING [STRING ...]]', '--titres  STRING [STRING [STRING ...]]', nargs='+', help='Le ou les titres à considérer')
    parser.add_argument('-r FLOAT', '--rendement FLOAT', type=float, default=0, help='Rendement annuel global (par défaut 0)')
    parser.add_argument('-v FLOAT', '--volatilite FLOAT', type=float, default=0, help='Indice de volatilité global sur le rendement annuel (par défaut 0)')
    parser.add_argument('-g BOOL', '--graphique BOOL', action='store_true', help='Affichage graphique (par défaut, pas d\'affichage graphique)')
    parser.add_argument('-p STRING', '--portefeuille STRING', default='folio', help='Nom du portefeuille (par défaut, utiliser folio)')

    return parser.parse_args()

def deposer(portefeuille, montant, date):
    portefeuille.deposer(montant, date)
    print(f"Solde après dépôt: {portefeuille.solde()}")

def acheter(portefeuille, titres, quantite, date):
    for titre in titres:
        portefeuille.acheter(titre, quantite, date)
    print(f"Solde après achat: {portefeuille.solde()}")

# Fonction pour la sous-commande 'vendre'
def vendre(portefeuille, titres, quantite, date):
    for titre in titres:
        portefeuille.vendre(titre, quantite, date)
    print(f"Solde après vente: {portefeuille.solde()}")

# Fonction pour la sous-commande 'lister'
def lister(portefeuille, date):
    for titre, quantite in portefeuille.titres(date).items():
        print(f"{titre} = {quantite} x {portefeuille.bourse.prix(titre, date)}")

# Fonction pour la sous-commande 'projeter'
def projeter(portefeuille, date, rendement, volatilite):
    valeur_projete = portefeuille.valeur_projetee_avec_volatilite(date, rendement, volatilite)
    print(f"Valeur projetée = {valeur_projete}")

if __name__ == "__main__":
    args = analyser_commande()
    # Création des instances de Bourse et Portefeuille
    bourse = Bourse()
    portefeuille = Portefeuille(bourse)
    nom_fichier_portefeuille = args.portefeuille if args.portefeuille else "folio.json"
    portefeuille = Portefeuille(bourse, nom_fichier_portefeuille)


    try:
        if args.action == "deposer":
            deposer(portefeuille, args.quantite, args.date)
            portefeuille.ecrire_json()
        elif args.action == "acheter":
            acheter(portefeuille, args.titres, args.quantite, args.date)
            portefeuille.ecrire_json()
        elif args.action == "vendre":
            vendre(portefeuille, args.titres, args.quantite, args.date)
            portefeuille.ecrire_json()
        elif args.action == "lister":
            lister(portefeuille, args.date)
            portefeuille.ecrire_json()
        elif args.action == "projeter":
            projeter(portefeuille, args.date, args.rendement, args.volatilite)
            portefeuille.ecrire_json()
    
    except (ErreurDate, ErreurQuantite, LiquiditeInsuffisante) as e:
        print(f"Erreur : {e}")