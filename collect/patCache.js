const { readFile } = require('node:fs/promises');

const KAPI = require('./KAPI');
const { append, handleError, writeIPv4 } = require('./kutils');

const readPATCache = async (channel) => {
  const ts2m1 = new Date().toISOString().slice(0, 15).replace(':', '.');
  const cachePath = `cache/pat/${ts2m1}/${channel}.tsv`;

  const lines = await readFile(cachePath, 'utf8')
    .catch((err) => {
      if (err.code !== 'ENOENT') {
        handleError(err.message, '@readPATCache()');
        throw new Error('handled');
      }
    });

  const record = JSON.parse(lines.split('\n').at(-2).split('\t').at(-1));

  return record;
};

const writePATCache = (channel, record) => {
  const ts = new Date().toISOString();
  const ts2m1 = ts.slice(0, 15).replace(':', '.');
  const cachePath = `cache/pat/${ts2m1}/${channel}.tsv`;

  const lines = `${ts}\t${record}\n`;

  return append(cachePath, lines);
};

const getPATRecord = async (channel) => readPATCache(channel)
  .catch(async (err) => {
    if (err.message === 'handled') throw new Error('handled');

    const sPAToken = await KAPI.reqPlaybackAccessToken(channel)
      .then((res) => res.data.data.streamPlaybackAccessToken);

    if (JSON.parse(sPAToken.value).authorization.forbidden) {
      await writeIPv4(channel, '#403');
      await handleError(JSON.parse(sPAToken.value).authorization.reason, '@getPATRecord()');
      throw new Error('handled');
    }

    await writePATCache(channel, JSON.stringify(sPAToken));

    return sPAToken;
  });

module.exports = { getPATRecord };
