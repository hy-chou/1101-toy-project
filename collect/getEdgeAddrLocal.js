const { dirname } = require('node:path');
const { mkdir, appendFile } = require('node:fs/promises');
const KAPI = require('./KAPI');
const { getDNSRecord } = require('./Kache');

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

// get Media Playlist that contains URLs of the files needed for streaming
function parseMasterPlaylist(playlist) {
  const parsedPlaylist = [];
  const lines = playlist.split('\n');
  for (let i = 4; i < lines.length - 1; i += 3) {
    parsedPlaylist.push({
      quality: lines[i - 2].split('NAME="')[1].split('"')[0],
      resolution:
        lines[i - 1].indexOf('RESOLUTION') !== -1
          ? lines[i - 1].split('RESOLUTION=')[1].split(',')[0]
          : null,
      uri: lines[i],
    });
  }

  if (parsedPlaylist.length === 0) {
    // playlist format is different then above
    const playlistInfo = {
      quality: lines[2].split('NAME="')[1].split('"')[0],
      resolution: lines[3].split('RESOLUTION=')[1].split(',')[0],
      uri: lines[4],
    };
    parsedPlaylist.push(playlistInfo);
  }

  return parsedPlaylist;
}

function getEdgeUrl(raw) {
  const lines = raw.split('\n');
  const urls = lines.filter((line) => line !== '' && line[0] !== '#');
  return urls.at(-1);
}

const getHostnameFromUrl = (url) => {
  const schemeless = url.slice(url.indexOf('://') + 3);
  const hostname = schemeless.slice(0, schemeless.indexOf('/'));
  return hostname;
};

const getEdgeAddr = async (channel) => KAPI.getPlaybackAccessToken(channel)
  .then((res) => res.data.data.streamPlaybackAccessToken)
  .then((token) => KAPI.getMasterPlaylist(token, channel))
  .then((res) => res.data)
  .then((masterPlaylist) => parseMasterPlaylist(masterPlaylist))
  .then((playlists) => playlists[0].uri)
  .then((uri) => KAPI.get(uri).then((res) => res.data))
  .then((rawContent) => getEdgeUrl(rawContent))
  .then((url) => getHostnameFromUrl(url))
  .then((hostname) => getDNSRecord(hostname))
  .catch((error) => {
    handleError(error, `@ getEdgeAddr(), ${channel}`);
    return error.message;
  });

module.exports = { getEdgeAddr };
