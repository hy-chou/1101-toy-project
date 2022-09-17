const { dirname } = require('node:path');
const { mkdir, appendFile, readdir } = require('node:fs/promises');

const getLatestFiles = async () => {
  const allTS2H = await readdir('./ulgs');
  const lastTS2H = allTS2H.at(-1);
  const latestFiles = await readdir(`./ulgs/${lastTS2H}`);

  return latestFiles.map((file) => `./ulgs/${lastTS2H}/${file}`);
};

const append = async (path, data) => {
  await mkdir(dirname(path), { recursive: true });
  return appendFile(path, data);
};

const handleError = async (err, location) => {
  const ts = new Date().toISOString();
  const ts2H = ts.slice(0, 13);
  const errPath = `errs/${ts2H}error.tsv`;
  const lines = `${ts}\t${location}\t${err}\n`;

  // console.error(lines);
  return append(errPath, lines);
};

const waitASecond = () => new Promise((resolve) => {
  setTimeout(resolve, 1000);
});

module.exports = {
  append, handleError, waitASecond, getLatestFiles,
};
