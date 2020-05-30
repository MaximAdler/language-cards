import json
import random
import time
from argparse import ArgumentParser
from datetime import datetime

from pyfiglet import Figlet
from termcolor import colored


from constants import CONGRATS, FIGLET_FONT
from helpers import clear_window

FIGLET = Figlet(justify='center', font=FIGLET_FONT)
ACCEPT_CHANGES = FIGLET.renderText('Got it')

clear_window()

parser = ArgumentParser(description='Tool for learning English.')
parser.add_argument('--new', dest='new_pair', help='Add new pair of words.',
                    nargs=2, metavar=('original', 'translation'), type=str)
parser.add_argument('--train', dest='train', help='Start training (using cards).', choices=('all', 'new',))
parser.add_argument('--settings', dest='settings', help='Change settings of tool.', nargs=2,
                    metavar=('option', 'value'))

args = parser.parse_args()

if all(val is None for val in args.__dict__.values()):
    print(FIGLET.renderText('Just do it motherfucker'))
    parser.print_help()

if args.new_pair is not None:
    original, translation = args.new_pair

    with open('dictionary.json') as dictionary:
        dictionary = json.loads(dictionary.read())

    next_id = int(max(dictionary)) + 1

    dictionary[next_id] = {
        'original': original,
        'translation': translation,
        'creation_date': str(datetime.now()),
        'learned': False,
        'count': 0,
    }

    with open('dictionary.json', 'w') as f:
        f.write(json.dumps(dictionary))

    print(ACCEPT_CHANGES)

if args.train is not None:
    with open('settings.json') as settings:
        settings = json.loads(settings.read())

    with open('dictionary.json', encoding='utf-8') as dictionary:
        dictionary = json.loads(dictionary.read())

    train_cards = [
        (_id, dictionary[_id],) for _id in dictionary if args.train == 'all' or not dictionary[_id]['learned']
    ]
    card_type = 'original'

    for i in range(3, 0, -1):
        print('Okay dude. Let\'s try...')
        print(FIGLET.renderText(str(i)))
        time.sleep(1)
        clear_window()

    for _ in range(settings['cards_per_training']):
        card = random.choice(train_cards)
        if settings['mixed']:
            card_type = random.choice(['original', 'translation'])

        print(FIGLET.renderText(f'---------\n{card[1][card_type]}\n---------\n'))
        answer = input('Type your translation here: ')

        real_answer = card[1]['original' if card_type == 'translation' else 'translation']
        if answer == real_answer:
            print(colored(FIGLET.renderText(random.choice(CONGRATS)), 'green'))
            time.sleep(1)

            card[1]['count'] += 1
            if card[1]['count'] >= 5:
                card[1]['learned'] = True
            dictionary[card[0]] = card[1]

            with open('dictionary.json', 'w') as f:
                f.write(json.dumps(dictionary))
        else:
            print(colored(FIGLET.renderText('Wrong!'), 'red'))
            print(f'Answer was: {real_answer}')
            time.sleep(4)

            clear_window()


if args.settings is not None:
    option, value = args.settings

    with open('settings.json') as settings:
        settings = json.loads(settings.read())

    if option not in settings:
        raise BaseException(f'No such option in settings. Possible options: {list(settings.keys())}')

    value_type = type(settings[option])
    settings[option] = value_type(value)

    with open('settings.json', 'w') as f:
        f.write(json.dumps(settings))

    print(ACCEPT_CHANGES)
