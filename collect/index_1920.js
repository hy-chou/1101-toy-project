const cron = require("node-cron");
const process = require("process");
const { getTopIP } = require("./getTopIP.js");

cron.schedule("* 20-39 19 * * *", () => getTopIP(1000));
cron.schedule("0    50 19 * * *", () => process.exit());
