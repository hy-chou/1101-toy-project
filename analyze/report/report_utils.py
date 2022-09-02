from os import listdir


def addunit(num=-1, unit='  '):
    if num < 10 ** 3:
        snum = str(num)[:4]
    elif num < 10 ** 6:
        snum = str(num/10**3)[:4]
        unit = ' k'
    elif num < 10 ** 9:
        snum = str(num/10**6)[:4]
        unit = ' M'
    else:
        snum = 'ERR'

    if snum[-1] == '.':
        snum = snum[:-1]
    snum = ' ' * (4 - len(snum)) + snum
    return snum + unit


def rmunit(s):
    if s[-1].isdecimal():
        return float(s)
    elif s[-1] == 'K' or s[-1] == 'k':
        return float(s[:-1]) * 1000
    elif s[-1] == 'M' or s[-1] == 'm':
        return float(s[:-1]) * 1000000
    elif s[-1] == 'G' or s[-1] == 'g':
        return float(s[:-1]) * 1000000000
    else:
        raise Exception(f'Undefined unit in "{s}".')


def isIPv4(s):
    if len(s) < 7 or 15 < len(s):
        return False
    blocks = s.split('.')
    if len(blocks) != 4:
        return False
    for block in blocks:
        if not block.isdigit():
            return False
        if len(block) > 3:
            return False
    return True


def gethours(dirpath='./ulgs'):
    hours = listdir(dirpath)
    hours = list(map(lambda x: x[:13], hours))
    hours = sorted(hours)
    return hours
