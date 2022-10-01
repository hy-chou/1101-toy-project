const { readFile } = require('node:fs/promises');
const { getPATRecord, getDNSRecord } = require('./Kache');
const KAPI = require('./KAPI');
const {
  listDir, append, handleError, url2hostname, m3u82url,
} = require('./kutils');

const writeIPv4 = async (channel, ipv4) => {
  const ts = new Date().toISOString();
  const ts2m = ts.slice(0, 16).replace(':', '.');
  const lines = `${ts}\t${ipv4}\t${channel}\n`;

  return append(`ipv4/${ts2m}.tsv`, lines);
};

const getUsherM3U8 = async (channel, sPAToken) => {
  const res = await KAPI.reqUsherM3U8(sPAToken, channel)
    .catch(async (err) => {
      if (err.response.status === 404) {
        await handleError(err.response.data[0].error, `404 @getUsherM3U8(${channel})`);
        throw new Error('handled');
      }
      await handleError(err.message, `mes @getUsherM3U8(${channel})`);
      await handleError(err.response, `res @getUsherM3U8(${channel})`);
      await handleError(err.request, `req @getUsherM3U8(${channel})`);
      await handleError(err.config, `con @getUsherM3U8(${channel})`);
      throw err;
    });
  return res.data;
};

const getWeaverM3U8 = async (channel, weaver0) => {
  const res = await KAPI.axiosGet(weaver0)
    .catch((err) => {
      handleError(err, `@getWeaverM3U8(${channel})`);
      throw err;
    });
  return res.data;
};

const getChannelIPv4 = async (channel) => {
  const ipv4 = await getPATRecord(channel)
    .then((sPAToken) => getUsherM3U8(channel, sPAToken))
    .then((usherm3u8) => m3u82url(usherm3u8))
    .then((weaverlist) => getWeaverM3U8(channel, weaverlist[0]))
    .then((weaverm3u8) => m3u82url(weaverm3u8))
    .then((edgelist) => url2hostname(edgelist[0]))
    .then((edgehostname0) => getDNSRecord(edgehostname0))
    .then((record) => {
      writeIPv4(channel, record);
      return record;
    })
    .catch((err) => {
      if (err.message !== 'handled') { handleError(err, `@getChannelIPv4(${channel})`); }
    });

  return ipv4;
};

const updatePage = async (path) => {
  const ulogins = (await readFile(path, 'utf8')).split('\n').at(-2).split('\t');
  const promises = [];

  ulogins.forEach((ulogin) => { promises.push(getChannelIPv4(ulogin)); });

  return Promise.all(promises)
    .catch((err) => handleError(err, '@updatePage'));
};

const updateEgdes = async () => {
  const promises = [];
  const lastTS = await listDir('./ulgs')
    .then((ts) => ts.at(-1))
    .catch((err) => {
      if (err.message !== 'handled') { handleError(err, '@updateEdges()'); }
    });

  if (lastTS) {
    await listDir(`./ulgs/${lastTS}`)
      .then((pages) => pages.forEach((page) => {
        promises.push(updatePage(`./ulgs/${lastTS}/${page}`));
      }))
      .catch((err) => {
        if (err.message !== 'handled') { handleError(err, '@updateEdges()'); }
      });
  }

  return Promise.all(promises)
    .catch((err) => handleError(err, '@updateEdges'))
    .finally(() => process.kill(process.pid, 'SIGTERM'));
};

if (require.main === module) {
  updateEgdes();
}
