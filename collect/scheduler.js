const cron = require("node-cron");
const process = require("process");
const { getSomeIP } = require("./getSomeIP.js");

cron.schedule(process.argv[4], () =>
  getSomeIP(process.argv[2], process.argv[3])
);
cron.schedule(process.argv[5], () => process.exit());
