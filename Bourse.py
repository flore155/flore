from datetime import datetime
from exceptions import ErreurDate
import requests
import json

class Bourse:
    def prix(self,symbole,_date):
        self.symbole = symbole 
        self.date = _date
        url = f'https://pax.ulaval.ca/action/{symbole}/historique/'
        réponse = requests.get(url=url)#, params=params)
        réponse = json.loads(réponse.text)
        historique = réponse['historique']
        historique = dict(reversed(sorted(historique.items())))
        date_en_cours = datetime.today()
        date_en_cours = date_en_cours.strftime('%Y-%m-%d')
        date_en_cours_obj = datetime.strptime(date_en_cours,'%Y-%m-%d')
        _date_obj = datetime.strptime(_date,'%Y-%m-%d')
        if _date_obj>date_en_cours_obj:
            raise ErreurDate("Erreur date")
        elif historique.get(_date)!=None:
            valeur = historique[_date]['fermeture']
        #elif _date_obj == date_en_cours_obj:
         #   valeur = historique[_date]['fermeture']
        else:
            _date = datetime.strptime(_date,'%Y-%m-%d')
            for dat_historique in réponse['historique'].keys():
                dat_historique_obj = datetime.strptime(dat_historique, '%Y-%m-%d')
                if dat_historique_obj < _date_obj:
                    valeur = historique[dat_historique]['fermeture']
                    break
        
        return valeur

#print(Bourse().prix('goog', '2023-12-03'))