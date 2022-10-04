const { readdir, readFile } = require('node:fs/promises');

const KAPI = require('./utils/API');
const { lookup, loadDNSCache } = require('./utils/dns');
const { writeData, getTS, url2hostname } = require('./utils/utils');

const getEdgeIPv4 = async (kache, userLogin) => {
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

const loadUserLogins = async () => {
  const file = await readdir('./ulgs')
    .then((files) => files.at(-1))
    .catch(() => []);

  return readFile(`./ulgs/${file}`, 'utf-8')
    .then((content) => content.slice(0, -1).split('\n'));
};

const updateEdges = async () => {
  const kache = new Map(await loadDNSCache());
  const userLogins = await loadUserLogins();

  return Promise.all(userLogins.map((userLogin) => getEdgeIPv4(kache, userLogin)));
};

if (require.main === module) {
  updateEdges();
}
