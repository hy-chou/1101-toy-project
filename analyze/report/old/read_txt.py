from datetime import datetime


def read_top():
    lines = []
    try:
        with open('./txts/top.txt') as f:
            lines = f.readlines()
    finally:
        return lines

def read_iftop():
    lines = []
    try:
        with open('./txts/iftop.txt') as f:
            lines = f.readlines()
    finally:
        return lines

def read_date():
    with open('./txts/date.txt') as f:
        lines = f.readlines()
    ts = []
    for line in lines:
        ts.append(datetime.fromisoformat(line[:-1]))
    return ts
