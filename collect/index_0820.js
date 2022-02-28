const cron = require("node-cron");
const process = require("process");
const { getTopIP } = require("./getTopIP.js");

cron.schedule("* 20-39 8 * * *", () => getTopIP(1000));
cron.schedule("0    50 8 * * *", () => process.exit());
