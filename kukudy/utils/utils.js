const { dirname } = require('node:path');
const {
  appendFile, mkdir, readdir, readFile,
} = require('node:fs/promises');

const getTS = () => new Date().toISOString();

const url2hostname = (url) => {
  const p = url.indexOf('://') + 3;
  const q = url.indexOf('/', p);

  return url.slice(p, q);
};

const writeData = (path, data) => mkdir(dirname(path), { recursive: true })
  .then(() => appendFile(path, data));

const readDNSCache = async () => {
  const ts2M = getTS().slice(0, 7);
  const files = await readdir(`../cache/${ts2M}`);

  return Promise.all(files.map((file) => readFile(`../cache/${ts2M}/${file}`, 'utf-8')
    .then((content) => content.slice(0, -1).split('\n'))
    .then((lines) => lines.at(-1).split('\t')[1])
    .then((ipv4) => [file.slice(0, -4), ipv4])));
};

const readUserLogins = () => readdir('./ulgs')
  .then((files) => readFile(`./ulgs/${files.at(-1)}`, 'utf-8'))
  .then((content) => content.slice(0, -1).split('\n'));

module.exports = {
  getTS, readDNSCache, readUserLogins, url2hostname, writeData,
};
