import csv


def getCount2(file):
    rawPath = file
    cdfPath = file[:-4] + '.count2'

    with open(rawPath, 'r', encoding='utf-8') as rawF:
        csvReader = csv.reader(rawF)
        rows = list(csvReader)
        cdf2d = []
        for i in range(len(rows)):
            ip_set = set()
            cdf = []
            for j in range(i, len(rows)):
                if len(rows[j]) == 3 and rows[j][1][-1].isdigit():
                    ip_set.add(rows[j][1].strip())
                cdf.append(len(ip_set))
            cdf2d.append(cdf)

    with open(cdfPath, 'w', encoding='utf-8') as cdfF:
        l = len(cdf2d)
        for i in range(l):
            for j in range(l):
                if (len(cdf2d[i]) > j):
                    cdfF.write('{} '.format(cdf2d[j][i]))
            cdfF.write('\n')


# for file in os.listdir():
#     if file.endswith(".csv") and not file.endswith("top.csv"):
#         getCDF(file)
getCount2('./try21/csvs/5T22_esl_csgo.csv')
