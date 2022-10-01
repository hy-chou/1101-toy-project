const dns = require('node:dns');
const { readFile } = require('node:fs/promises');

const { append, handleError } = require('./kutils');

const dnsCache = {};

const disk2memory = async () => {
  const ts2M = new Date().toISOString().slice(0, 7);
  const cachePath = `cache/dns/${ts2M}.tsv`;

  await readFile(cachePath, 'utf8')
    .then((content) => content.split('\n'))
    .then((lines) => lines.forEach((line) => {
      const { hostname, record } = line.split('\t');

      dnsCache[hostname] = record;
    }))
    .catch((err) => {
      if (err.code !== 'ENOENT') { handleError(err.message, '@disk2memory()'); }
    });
};

const writeDNSCache = async (hostname, ipv4) => {
  const ts2M = new Date().toISOString().slice(0, 7);
  const lines = `${hostname}\t${ipv4}\n`;

  return append(`./cache/dns/${ts2M}.tsv`, lines);
};

const getDNSRecord = async (hostname) => {
  if (dnsCache[hostname]) { return dnsCache[hostname]; }

  const ipv4 = await dns.promises.lookup(hostname)
    .then((result) => result.address);

  dnsCache[hostname] = ipv4;
  await writeDNSCache(hostname, ipv4);
  return ipv4;
};

module.exports = { getDNSRecord, disk2memory };
