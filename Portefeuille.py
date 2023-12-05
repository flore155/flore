"""Contient la classe Portefeuille"""
from datetime import datetime
from exceptions import ErreurQuantite, LiquiditeInsuffisante, ErreurDate

class Portefeuille:
    """Encapsule les methodes de transactions"""
    def __init__(self, bourse):
        """Construit le Portefeuille"""
        self.bourse = bourse
        self.transactions = {}
        self.liquiditer = 0

    def deposer(self, montant, date=datetime.now().date()):
        """Depose le montant liquide dans le portefeuille"""
        if date > date.today():
            raise ErreurDate()
        self.liquiditer = montant
        self.transactions.append({"type": "depôt", "montant": montant, "date": date})

    def solde(self, date=datetime.now().date()):
        """Retourne le solde des liquiditées du Portefeuille"""
        if date > date.today():
            raise ErreurDate()
        solde = 0
        for transaction in self.transactions:
            if transaction["date"] <= date:
                if transaction["type"] == "depôt":
                    solde += transaction["montant"]
                elif transaction["type"] == "vente":
                    solde += transaction["montant_liquide"]
        return solde

    def acheter(self, symbole, quantite, date=datetime.now().date()):
        """Effectue l'achat de la quantité d'actions souhaitée"""
        if date > date.today():
            raise ErreurDate()
        prix_unit = self.bourse.prix(symbole, date)
        cout_total = prix_unit * quantite
        solde_actuel = self.solde(date)
        if solde_actuel < cout_total:
            raise LiquiditeInsuffisante("Liquidite insuffisante pour effectuer l'achat.")
        self.transactions.append({"type": "achat", "symbole": symbole,
                                  "quantité": quantite, "date": date})
        self.transactions.append({"type": "depôt", "montant": -cout_total, "date": date})

    def vendre(self, symbole, quantite, date=datetime.now().date()):
        """Effectue une vente de la quantité d'actions souhaitée"""
        if date > date.today():
            raise ErreurDate()
        prix_unit = self.bourse.prix(symbole, date=datetime.now().date())
        quantite_en_portefeuille = self.quantite_titres(symbole, date)

        if quantite > quantite_en_portefeuille:
            raise ErreurQuantite("Quantité insuffisante de titres pour effectuer la vente.")

        montant_vente = prix_unit * quantite

        self.transactions.append({"type": "vente", "symbole":
                                symbole, "quantité": quantite, "date": date})
        self.transactions.append({"type": "depôt", "montant":
                                  montant_vente, "date": date})

    def valeur_totale(self, date=datetime.now().date()):
        """Retourne la valeur totale du Portefeuille"""
        if date > date.today():
            raise ErreurDate()
        solde_liquide = self.solde(date)
        valeur_titres = sum(self.bourse.prix(trans["symbole"], date) * trans["quantité"]
                            for trans in self.transactions if trans["type"] == "achat")
        return solde_liquide + valeur_titres

    def valeur_des_titres(self, symboles, date=datetime.now().date()):
        """retourne pour la date spécifiée la valeur totale des titres spécifiés"""
        if date > date.today():
            raise ErreurDate()
        valeur_titres = sum(self.bourse.prix(symbole, date) * self.quantite_titres(symbole, date)
                            for symbole in symboles)
        return valeur_titres

    def titres(self, date=datetime.now().date()):
        """retourne pour la date spécifiée en argument, un dictionnaire des
        symboles de tous les titres du portefeuille à cette date"""
        if date > date.today():
            raise ErreurDate()
        titres_en_portefeuille = {}
        for trans in self.transactions:
            if trans["type"] == "achat" and trans["date"] <= date:
                symbole = trans["symbole"]
                quantite = trans["quantité"]
                if symbole in titres_en_portefeuille:
                    titres_en_portefeuille[symbole] += quantite
                else:
                    titres_en_portefeuille[symbole] = quantite

        return titres_en_portefeuille

    def valeur_projetee(self, date, rendement):
        """retourne la valeur du portefeuille projetée à cette date"""
        valeur_initiale = self.valeur_totale()
        annees = (date - datetime.now().date()).days // 365
        valeur_projetee = valeur_initiale * (1 + rendement / 100) ** annees
        jours = (date - datetime.now().date()).days % 365
        valeur_projetee += valeur_initiale * (rendement / 100) * (jours / 365)
        return valeur_projetee

    def quantite_titres(self, symbole, date):
        """retourne la quantite de titre correspondant à un symbole"""
        quantite = sum(trans["quantité"]
                       for trans in self.transactions
                       if trans["type"] == "achat" and
                       trans["symbole"] == symbole and trans["date"] <= date)
        return quantite
    