from datetime import datetime, date
from exceptions import ErreurQuantité, LiquiditéInsuffisante, ErreurDate

class Portefeuille:
    def __init__(self, bourse,date=None):
        self.bourse = bourse()
        self.transactions = []
        self.date = date()

    def déposer(self, montant, date=None):
        if date == None:
            date = datetime.now().date()
        if date > date.today():
            raise ErreurDate()
        self.liquiditer = montant
        self.transactions.append({"type": "dépôt", "montant": montant, "date": date})

    def solde(self, date=None):
        if date == None:
            date = datetime.now().date()
        if date > date.today():
            raise ErreurDate()
        solde = 0
        for transaction in self.transactions:
            if transaction["date"] <= date:
                if transaction["type"] == "dépôt":
                    solde += transaction["montant"]
                elif transaction["type"] == "vente":
                    solde += transaction["montant_liquide"]
        return solde

    def acheter(self, symbole, quantité, date=None):
        if date == None:
            date=datetime.now().date()
        if date > date.today():
            raise ErreurDate()
        prix_unit = self.bourse.prix(symbole, date)
        coût_total = prix_unit * quantité
        solde_actuel = self.solde(date)
        
        if solde_actuel < coût_total:
            raise LiquiditéInsuffisante("Liquidité insuffisante pour effectuer l'achat.")
            
        self.transactions.append({"type": "achat", "symbole": symbole, "quantité": quantité, "date": date})
        self.transactions.append({"type": "dépôt", "montant": -coût_total, "date": date})

    def vendre(self, symbole, quantité, date=None):
        if date == None:
            date=datetime.now().date()
        if date > date.today():
            raise ErreurDate()
        
        prix_unit = self.bourse.prix(symbole, date=datetime.now().date())
        quantité_en_portefeuille = self.quantité_titres(symbole, date)

        if quantité > quantité_en_portefeuille:
            raise ErreurQuantité("Quantité insuffisante de titres pour effectuer la vente.")

        montant_vente = prix_unit * quantité

        self.transactions.append({"type": "vente", "symbole": symbole, "quantité": quantité, "date": date})
        self.transactions.append({"type": "dépôt", "montant": montant_vente, "date": date})

    def valeur_totale(self, date=None):
        if date == None:
            date=datetime.now().date()
        if date > date.today():
            raise ErreurDate()
        
        solde_liquide = self.solde(date)
        valeur_titres = sum(self.bourse.prix(trans["symbole"], date) * trans["quantité"]
                            for trans in self.transactions if trans["type"] == "achat")
        return solde_liquide + valeur_titres

    def valeur_des_titres(self, symboles, date=None):
        if date == None:
            date=datetime.now().date()
        if date > date.today():
            raise ErreurDate()
        
        valeur_titres = sum(self.bourse.prix(symbole, date) * self.quantité_titres(symbole, date)
                            for symbole in symboles)
        return valeur_titres

    def titres(self, date=None):
        if date == None:
            date=datetime.now().date()
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

    def valeur_projetée(self, date, rendement):
        valeur_initiale = self.valeur_totale()
        années = (date - datetime.now().date()).days // 365
        valeur_projetée = valeur_initiale * (1 + rendement / 100) ** années
        return valeur_projetée

    def quantité_titres(self, symbole, date):
        quantité = sum(trans["quantité"]
                       for trans in self.transactions
                       if trans["type"] == "achat" and trans["symbole"] == symbole and trans["date"] <= date)
        return quantité
