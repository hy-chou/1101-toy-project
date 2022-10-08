const KAPI = require('./utils/API');
const { writeData, getTS } = require('./utils/utils');

const getStreams = async (endPage = 1) => {
  const cursor = [''];
  const userLogins = new Set();

  for (let p = 0; p < endPage; p += 1) {
    // eslint-disable-next-line no-await-in-loop
    await KAPI.reqStreams(cursor[0])
      .then((res) => res.data)
      .then((data) => {
        data.data.forEach((stream) => userLogins.add(stream.user_login));
        cursor.pop();
        cursor.push(data.pagination.cursor);
      })
      .catch((err) => {
        const ts = getTS();
        const ts2H = ts.slice(0, 13);

        writeData(
          `./errs/${ts2H}.tsv`,
          `${ts}\t@getStreams p${p}\t${err.message}\n`,
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
