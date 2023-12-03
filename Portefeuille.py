from datetime import date

class Portefeuille:
    def __init__(self, bourse):
        self.bourse = bourse
        self.transactions = []

    
    def déposer(self, montant, date=date.today()):
        if date > date.today():
            raise  TimeoutError
        self.liquiditer = montant
        self.transactions.append({"type": "dépôt", "montant": montant, "date": date})


    
    def solde(self,date=date.today):
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
    
    def acheter(self,symbole, quantité, date=date.today):
        if date > date.today():
            raise  TimeoutError
        self.prix_unit = self.bourse.prix(symbole, date)
        coût_total = self.prix_unit * quantité
        solde_actuel = self.solde(date) 
        
        if solde_actuel < coût_total:
            raise LiquiditéInsuffisante("Liquidité insuffisante pour effectuer l'achat.")
        self.transactions.append({"type": "achat", "symbole": symbole, "quantité": quantité, "date": date})
        self.transactions.append({"type": "dépôt", "montant": -coût_total, "date": date})


    def vendre(self,symbole, quantité, date=date.today()):
        if date > date.today():
            raise  TimeoutError
       
        self.prix_unit = self.bourse.prix(symbole, date)
        quantité_en_portefeuille = self.quantité_titres(symbole, date)

        if quantité > quantité_en_portefeuille:
            raise ErreurQuantité("Quantité insuffisante de titres pour effectuer la vente.")

        montant_vente = self.prix_unitaire * quantité

        self.transactions.append({"type": "vente", "symbole": symbole, "quantité": quantité, "date": date})
        self.transactions.append({"type": "dépôt", "montant": montant_vente, "date": date})
