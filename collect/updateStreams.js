const KAPI = require('./KAPI');
const { handleError, append } = require('./kutils');

const getStreams = async (cursor, p) => {
  const res = await KAPI.reqStreams(cursor)
    .catch(async (err) => {
      await handleError(err, `@getStreams(${p})`);
      throw new Error('handled');
    });

  return res.data;
};

const logStreams = async (ts, data, p) => {
  const lines = data.data.reduce(
    (preVal, val) => `${preVal}${val.user_login}\t`,
    `${ts}\n`,
  );
  return append(`./ulgs/${ts.slice(0, 16)}/p${p}.tsv`, `${lines.slice(0, -1)}\n`);
};

const updateStreams = async (numPage = 1) => {
  const t0 = (new Date()).toISOString().replaceAll(':', '.');
  const cursor = [''];

  for (let p = 0; p < numPage; p += 1) {
    // eslint-disable-next-line no-await-in-loop
    await getStreams(cursor[p], p)
      .then(async (data) => {
        cursor.push(data.pagination.cursor);
        await logStreams(t0, data, p);
      });
  }
};

if (require.main === module) {
  const pargv = process.argv;

  if (pargv.length === 2) {
    updateStreams(1);
  } else if (pargv.length === 3) {
    const numPage = Math.ceil(Number(pargv[2]) / 100);

    updateStreams(numPage);
  } else {
    process.kill(process.pid, 'SIGTERM');
  }
}
