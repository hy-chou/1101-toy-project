const cron = require("node-cron");
const process = require("process");
const { getTopIP } = require("./getTopIP.js");

cron.schedule("* 00-19 10 * * *", () => getTopIP(1000));
cron.schedule("0    30 10 * * *", () => process.exit());
