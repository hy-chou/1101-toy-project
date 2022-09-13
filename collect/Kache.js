const dns = require("node:dns");
const { dirname } = require("node:path");
const { mkdir, appendFile, readFile } = require("node:fs/promises");

const append = async (path, data) => {
  await mkdir(dirname(path), { recursive: true });
  return appendFile(path, data);
};

const getDNSRecord = async (hostname) => {
  return readDNSCache(hostname).catch(async (err) => {
    const record = await dns.promises
      .lookup(hostname)
      .then((result) => result.address);

    console.error(err);
    writeDNSCache(hostname, record);

    return record;
  });
};

const readDNSCache = async (hostname) => {
  const ts2M = new Date().toISOString().slice(0, 7);
  const cachePath = `cache/dns/${ts2M}/${hostname}.tsv`;

  const lines = await readFile(cachePath, "utf8");

  return lines.split("\n").at(-2).split("\t").at(-1);
};

const writeDNSCache = async (hostname, record) => {
  const ts = new Date().toISOString();
  const ts2M = ts.slice(0, 7);
  const cachePath = `cache/dns/${ts2M}/${hostname}.tsv`;

  const lines = ts + "\t" + record + "\n";

  return append(cachePath, lines);
};

module.exports = { getDNSRecord };
