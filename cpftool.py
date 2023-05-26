#!/usr/bin/env python3

import sys
import random
import argparse


__BANNER = sys.argv[0].split('/')[-1].split('.')[0] + ''' \
[options]
    -h, --help              this
    -p, --pretty            print CPFs with field separators
    -v, --verify   [CPF]    verify the validity of [CPF]
    -s, --state    [state]  set the CPF state for validation or generation
    -g, --generate [n]      generate [n] random and valid CPF numbers\
'''

__STATE_DIGIT = {
    'ac': 2, 'al': 4, 'ap': 2, 'am': 2, 'ba': 5, 'ce': 3, 'df': 1, 'es': 7,
    'go': 1, 'ma': 3, 'mt': 1, 'ms': 1, 'mg': 6, 'pa': 2, 'pb': 4, 'pr': 9,
    'pe': 4, 'pi': 3, 'rj': 7, 'rn': 4, 'rs': 0, 'ro': 2, 'rr': 2, 'sc': 9,
    'sp': 8, 'se': 5, 'to': 1
}


# Sanitize a valid CPF string
def sanitize(cpf: str) -> str:
    return cpf.replace('.', '').replace('-', '')

# Add separators to CPF string
def prettify(cpf: str) -> str:
    return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'

# Generate CPF verifying digits for a numeric string
def verifying_digits(s: str) -> tuple:
    cpf = [int(c) for c in s]

    if (vd1 := sum(n * (i + 1) for i, n in enumerate(cpf)) % 11) == 10:
        vd1 = 0

    if (vd2 := sum(n * i for i, n in enumerate(cpf + [vd1])) % 11) == 10:
        vd2 = 0

    return (vd1, vd2)


# Validate a CPF string
def validate(s: str, state=None) -> bool:
    if not len(s) == 11 and s.isnumeric():
        return False

    if state and int(s[8]) != __STATE_DIGIT[state]:
        return False

    return verifying_digits(s[:9]) == tuple(int(c) for c in s[9:])


# Generate CPF
def generate(n: int, state=None):
    if state is None:
        state = random.choice(list(__STATE_DIGIT))
    elif state not in __STATE_DIGIT:
        raise ValueError('Invalid state')

    sd = __STATE_DIGIT[state]

    for _ in range(n):
        base = f'{random.randrange(10)}{str(random.randrange(1000000, 9999999))}'
        vd = verifying_digits(base)

        yield f'{base}{sd}{vd[0]}{vd[1]}'


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__BANNER)
        sys.exit(1)

    parser = argparse.ArgumentParser(
        usage=__BANNER, description='CPFTool', add_help=False
    )

    parser.add_argument('-h', '--help', action='store_true')
    parser.add_argument('-p', '--pretty', action='store_true')
    parser.add_argument('-v', '--verify', type = str, default=None)
    parser.add_argument('-s', '--state', type = str, default=None)
    parser.add_argument('-g', '--generate', type = int, default=None)

    args = parser.parse_args()

    if args.help:
        print(__BANNER)
        sys.exit(0)

    if not (args.verify or args.generate):
        print(__BANNER)
        sys.exit(1)

    if args.verify:
        sys.exit(0 if validate(sanitize(args.verify), state=args.state) else 1)

    if args.generate:
        for cpf in generate(args.generate, state=args.state):
            print(cpf if not args.pretty else prettify(cpf))

