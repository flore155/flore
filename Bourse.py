from datetime import datetime
from exceptions import ErreurDate
import requests
import json

class Bourse:
    def prix(self, symbole, _date):
        url = f'https://pax.ulaval.ca/action/{symbole}/historique/'
        réponse = requests.get(url=url)
        réponse = json.loads(réponse.text)

        historique = réponse.get('historique', {})
        historique = dict(reversed(sorted(historique.items())))

        date_en_cours = datetime.today().date()
        _date_str = _date.strftime('%Y-%m-%d')

        if _date > date_en_cours:
            raise ErreurDate("Erreur date")

        valeur = None

        if _date_str in historique:
            valeur = historique[_date_str]['fermeture']
        else:
            for dat_historique, valeurs in historique.items():
                dat_historique_obj = datetime.strptime(dat_historique, '%Y-%m-%d').date()
                if dat_historique_obj <= _date:
                    valeur = valeurs['fermeture']
                    break

        if valeur is None:
            raise ErreurDate("Aucune valeur trouvée pour la date spécifiée")

        return valeur