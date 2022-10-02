const dns = require('node:dns');
const { readDNSCache, writeData, getTS } = require('./utils');

const init = async () => new Map(await readDNSCache());

const lookup = async (kache, hostname) => {
  if (kache.has(hostname)) return kache.get(hostname);

  const ts = getTS();
  const ts2M = ts.slice(0, 7);
  const ipv4 = await dns.promises.lookup(hostname)
    .then((result) => result.address);

  await writeData(`../cache/${ts2M}/${hostname}.tsv`, `${ts}\t${ipv4}\n`);
  kache.set(hostname, ipv4);
  return ipv4;
};

module.exports = { init, lookup };
