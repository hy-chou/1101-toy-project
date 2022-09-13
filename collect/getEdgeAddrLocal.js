const { URL } = require("url");
const { dirname } = require("node:path");
const m3u8Parser = require("m3u8-parser");
const { mkdir, appendFile } = require("node:fs/promises");
const KAPI = require("./KAPI.js");
const { getDNSRecord } = require("./Kache.js");

const handleError = async (err, location) => {
  const ts = new Date().toISOString();
  const ts2H = ts.slice(0, 13);
  const errPath = `errs/${ts2H}error.tsv`;
  const lines = ts + "\t" + location + "\t" + err + "\n";

  console.error(lines);
  return append(errPath, lines);
};

const append = async (path, data) => {
  await mkdir(dirname(path), { recursive: true });
  return appendFile(path, data);
};

function getPlaybackAccessToken(channel) {
  return KAPI.getPlaybackAccessToken(channel).then(
    (res) => res.data.data.streamPlaybackAccessToken
  );
}

function getMasterPlaylist(token, channel) {
  return KAPI.getMasterPlaylist(token, channel).then((res) => res.data);
}

// get Media Playlist that contains URLs of the files needed for streaming
function parseMasterPlaylist(playlist) {
  const parsedPlaylist = [];
  const lines = playlist.split("\n");
  for (let i = 4; i < lines.length - 1; i += 3) {
    parsedPlaylist.push({
      quality: lines[i - 2].split('NAME="')[1].split('"')[0],
      resolution:
        lines[i - 1].indexOf("RESOLUTION") !== -1
          ? lines[i - 1].split("RESOLUTION=")[1].split(",")[0]
          : null,
      uri: lines[i],
    });
  }

  if (parsedPlaylist.length === 0) {
    // playlist format is different then above
    const playlistInfo = {
      quality: lines[2].split('NAME="')[1].split('"')[0],
      resolution: lines[3].split("RESOLUTION=")[1].split(",")[0],
      uri: lines[4],
    };
    parsedPlaylist.push(playlistInfo);
  }

  return parsedPlaylist;
}

function getBestQualityPlaylistUri(playlists) {
  return playlists[0].uri;
}

function getPlaylistContent(uri) {
  return KAPI.get(uri).then((res) => res.data);
}

function getEdgeUrl(raw) {
  const parser = new m3u8Parser.Parser();
  parser.push(raw);
  parser.end();
  // return the uri of the last .ts file
  return parser.manifest.segments.slice(-1).pop().uri;
}

const getEdgeAddr = async (channel) => {
  return getPlaybackAccessToken(channel)
    .then((token) => getMasterPlaylist(token, channel))
    .then((masterPlaylist) => parseMasterPlaylist(masterPlaylist))
    .then((playlists) => getBestQualityPlaylistUri(playlists))
    .then((uri) => getPlaylistContent(uri))
    .then((rawContent) => new URL(getEdgeUrl(rawContent)).hostname)
    .then((hostname) => getDNSRecord(hostname))
    .catch((error) => {
      handleError(error, `@ getEdgeAddr(), ${channel}`);
      return error.message;
    });
};

module.exports = { getEdgeAddr };
