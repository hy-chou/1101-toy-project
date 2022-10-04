const KAPI = require('./utils/API');
const { init, lookup } = require('./utils/dns');
const {
  writeData, getTS, readUserLogins, url2hostname,
} = require('./utils/utils');

let kache;

const getEdgeIPv4 = async (userLogin) => {
  const ipv4 = await KAPI.reqPlaybackAccessToken(userLogin)
    .then((res) => res.data.data.streamPlaybackAccessToken)
    .then((sPAToken) => KAPI.reqUsherM3U8(sPAToken, userLogin))
    .then((res) => res.data)
    .then((usherM3U8) => usherM3U8.split('\n').find((line) => line[0] !== '#'))
    .then((weaverURL) => KAPI.reqGet(weaverURL))
    .then((res) => res.data)
    .then((weaverM3U8) => weaverM3U8.split('\n').find((line) => line[0] !== '#'))
    .then((edgeURL) => url2hostname(edgeURL))
    .then((hostname) => lookup(kache, hostname))
    .catch((err) => {
      if (err.message === 'E404') { return 'E404'; }
      if (err.message === 'E403') { return 'E403'; }
      if (err.message === 'ECONNABORTED') { return 'ECONNABORTED'; }
      return err.message;
    });
  const ts = getTS();
  const ts2H = ts.slice(0, 13);

  return writeData(
    `./ipv4/${ts2H}.tsv`,
    `${ts}\t${ipv4}\t${userLogin}\n`,
  );
};

const updateEgdes = async () => {
  kache = await init();

  const userLogins = await readUserLogins()
    .catch((err) => {
      if (err.code === 'ENOENT') {
        const ts = getTS();
        const ts2H = ts.slice(0, 13);

        writeData(
          `./err/${ts2H}.txt`,
          `${ts}\t@updateEdges\t${err.message}\n`,
        );
      }
      return [];
    });

  return Promise.all(userLogins.map((userLogin) => getEdgeIPv4(userLogin)));
};

if (require.main === module) {
  updateEgdes();
}
