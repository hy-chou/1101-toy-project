const fs = require("fs");
const path = require("path");
const cron = require("node-cron");
const process = require("process");
const { getEdgeAddr } = require("./getEdgeAddrLocal.js");


const handleError = async (err, location) => {
  const ts = new Date().toISOString();
  const lines = `${ts}\t${location}\t${err}\n`;

  fs.appendFileSync(path.join(process.cwd(), "error.err"), lines);
};

const waitAMinute = () => new Promise(resolve => setTimeout(resolve, 1000));

const calcDts = (ts1) => (new Date() - ts1) / 1000;

const readUserLogins = async (c) => {
  const ulgPath = path.join(process.cwd(), `ulg${c}.tsv`);
  const ts1 = new Date();

  while (!fs.existsSync(ulgPath)) {
    await waitAMinute();
    handleError(`g.${c} waited ${calcDts(ts1)} sec`, "@ readUserLogins()");

    if (calcDts(ts1) > 60) {
      handleError(`g.${c} stopped waiting`, "@ readUserLogins()");
      return [];
    }
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
    handleError(err, "@ writeEdge()");
  }
};

const getEdgeFromUserLogin = async (ulogin) => {
  const ts1 = new Date();

  await getEdgeAddr(ulogin)
  .then((addr) => writeEdge(ulogin, ts1, addr))
  .catch((error) => writeEdge(ulogin, ts1, error.message));
};

const collectEdgesOfGroup = async (c, burstMode=false) => {
  const ulogins = (await readUserLogins(c));

  if (burstMode) return Promise.all(ulogins.map(item => getEdgeFromUserLogin(item)))

  return ulogins.reduce(
    (preVal, _, i) => preVal.then(() => getEdgeFromUserLogin(ulogins[i])),
    Promise.resolve()
  )
};

const main = async (c1=1, cn=100, groupSize=100, burstMode=false) => {
  let cs = [c1];

  while (cs[cs.length - 1] + groupSize - 1 < cn) {
    cs.push(cs[cs.length - 1] + groupSize);
  }

  return Promise.all(cs.map(c => collectEdgesOfGroup(c, burstMode)));
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
