const cron = require('node-cron');
const process = require('node:process');
const KAPI = require('./KAPI');
const { handleError, append } = require('./kutils');

const logStreams = async (ts, rtt, headers, data, pageCount) => {
  const promises = [];
  const ts2H = ts.slice(0, 13);
  const tsR = ts.replaceAll(':', '.');
  const lines = data.data.reduce(
    (preVal, val) => `${preVal}${val.user_login}\t`,
    `${ts}\n`,
  );

  promises.push(append(`./rtts/uS/${ts2H}.txt`, `${ts}\t${rtt}\n`));
  // eslint-disable-next-line no-restricted-syntax
  for (const [key, value] of Object.entries(headers)) {
    promises.push(append(`./hdrs/${ts2H}/${key}.txt`, `${ts}\t${value}\n`));
  }
  promises.push(append(`./data/${ts2H}/${tsR}.json`, JSON.stringify(data)));
  promises.push(append(`./ulgs/${ts2H}/p${pageCount}.tsv`, `${lines.slice(0, -1)}\n`));

  return Promise.all(promises)
    .catch((err) => handleError(err, `@ logStreams(${pageCount})`));
};

const updateStreams = async (numPage = 1, cursor = '', pageCount = 1) => {
  if (numPage === 0) { return; }

  const t0 = new Date();

  await KAPI.axiosGetStreams(cursor)
    .then(async (res) => {
      const rtt = (new Date() - t0) / 1000;
      const { headers, data } = res;
      const newCursor = res.data.pagination.cursor;

      await Promise.all([
        logStreams(t0.toISOString(), rtt, headers, data, pageCount),
        updateStreams(numPage - 1, newCursor, pageCount + 1),
      ]);
    })
    .catch((err) => {
      handleError(err, `@ updateStreams(${numPage})`);
      return updateStreams(numPage - 1, cursor, pageCount + 1);
    })
    .finally(() => process.kill(process.pid, 'SIGTERM'));
};

if (require.main === module) {
  const pargv = process.argv;

  if (pargv.length === 2) {
    updateStreams(1);
  } else if (pargv.length === 4) {
    const numPage = Math.ceil(Number(pargv[3]) / 100);

    updateStreams(numPage);
  } else if (pargv.length === 5) {
    const numPage = Math.ceil(Number(pargv[3]) / 100);

    cron.schedule(pargv[4], () => updateStreams(numPage));
  } else {
    process.kill(process.pid, 'SIGTERM');
  }
}
