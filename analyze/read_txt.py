from datetime import datetime


def read_top():
    with open('./txts/top.txt') as f:
        lines = f.readlines()
    return lines

def read_iftop():
    with open('./txts/iftop.txt') as f:
        lines = f.readlines()
    return lines

def read_date():
    with open('./txts/date.txt') as f:
        lines = f.readlines()
    ts = []
    for line in lines:
        ts.append(datetime.fromisoformat(line[:-1]))
    return ts
