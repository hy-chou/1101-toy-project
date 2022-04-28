const cron = require("node-cron");
const process = require("process");
const { getSomeIP } = require("./getSomeIP.js");

cron.schedule(process.argv[2], () => {
  getSomeIP(10001, 11000);
  getSomeIP(11001, 12000);
  getSomeIP(12001, 13000);
  getSomeIP(13001, 14000);
  getSomeIP(14001, 15000);
  getSomeIP(15001, 16000);
  getSomeIP(16001, 17000);
  getSomeIP(17001, 18000);
  getSomeIP(18001, 19000);
  getSomeIP(19001, 20000);
});

cron.schedule(process.argv[3], () => process.exit());
