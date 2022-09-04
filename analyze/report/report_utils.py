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


def rmunit(snum='-1'):
    snum = snum.strip()
    if snum[-1].isdecimal():
        num = float(snum)
    elif snum[-1] == 'K' or snum[-1] == 'k':
        num = float(snum[:-1]) * 1000
    elif snum[-1] == 'M' or snum[-1] == 'm':
        num = float(snum[:-1]) * 1000000
    elif snum[-1] == 'G' or snum[-1] == 'g':
        num = float(snum[:-1]) * 1000000000
    else:
        raise Exception(f'Undefined unit in "{snum}".')
    return num


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
