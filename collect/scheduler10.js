const cron = require("node-cron");
const process = require("process");
const { getSomeIP } = require("./getSomeIP.js");

cron.schedule(process.argv[2], () => {
  getSomeIP(1, 10);
  // let i = 1;
  // while (i <= 10){
  //   getSomeIP(i, i);
  //   i++;
  // }
});

cron.schedule(process.argv[3], () => process.exit());
