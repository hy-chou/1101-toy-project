const fs = require("fs");
const path = require("path");
const cron = require("node-cron");
const process = require("process");
const { getEdgeAddr } = require("./getEdgeAddrLocal.js");

const handleDelay = async () => new Promise((resolve) => setTimeout(resolve, 1000));

const handleError = async (err, location) => {
  const ts = new Date().toISOString();
  const lines = ts + "\t" + location + "\t" + err + "\n";

  fs.appendFileSync(path.join(process.cwd(), "error.err"), lines);
}

const readUserLogins = async (p) => {
  let lines = "";
  let channels = [];
  const filename = `ulogins${p}.tsv`;
  const filepath = path.join(process.cwd(), filename);

  const ts1 = new Date();
  while (!fs.existsSync(filepath)) {
    await handleDelay();
    handleError(`page ${p} waited for ${(new Date() - ts1)/1000} sec`, "@readUserLogins");
    if ((new Date() - ts1) > 60000) {
      handleError(`page ${p} stopped waiting after a minute`, "@readUserLogins");
      return channels;
    }
  }

  lines = fs.readFileSync(filepath, "utf8");
  lines = lines.split("\n");
  channels = lines[lines.length - 2].split("\t");

  return channels;
}

const writeEdge = async (channel, ts1, addr) => {
  const dts = (new Date() - ts1)/1000;
  const ts2H = ts1.toISOString().substring(0, 13);
  const lines = ts1.toISOString() + "\t" + addr + "\t" + dts + "\n";

  const fileName = ts2H + channel + ".tsv";
  const filePath = path.join(process.cwd(), fileName);

  try {
    fs.appendFileSync(filePath, lines);
  } catch (err) {
    handleError(err, "@writeEdge");
  }
}

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
}

const main = async (p1=1, pn=1, burstMode=false) => {
  let p = p1;
  let ps = [p1];

  while (ps[ps.length - 1] < pn) ps.push(++p);

  Promise.all(ps.map(p => collectEdgesOnPage(p, burstMode)))
  // .then(() => process.kill(process.pid, 'SIGTERM'))
}

if (require.main === module) {
  if (process.argv.length === 2) {
    main();
  } else if (process.argv.length === 4) {
    main(Number(process.argv[2]), Number(process.argv[3]));
  } else if (process.argv.length === 6) {
    cron.schedule(process.argv[4], () => {
      main(Number(process.argv[2]), Number(process.argv[3]));
    });
    cron.schedule(process.argv[5], () => process.kill(process.pid, 'SIGTERM'));
  }
}
