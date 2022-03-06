const cron = require("node-cron");
const process = require("process");
const { getMidIP } = require("./getMidIP.js");

cron.schedule(process.argv[2], () => getMidIP(1001, 2000));
cron.schedule(process.argv[3], () => process.exit());
