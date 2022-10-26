const { readdir, readFile } = require('node:fs/promises');

const KAPI = require('./utils/API');
const { getTS, writeData } = require('./utils/utils');

const getPAT = (userLogin) => KAPI.reqPlaybackAccessToken(userLogin)
  .then((res) => res.data.data.streamPlaybackAccessToken)
  .catch((err) => err.message);

const loadUserLogins = async () => {
  const file = await readdir('./ulgs')
    .then((files) => files.at(-1))
    .catch(() => []);

  return readFile(`./ulgs/${file}`, 'utf-8')
    .then((content) => content.slice(0, -1).split('\n'));
};

const getPATs = async () => {
  const patsPath = `./pats/${getTS().replaceAll(':', '.')}.tsv`;

  await loadUserLogins()
  // bursty
    .then((userLogins) => userLogins.forEach(async (userLogin) => {
      const ts = getTS();
      const sPAT = await getPAT(userLogin);

      writeData(
        patsPath,
        `${ts}\t${JSON.stringify(sPAT)}\t${userLogin}\n`,
      );
    }));
  // // single queue
  //   .then((userLogins) => userLogins.reduce(
  //     (lastPromise, userLogin) => lastPromise.then(async () => {
  //       writeData(
  //         edgsPath,
  //         `${getTS()}\t${await getVideoEdgeHostname(userLogin)}\t${userLogin}\n`,
  //       );
  //     }),
  //     Promise.resolve(),
  //   ));
};

if (require.main === module) {
  getPATs();
}
