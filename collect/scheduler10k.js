const cron = require("node-cron");
const process = require("process");
const { getSomeIP } = require("./getSomeIP.js");

cron.schedule(process.argv[2], () => {
  getSomeIP(0001, 1000);
  getSomeIP(1001, 2000);
  getSomeIP(2001, 3000);
  getSomeIP(3001, 4000);
  getSomeIP(4001, 5000);
  getSomeIP(5001, 6000);
  getSomeIP(6001, 7000);
  getSomeIP(7001, 8000);
  getSomeIP(8001, 9000);
  getSomeIP(9001, 10000);
});

cron.schedule(process.argv[3], () => process.exit());
