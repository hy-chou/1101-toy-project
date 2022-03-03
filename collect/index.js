const cron = require("node-cron");
const process = require("process");
const { getTopIP } = require("./getTopIP.js");

cron.schedule(process.argv[2], () => getTopIP(1000));
cron.schedule(process.argv[3], () => process.exit());
