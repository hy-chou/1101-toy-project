def index_n_js():
    a = [' 00-19 ', ' 20-39 ', ' 40-59 ']
    b = [' 30 ', ' 50 ', ' 10 ']

    for h in range(10, 24):
        for i in [2]:
            content = """const cron = require("node-cron");
const process = require("process");
const { getTopIP } = require("./getTopIP.js");

cron.schedule("*""" + a[i] + str(h) + """ * * *", () => getTopIP(1000));
cron.schedule("0   """ + b[i] + str(h+1) + """ * * *", () => process.exit());
"""
            filename = 'index_{}40.js'.format(h)
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)


index_n_js()
