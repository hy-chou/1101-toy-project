const { dirname } = require('node:path');
const { appendFile, mkdir } = require('node:fs/promises');

const getTS = () => new Date().toISOString();

const url2hostname = (url) => {
  const p = url.indexOf('://') + 3;
  const q = url.indexOf('/', p);

  return url.slice(p, q);
};

const writeData = (path, data) => mkdir(dirname(path), { recursive: true })
  .then(() => appendFile(path, data));

module.exports = {
  getTS, url2hostname, writeData,
};
