from datetime import datetime

class Portefeuille:
    def __init__(self, bourse):
        self.bourse = bourse
        self.transactions = []

    
    def déposer(self, montant, date=datetime.now().date()):
        if date > date.today():
            raise  TimeoutError
        self.liquiditer = montant
        self.transactions.append({"type": "dépôt", "montant": montant, "date": date})


    
    def solde(self,date=datetime.now().date()):
        if date > date.today():
            raise  TimeoutError
        solde = 0
        for transaction in self.transactions :
            if transaction["date"] <= date:
                if transaction["type"] == "dépôt":
                    solde += transaction["montant"]
                elif transaction["type"] == "vente":
                    solde += transaction["montant_liquide"]

        return solde
    
    def acheter(self,symbole, quantité, date=datetime.now().date()):
        if date > date.today():
            raise  TimeoutError
        prix_unit = self.bourse.prix(symbole, date)
        coût_total = prix_unit * quantité
        solde_actuel = self.solde(date) 
        
        if solde_actuel < coût_total:
            raise LiquiditéInsuffisante("Liquidité insuffisante pour effectuer l'achat.")
        self.transactions.append({"type": "achat", "symbole": symbole, "quantité": quantité, "date": date})
        self.transactions.append({"type": "dépôt", "montant": -coût_total, "date": date})


    def vendre(self,symbole, quantité, date=datetime.now().date()):
        if date > date.today():
            raise  TimeoutError
       
        prix_unit = self.bourse.prix(symbole, date=datetime.now().date())
        quantité_en_portefeuille = self.quantité_titres(symbole, date)

        if quantité > quantité_en_portefeuille:
            raise ErreurQuantité("Quantité insuffisante de titres pour effectuer la vente.")

        montant_vente = prix_unit * quantité

        self.transactions.append({"type": "vente", "symbole": symbole, "quantité": quantité, "date": date})
        self.transactions.append({"type": "dépôt", "montant": montant_vente, "date": date})
    
    def valeur_totale(self, date=datetime.now().date()):
        if date > date.today():
            raise  TimeoutError
        
        solde_liquide = self.solde(date)
        valeur_titres = sum(self.bourse.prix(trans["symbole"], date) * trans["quantité"]
                            for trans in self.transactions if trans["type"] == "achat")
        return solde_liquide + valeur_titres