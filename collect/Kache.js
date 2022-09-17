const dns = require('node:dns');
const { readFile } = require('node:fs/promises');

const KAPI = require('./KAPI');
const { append } = require('./kutils');

const readDNSCache = async (hostname) => {
  const ts2M = new Date().toISOString().slice(0, 7);
  const cachePath = `cache/dns/${ts2M}/${hostname}.tsv`;

  const lines = await readFile(cachePath, 'utf8');

  return lines.split('\n').at(-2).split('\t').at(-1);
};

const writeDNSCache = async (hostname, record) => {
  const ts = new Date().toISOString();
  const ts2M = ts.slice(0, 7);
  const cachePath = `cache/dns/${ts2M}/${hostname}.tsv`;

  const lines = `${ts}\t${record}\n`;

  return append(cachePath, lines);
};

const getDNSRecord = async (hostname) => readDNSCache(hostname)
  .catch(async (err) => {
    const record = await dns.promises
      .lookup(hostname)
      .then((result) => result.address);

    if (err.code !== 'ENOENT') console.error(err);
    writeDNSCache(hostname, record);

    return record;
  });

const readPATCache = async (channel) => {
  const ts2M = new Date().toISOString().slice(0, 7);
  const cachePath = `cache/pat/${ts2M}/${channel}.tsv`;

  const lines = await readFile(cachePath, 'utf8');
  const record = JSON.parse(lines.split('\n').at(-2).split('\t').at(-1));

  return record;
};

const writePATCache = (channel, record) => {
  const ts = new Date().toISOString();
  const ts2M = ts.slice(0, 7);
  const cachePath = `cache/pat/${ts2M}/${channel}.tsv`;

  const lines = `${ts}\t${record}\n`;

  return append(cachePath, lines);
};

const getPATRecord = async (channel) => readPATCache(channel)
  .catch(async (err) => {
    const record = await KAPI.axiosPostPlaybackAccessToken(channel)
      .then((res) => res.data.data.streamPlaybackAccessToken);

    if (err.code !== 'ENOENT') console.error(err);
    writePATCache(channel, JSON.stringify(record));

    return record;
  });

module.exports = { getDNSRecord, getPATRecord };
