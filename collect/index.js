const cron = require("node-cron");
const process = require("process");
const { getTopIP } = require("./getTopIP.js");

cron.schedule("* 12 * * * *", () => getTopIP(10));
cron.schedule("0 13 * * * *", () => process.exit());
