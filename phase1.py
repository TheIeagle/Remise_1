import argparse
from datetime import datetime
import json
import requests

def analyser_commande():
    parser = argparse.ArgumentParser(description="Extraction de valeurs historiques pour un ou plusieurs symboles boursiers.")
    parser.add_argument('-d', '--debut', type=lambda d: datetime.strptime(d, '%Y-%m-%d').date(), help='Date recherchée la plus ancienne (format: AAAA-MM-JJ)', metavar='DATE')
    parser.add_argument('-f', '--fin', type=lambda d: datetime.strptime(d, '%Y-%m-%d').date(), help='Date recherchée la plus récente (format: AAAA-MM-JJ)', metavar='DATE')
    parser.add_argument('-v', '--valeur', type=str, choices=['fermeture', 'ouverture', 'min', 'max', 'volume'],
                        default='fermeture', help='La valeur désirée (par défaut: fermeture)')
    parser.add_argument('symbole', nargs='+', help='Nom d\'un symbole boursier')

    args = parser.parse_args()

    for symbole in args.symbole:
        if not args.debut:
            args.debut = args.fin
        if not args.fin:
            args.fin = datetime.now().date()

        historique = produire_historique(symbole, args.debut, args.fin, args.valeur)

        print(f'titre={symbole}: valeur={args.valeur}, début=datetime.date({args.debut.year}, {args.debut.month}, {args.debut.day}), fin=datetime.date({args.fin.year}, {args.fin.month}, {args.fin.day})')
        historique_formatte = [(f'datetime.date({d.year}, {d.month}, {d.day})', v) for d, v in historique]
        print(historique_formatte)

def produire_historique(symbole, debut, fin, valeur):
    url = f'https://pax.ulaval.ca/action/{symbole}/historique/'
    params = {'début': debut.strftime('%Y-%m-%d'), 'fin': fin.strftime('%Y-%m-%d')}

    reponse = requests.get(url=url, params=params)
    donnees = json.loads(reponse.text)

    if 'message d\'erreur' in donnees:
        raise ValueError(donnees['message d\'erreur'])

    historique = donnees['historique']

    resultats = [(datetime.strptime(date, '%Y-%m-%d').date(), day_data[valeur])
                 for date, day_data in historique.items() if valeur in day_data]

    resultats.sort(key=lambda x: x[0])

    return resultats

analyser_commande()