const cron = require("node-cron");
const process = require("process");
const { getTopIP } = require("./getTopIP.js");

cron.schedule("* 20-39 11 * * *", () => getTopIP(1000));
cron.schedule("0    50 11 * * *", () => process.exit());
