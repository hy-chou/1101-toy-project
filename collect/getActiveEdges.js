const cron = require('node-cron');
const process = require('node:process');
const { readFile } = require('node:fs/promises');

const { getEdgeAddr } = require('./getEdgeAddrLocal');
const { append, handleError, waitASecond } = require('./kutils');

const readUserLogins = async (c, ttl = 60) => {
  const ts2H = new Date().toISOString().slice(0, 13);
  const ulgPath = `ulgs/${ts2H}/${ts2H}ulg${c}.tsv`;
  let userLogins = [];

  try {
    let lines = await readFile(ulgPath, 'utf8');

    lines = lines.split('\n');
    userLogins = lines[lines.length - 2].split('\t');
  } catch (err) {
    if (ttl) {
      if (err.code !== 'ENOENT') handleError(err, '@ readUserLogins()');
      await waitASecond();
      userLogins = readUserLogins(c, ttl - 1);
    } else {
      await handleError(`g.${c} stopped waiting`, '@ readUserLogins()');
    }
  }

  return userLogins;
};

const writeEdge = async (channel, addr) => {
  const ts = new Date().toISOString();
  const ts2H = ts.slice(0, 13);
  const lines = `${ts}\t${addr}\n`;
  const tsvPath = `tsvs/${ts2H}/${channel}.tsv`;

  return append(tsvPath, lines);
};

const writeRTT = async (channel, dts) => {
  const ts = new Date().toISOString();
  const ts2H = ts.slice(0, 13);
  const lines = `${ts}\t${dts}\n`;
  const rttPath = `rtts/${ts2H}/${channel}.tsv`;

  return append(rttPath, lines);
};

const getEdgeFromUserLogin = async (ulogin) => {
  const tsPre = new Date();
  const edgeAddr = await getEdgeAddr(ulogin);

  return Promise.all([
    writeEdge(ulogin, edgeAddr),
    writeRTT(ulogin, (new Date() - tsPre) / 1000),
  ])
    .catch((error) => writeEdge(ulogin, tsPre, error.message));
};

const collectEdgesOfGroup = async (c, burstMode = false) => {
  const ulogins = await readUserLogins(c);

  if (burstMode) {
    return Promise.all(ulogins.map((item) => getEdgeFromUserLogin(item)));
  }

  return ulogins.reduce(
    (preVal, _, i) => preVal.then(() => getEdgeFromUserLogin(ulogins[i])),
    Promise.resolve(),
  );
};

const main = async (c1 = 1, cn = 100, groupSize = 100, burstMode = false) => {
  const cs = [c1];

  while (cs[cs.length - 1] + groupSize - 1 < cn) {
    cs.push(cs[cs.length - 1] + groupSize);
  }

  return Promise.all(cs.map((c) => collectEdgesOfGroup(c, burstMode)))
    .catch((error) => handleError(error, '@ gAE main()'))
    .finally(() => process.kill(process.pid, 'SIGTERM'));
};

if (require.main === module) {
  const pargv = process.argv;

  switch (pargv.length) {
    case 2:
      main();
      break;
    case 4:
      main(Number(pargv[2]), Number(pargv[3]));
      break;
    case 5:
      cron.schedule(pargv[4], () => main(Number(pargv[2]), Number(pargv[3])));
      break;
    default:
      // console.error('Error:  wrong argv');
      process.kill(process.pid, 'SIGTERM');
  }
}
