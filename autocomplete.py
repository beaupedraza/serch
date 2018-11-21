import requests
import argparse
import csv
import os
import sys



def autocomplete(query):
    ENDPOINTS = ['https://www.google.com/complete/search', 'http://suggestqueries.google.com/complete/search']
    ENDPOINT = ENDPOINTS[0]

    payload = {'client': 'firefox', 'q': query}
    response = requests.get(ENDPOINT, params=payload)
    return response.json()[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inp', help='Input file containing search terms', type=str, default='input.txt')
    parser.add_argument('-o', '--out', help='Output CSV file', type=str, default='autocomplete.csv')
    parser.add_argument('-c', '--cli', help='If the program is to be run in interactive CLI mode', action='store_true')

    args = parser.parse_args()

    if args.cli:
        query = input('[*] Enter query: ')
        print('[*] Autocomplete results: {}'.format(autocomplete(query)))
    else:
        print('[*] Reading queries from {}'.format(args.inp))
        with open(args.inp) as f:
            inp = f.readlines()

        print('[*] Fetching autocomplete data')
        with open(args.out, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            inp = [i.rstrip(os.linesep) for i in inp]
            inp = [i for i in inp if i]
            done = 0

            for query in inp:
                sys.stdout.write('\r[*] Keywords searched: {}'.format(done))
                writer.writerow([query] + autocomplete(query))
                done = done + 1
                sys.stdout.flush()
        print()
        print('[*] Done!')


if __name__=='__main__':
    main()