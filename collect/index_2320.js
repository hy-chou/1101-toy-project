const cron = require("node-cron");
const process = require("process");
const { getTopIP } = require("./getTopIP.js");

cron.schedule("* 20-39 23 * * *", () => getTopIP(1000));
cron.schedule("0    50 23 * * *", () => process.exit());
