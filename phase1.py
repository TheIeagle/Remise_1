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

if __name__ == '__main__':
    args = analyser_commande()
    print(args)