const cron = require("node-cron");
const process = require("process");
const { getTopIP } = require("./getTopIP.js");

cron.schedule("* 40-59 20 * * *", () => getTopIP(1000));
cron.schedule("0    10 21 * * *", () => process.exit());
