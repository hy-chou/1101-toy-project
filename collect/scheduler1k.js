const cron = require("node-cron");
const process = require("process");
const { getSomeIP } = require("./getSomeIP.js");

cron.schedule(process.argv[2], () => {
  getSomeIP(0001, 1000);
});

cron.schedule(process.argv[3], () => process.exit());
