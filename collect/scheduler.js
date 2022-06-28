const cron = require("node-cron");
const process = require("process");
const { getSomeIP } = require("./getSomeIP.js");

cron.schedule(process.argv[4], () =>{
  let p = Number(process.argv[2]);
  const q = Number(process.argv[3]);

  while (p <= q) {
    if (p + 100 < q)
      getSomeIP(p, p + 99);
    else
      getSomeIP(p, q);
    p += 100;
  }
});
cron.schedule(process.argv[5], () => process.exit());
