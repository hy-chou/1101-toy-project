import os
import sys


def getGnuplotScript(filename, plotFile):
    line = "'{}' w l,\n".format(filename)
    with open(plotFile, 'a', encoding='utf-8') as oF:
        oF.write(line)


plotFile = './plot_CDF_{}.gnuplot'.format(sys.argv[1])
for file in os.listdir():
    if file.startswith(sys.argv[1]):
        getGnuplotScript(file, plotFile)
