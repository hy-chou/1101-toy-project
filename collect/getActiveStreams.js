const cron = require('node-cron');
const process = require('node:process');
const KAPI = require('./KAPI');
const { append, handleError } = require('./kutils');

const getAPageOfStreams = async (cursor = '') => {
  let data;
  try {
    data = await KAPI.axiosGetStreams(cursor).then((res) => res.data);
  } catch (err) {
    handleError(err, '@ getAPageOfStreams()');
    return err;
  }

  const ts = new Date().toISOString();
  const ts2H = ts.slice(0, 13);
  const rawPath = `raws/${ts2H}raw.json.tsv`;
  const lines = `${ts}\t${JSON.stringify(data)}\n`;

  await append(rawPath, lines);
  return data;
};

const writeUserLogins = async (c, ulogins) => {
  const ts = new Date().toISOString();
  const ts2H = ts.slice(0, 13);
  const ulgPath = `ulgs/${ts2H}/${ts2H}ulg${c}.tsv`;

  let lines = ulogins.reduce((previousValue, currentValue) => {
    const line = `${previousValue + currentValue}\t`;
    return line;
  }, `${ts}\n`);
  lines = `${lines.slice(0, -1)}\n`;

  return append(ulgPath, lines);
};

const getUserLogins = async (c1 = 1, cn = 100, groupSize = 100) => {
  let cSliced = 0;
  let data = await getAPageOfStreams();
  let grandList = data.data.map((item) => item.user_login);
  const writingList = [];

  while (grandList.length < c1) {
    data = await getAPageOfStreams(data.pagination.cursor);
    grandList = grandList.concat(data.data.map((item) => item.user_login));
  }

  grandList = grandList.slice(c1 - 1);
  cSliced += c1 - 1;

  while (cSliced < cn) {
    while (grandList.length < groupSize) {
      data = await getAPageOfStreams(data.pagination.cursor);
      grandList = grandList.concat(data.data.map((item) => item.user_login));
    }
    writingList.push(
      writeUserLogins(
        cSliced + 1,
        grandList.slice(0, Math.min(groupSize, cn - cSliced)),
      ),
    );
    grandList = grandList.slice(groupSize);
    cSliced += groupSize;
  }

  return Promise.all(writingList)
    .catch((err) => handleError(err, '@ getUserLogins()'))
    .finally(() => process.kill(process.pid, 'SIGTERM'));
};

if (require.main === module) {
  const pargv = process.argv;

  switch (pargv.length) {
    case 2:
      getUserLogins();
      break;
    case 4:
      getUserLogins(Number(pargv[2]), Number(pargv[3]));
      break;
    case 5:
      cron.schedule(pargv[4], () => getUserLogins(Number(pargv[2]), Number(pargv[3])));
      break;
    default:
      // console.error('Error:  wrong argv');
      process.kill(process.pid, 'SIGTERM');
  }
}
