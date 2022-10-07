const dns = require('node:dns');
const { readdir, readFile } = require('node:fs/promises');

const { getTS } = require('./utils');

const loadDNSCache = async () => {
  const ts2M = getTS().slice(0, 7);
  const files = await readdir(`../cache/${ts2M}`).catch(() => []);

  return Promise.all(files.map(async (hostname) => {
    const content = await readFile(`../cache/${ts2M}/${hostname}`, 'utf-8');
    const ipv4 = content.split('\n')[0].split('\t')[1];

    return [hostname, ipv4];
  }));
};

const lookup = async (kache, hostname) => {
  if (kache.has(hostname)) {
    return kache.get(hostname);
  }

  const ipv4 = (await dns.promises.lookup(hostname)).address;

  kache.set(hostname, ipv4);
  return ipv4;
};

module.exports = { loadDNSCache, lookup };
