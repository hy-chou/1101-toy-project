const cron = require("node-cron");
const process = require("process");
const { getTopIP } = require("./getTopIP.js");

cron.schedule("* 40-59 2 * * *", () => getTopIP(1000));
cron.schedule("0    10 3 * * *", () => process.exit());
