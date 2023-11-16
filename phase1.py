import argparse
import requests
import json
from datetime import datetime

def analyser_commande():
    parser = argparse.ArgumentParser(description="Extraction de valeurs historiques pour un ou plusieurs symboles boursiers.")
    parser.add_argument('-d', '--debut', type=lambda d: datetime.strptime(d, '%Y-%m-%d').date(), help='Date recherchée la plus ancienne (format: AAAA-MM-JJ)', metavar='DATE')
    parser.add_argument('-f', '--fin', type=lambda d: datetime.strptime(d, '%Y-%m-%d').date(), help='Date recherchée la plus récente (format: AAAA-MM-JJ)', metavar='DATE')
    parser.add_argument('-v', '--valeur', type=str, choices=['fermeture', 'ouverture', 'min', 'max', 'volume'],
                        default='fermeture', help='La valeur désirée (par défaut: fermeture)')
    parser.add_argument('symbole', nargs='+', help='Nom d\'un symbole boursier')
    return parser.parse_args()

def produire_historique(symbole, debut, fin, valeur):
    url = f'https://pax.ulaval.ca/action/{symbole}/historique/'
    params = {'début': debut.strftime('%Y-%m-%d'), 'fin': fin.strftime('%Y-%m-%d')}
    
    reponse = requests.get(url=url, params=params)
    donnees = json.loads(reponse.text)
    
    historique = donnees['historique']
    
    resultats = [(datetime.strptime(date, '%Y-%m-%d').date(), day_data[valeur]) 
                 for date, day_data in historique.items() if valeur in day_data]
    
    resultats.sort(key=lambda x: x[0])
    
    return resultats

if __name__ == '__main__':
    args = analyser_commande()
    print(args)
