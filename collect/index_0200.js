const cron = require("node-cron");
const process = require("process");
const { getTopIP } = require("./getTopIP.js");

cron.schedule("* 00-19 2 * * *", () => getTopIP(1000));
cron.schedule("0    30 2 * * *", () => process.exit());
