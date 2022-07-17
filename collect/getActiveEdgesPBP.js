const fs = require("fs");
const path = require("path");
const cron = require("node-cron");
const process = require("process");
const { getEdgeAddr } = require("./getEdgeAddrLocal.js");
// const { getUserLogins } = require("./getActiveStreams.js");


const handleError = async (err, location) => {
  const ts = new Date().toISOString();
  const lines = `${ts}\t${location}\t${err}\n`;

  fs.appendFileSync(path.join(process.cwd(), "error.err"), lines);
};

const waitAMinute = () => new Promise(resolve => setTimeout(resolve, 1000));

const calcDts = (ts1) => (new Date() - ts1) / 1000;

const readUserLogins = async (p) => {
  const ulgPath = path.join(process.cwd(), `p${p}.ulg.tsv`);
  const ts1 = new Date();

  while (!fs.existsSync(ulgPath)) {
    await waitAMinute();
    handleError(`p.${p} waited ${calcDts(ts1)} sec`, "@ readUserLogins()");

    if (calcDts(ts1) > 60) {
      handleError(`page ${p} stopped waiting`, "@ readUserLogins()");
      return [];
    }
    // if (calcDts(ts1) > Math.max(10, p * 0.3)) {
    //   handleError(`self getUserLogins(${p}) after ${calcDts(ts1)} sec`,"@ readUserLogins()");
    //   await getUserLogins(p);
    //   handleError(`p.${p} waited ${calcDts(ts1)} sec`, "@ readUserLogins()");
    // }
  }

  let lines = fs.readFileSync(ulgPath, "utf8").split("\n");

  return lines[lines.length - 2].split("\t");
};

const writeEdge = async (channel, ts1, addr) => {
  const dts = (new Date() - ts1)/1000;
  const ts2H = ts1.toISOString().slice(0, 13);
  const lines = ts1.toISOString() + "\t" + addr + "\t" + dts + "\n";
  const tsvPath = path.join(process.cwd(), `${ts2H}${channel}.tsv`);

  try {
    fs.appendFileSync(tsvPath, lines);
  } catch (err) {
    handleError(err, "@writeEdge");
  }
};

const getEdgeFromUserLogin = async (channel) => {
  const ts1 = new Date();

  await getEdgeAddr(channel)
  .then((addr) => writeEdge(channel, ts1, addr))
  .catch((error) => writeEdge(channel, ts1, error.message));
};

const collectEdgesOnPage = async (p, burstMode=false) => {
  const channels = (await readUserLogins(p));

  if (burstMode) return Promise.all(channels.map(channel => getEdgeFromUserLogin(channel)))

  return channels.reduce(
    (p, _, i) => p.then(() => getEdgeFromUserLogin(channels[i])),
    Promise.resolve()
  )
};

const main = async (p1=1, pn=p1, burstMode=false) => {
  let ps = [p1];

  while (ps[ps.length - 1] < pn) ps.push(ps[ps.length - 1] + 1);

  return Promise.all(ps.map(p => collectEdgesOnPage(p, burstMode)));
};

if (require.main === module) {
  const pargv = process.argv;
  const stopProcess = () => process.kill(process.pid, 'SIGTERM');

  switch (pargv.length) {
    case 2:
      main()
      .then(stopProcess);
      break;
    case 4:
      main(Number(pargv[2]), Number(pargv[3]))
      .then(stopProcess);
      break;
    case 6:
      cron.schedule(pargv[4], () => main(Number(pargv[2]), Number(pargv[3])));
      cron.schedule(pargv[5], stopProcess);
      break;
    default:
      console.log("Error:  wrong argv")
      stopProcess();
  }
}
