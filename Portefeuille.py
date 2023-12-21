from datetime import datetime, date, timedelta
from exceptions import ErreurQuantite, LiquiditeInsuffisante, ErreurDate
from math import numpy as np
import matplotlib.pyplot as plt

class Portefeuille:
    def __init__(self, bourse):
        self.bourse = bourse
        self.transactions = []

    def deposer(self, montant, date=None):
        if date is None:
            date = datetime.now().date()
        if date > date.today():
            raise ErreurDate()
        self.liquiditer = montant
        self.transactions.append({"type": "depot", "montant": montant, "date": date})

    def solde(self, date=None):
        if date is None:
            date = datetime.now().date()
        if date > date.today():
            raise ErreurDate()
        solde = 0
        for transaction in self.transactions:
            if transaction["date"] <= date:
                if transaction["type"] == "depot":
                    solde += transaction["montant"]
                elif transaction["type"] == "vente":
                    solde += transaction["montant_liquide"]
        return solde

    def acheter(self, symbole, quantite, date=None):
        if date is None:
            date = datetime.now().date()
        if date > date.today():
            raise ErreurDate()
        prix_unit = self.bourse.prix(symbole, date)
        cout_total = prix_unit * quantite
        solde_actuel = self.solde(date)

        if solde_actuel < cout_total:
            raise LiquiditeInsuffisante("Liquidite insuffisante pour effectuer l'achat.")
        self.transactions.append({"type": "achat", "symbole": symbole, "quantite": quantite, "date": date})
        self.transactions.append({"type": "depot", "montant": -cout_total, "date": date})

    def vendre(self, symbole, quantite, date=None):
        if date is None:
            date = datetime.now().date()
        if date > date.today():
            raise ErreurDate()

        prix_unit = self.bourse.prix(symbole, date=datetime.now().date())
        quantité_en_portefeuille = self.quantite_titres(symbole, date)

        if quantite > quantité_en_portefeuille:
            raise ErreurQuantite("Quantité insuffisante de titres pour effectuer la vente.")

        montant_vente = prix_unit * quantite

        self.transactions.append({"type": "vente", "symbole": symbole, "quantité": quantite, "date": date})
        self.transactions.append({"type": "dépôt", "montant": montant_vente, "date": date})

    def valeur_totale(self, date=None):
        if date is None:
            date = datetime.now().date()
        if date > date.today():
            raise ErreurDate()

        solde_liquide = self.solde(date)
        valeur_titres = sum(
            self.bourse.prix(trans["symbole"], date) * trans["quantite"] for trans in self.transactions if
            trans["type"] == "achat"
        )
        return solde_liquide + valeur_titres

    def valeur_des_titres(self, symboles, date=None):
        if date is None:
            date = datetime.now().date()
        if date > date.today():
            raise ErreurDate()

        valeur_titres = sum(
            self.bourse.prix(symbole, date) * self.quantité_titres(symbole, date) for symbole in symboles
        )
        return valeur_titres

    def titres(self, date=None):
        if date is None:
            date = datetime.now().date()
        if date > date.today():
            raise ErreurDate()

        titres_en_portefeuille = {}
        for trans in self.transactions:
            if trans["type"] == "achat" and trans["date"] <= date:
                symbole = trans["symbole"]
                quantité = trans["quantité"]
                if symbole in titres_en_portefeuille:
                    titres_en_portefeuille[symbole] += quantité
                else:
                    titres_en_portefeuille[symbole] = quantité

        return titres_en_portefeuille

    def valeur_projetee(self, date, rendement):
        valeur_initiale = self.valeur_totale()
        années = (date - datetime.now().date()).days // 365
        valeur_projetee = valeur_initiale * (1 + rendement / 100) ** années
        jours = (date - datetime.now().date()).days % 365
        valeur_projetée += valeur_initiale * (rendement / 100) * (jours / 365)
        return valeur_projetée

    def quantite_titres(self, symbole, date):
        quantite = sum(
            trans["quantité"]
            for trans in self.transactions
            if trans["type"] == "achat" and trans["symbole"] == symbole and trans["date"] <= date
        )
        return quantite
   
    def valeur_projetee_avec_volatilite(self, date, rendement, volatilite, nb_simulations=1000):
        valeur_initiale = self.valeur_totale()
        années = (date - datetime.now().date()).days // 365
        jours = (date - datetime.now().date()).days % 365

        rendements_annuels = np.random.normal(rendement / 100, volatilite / 100, nb_simulations)
        valeurs_projetees = valeur_initiale * np.power(1 + rendements_annuels, années)
        valeurs_projetees += valeur_initiale * rendements_annuels * (jours / 365)

        return np.percentile(valeurs_projetees, [25, 50, 75])

    def projection_aleatoire(self, date, rendements_par_symbole):
        valeur_projete = 0
        for symbole, (mu, sigma) in rendements_par_symbole.items():
            quantite = self.quantite_titres(symbole, date)
            if quantite > 0:
                prix_actuel = self.bourse.prix(symbole, date)
                rendement_annuel = np.random.normal(mu / 100, sigma / 100)
                valeur_projete += quantite * prix_actuel * (1 + rendement_annuel)

        return valeur_projete
    



class PortefeuilleGraphique(Portefeuille):
    def __init__(self, bourse):
        super().__init__(bourse)

    def graphique_historique(self, symboles, date_debut):
        plt.figure(figsize=(10, 6))
        for symbole in symboles:
            dates, prix = self.bourse.historique(symbole, date_debut)
            plt.plot(dates, prix, label=symbole)
        plt.title("Historique des Prix des Actions")
        plt.xlabel("Date")
        plt.ylabel("Prix")
        plt.legend()
        plt.show()

    def graphique_projection(self, date, rendement, volatilite):
        quartiles = self.valeur_projetee_avec_volatilite(date, rendement, volatilite)
        dates = [date - timedelta(months=3*i) for i in range(4)]
        plt.figure(figsize=(10, 6))
        for i, q in enumerate(quartiles):
            plt.plot(dates, [q]*len(dates), label=f"Q{i+1}")
        plt.title("Projection des Quartiles de Valeur du Portefeuille")
        plt.xlabel("Date")
        plt.ylabel("Valeur Projetée")
        plt.legend()
        plt.show()
