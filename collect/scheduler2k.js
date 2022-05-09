const cron = require("node-cron");
const process = require("process");
const { getSomeIP } = require("./getSomeIP.js");

cron.schedule(process.argv[2], () => {
  getSomeIP(   1, 1000);
  getSomeIP(1001, 2000);
});

cron.schedule(process.argv[3], () => process.exit());
