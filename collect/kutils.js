const { dirname } = require('node:path');
const { mkdir, appendFile, readdir } = require('node:fs/promises');

const append = async (path, data) => {
  await mkdir(dirname(path), { recursive: true });
  return appendFile(path, data);
};

const handleError = async (err, location) => {
  const ts = new Date().toISOString();
  const ts2H = ts.slice(0, 13);
  const errPath = `errs/${ts2H}error.tsv`;
  const lines = `${ts}\t${location}\t${err}\n`;

  console.error(lines);
  return append(errPath, lines);
};

const listDir = async (path) => {
  const files = await readdir(path)
    .catch(async (err) => {
      await handleError(err, '@listDir');
      throw new Error('handled');
    });
  files.sort();
  return files;
};

const m3u82url = (m3u8) => m3u8.split('\n').filter((line) => line[0] !== '#');

const url2hostname = (url) => {
  const p = url.indexOf('://') + 3;
  const q = url.indexOf('/', p);

  return url.slice(p, q);
};

const waitASecond = () => new Promise((resolve) => {
  setTimeout(resolve, 1000);
});

module.exports = {
  append, handleError, listDir, m3u82url, waitASecond, url2hostname,
};
