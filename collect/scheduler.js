const cron = require("node-cron");
const process = require("process");
const { getSomeIP } = require("./getSomeIP.js");


cron.schedule(process.argv[4], () =>{
  let p = Number(process.argv[2]);
  const q = Number(process.argv[3]);
  let pqarray = [];

  while (p + 99 < q) {
    pqarray.push([p, p + 99]);
    p += 100;
  }
  pqarray.push([p, q]);

  pqarray.map((pq) => {
    getSomeIP(pq[0], pq[1]);
  });
});

// cron.schedule(process.argv[5], () => process.exit());
cron.schedule(process.argv[5], () => process.kill(process.pid, 'SIGTERM'));
