const KAPI = require('./utils/API');
const { writeData, getTS } = require('./utils/utils');

const getStreams = async (endPage = 1) => {
  const strmPath = `./strm/${getTS().replaceAll(':', '.')}.json.txt`;
  const cursor = [''];
  const userLogins = new Set();
  let p = 0;
  let lastSize = -1;
  let lastLastSize = -1;

  while (p < endPage && userLogins.size !== lastLastSize) {
    p += 1;
    lastLastSize = lastSize;
    lastSize = userLogins.size;

    // eslint-disable-next-line no-await-in-loop
    await KAPI.reqStreams(cursor[0])
      .then((res) => res.data)
      .then(async (data) => {
        await writeData(strmPath, `${JSON.stringify(data)}\n`);
        data.data.forEach((stream) => userLogins.add(stream.user_login));
        cursor.pop();
        cursor.push(data.pagination.cursor);
      })
      .catch(async (err) => {
        await writeData(
          `./errs/${getTS().slice(0, 13)}.tsv`,
          `${getTS()}\t@getStreams\t${err.message}\n`,
        );
      });
  }

  return userLogins;
};

const updateStreams = async (endPage = 1) => {
  const ulgsPath = `./ulgs/${getTS().replaceAll(':', '.')}.txt`;
  const userLogins = Array.from(await getStreams(endPage));
  const content = `${userLogins.join('\n')}\n`;

  await writeData(ulgsPath, content);
};

if (require.main === module) {
  const pargv = process.argv;

  if (pargv.length === 2) {
    updateStreams(1);
  } else if (pargv.length === 3) {
    const endPage = Math.ceil(Number(pargv[2]) / 100);

    updateStreams(endPage);
  }
}
