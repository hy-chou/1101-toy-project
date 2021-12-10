import os


def getGnuplotScript(file, outPath):
    line = "'{}' using 2 w l,\n".format(file)
    with open(outPath, 'a', encoding='utf-8') as outFile:
        outFile.write(line)

# def getP(num):
#     line = "'try21/5T18_auronplay.2cdf' using {} w l, ".format(num)
#     pPath = 'plot3598.p'
#     with open(pPath, 'a', encoding='utf-8') as plotF:
#         plotF.write(line)


outPath = './plot_CDF_6T1.gnuplot'
for file in os.listdir('./try21/cdfs/'):
    if file.startswith('6T1'):
        getGnuplotScript(file, outPath)

# list = ['auronplay', 'gaules', 'valorant', 'baiano',
#         'esl_csgo', 'montanablack88', 'dota2ruhub', 'thegrefg']
# for channel in list:
#     getP("5T18_{}.cdf".format(channel))

# for i in range(3598):
#     getP(i + 1)
