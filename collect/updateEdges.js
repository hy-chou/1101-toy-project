const { readFile } = require('node:fs/promises');
const { getPATRecord } = require('./patCache');
const { disk2memory, getDNSRecord } = require('./dnsCache');
const KAPI = require('./KAPI');
const {
  listDir, append, handleError, url2hostname, m3u82url, writeIPv4,
} = require('./kutils');

const getUsherM3U8 = async (channel, sPAToken) => {
  const res = await KAPI.reqUsherM3U8(sPAToken, channel)
    .catch(async (err) => {
      if (err.response.data[0].error === 'twirp error not_found: transcode does not exist') {
        await writeIPv4(channel, '#404');
        throw new Error('handled');
      }
      console.log(err);
      await handleError(err.message, `@getUsherM3U8(${channel})`);
      throw new Error('handled');
    });
  return res.data;
};

const getWeaverM3U8 = async (channel, weaver0) => {
  const res = await KAPI.axiosGet(weaver0)
    .catch(async (err) => {
      await handleError(err.message, `@getWeaverM3U8(${channel})`);
      throw new Error('handled');
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
  const ulogins = (await readFile(path, 'utf8')).split('\n')[1].split('\t');
  const promises = [];

  ulogins.forEach((ulogin) => { promises.push(getChannelIPv4(ulogin)); });

  return Promise.all(promises)
    .catch((err) => handleError(err, '@updatePage'));
};

const updateEgdes = async () => {
  await disk2memory();

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
