const KAPI = require('./utils/API');
const { writeData, getTS } = require('./utils/utils');

const getSpecificStreams = async () => {
  const strmPath = `./strm/${getTS().replaceAll(':', '.')}.json.txt`;
  const userLogins = new Set();
  const watchlist = ['hychouTwitch'];

  await KAPI.reqSpecificStreams(watchlist)
    .then((res) => res.data)
    .then(async (data) => {
      await writeData(strmPath, `${JSON.stringify(data)}\n`);
      data.data.forEach((stream) => userLogins.add(stream.user_login));
    })
    .catch(async (err) => {
      await writeData(
        `./errs/${getTS().slice(0, 13)}.tsv`,
        `${getTS()}\t@getSpecificStreams\t${err.message}\n`,
      );
    });

  return userLogins;
};

const updateSpecificStreams = async () => {
  const ulgsPath = `./ulgs/${getTS().replaceAll(':', '.')}.txt`;
  const userLogins = Array.from(await getSpecificStreams());
  const content = `${userLogins.join('\n')}\n`;

  await writeData(ulgsPath, content);
};

if (require.main === module) {
  updateSpecificStreams();
}
