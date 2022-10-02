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

const readUserLogins = () => readdir('./ulgs')
  .then((files) => readFile(`./ulgs/${files.at(-1)}`, 'utf-8'))
  .then((content) => content.slice(0, -1).split('\n'));

module.exports = {
  getTS, readUserLogins, url2hostname, writeData,
};
