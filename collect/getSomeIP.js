const fs = require("fs");
const path = require("path");
const { URL } = require("url");
const { lookupDNSCache } = require("../../Jujuby/Prober/Cache/DNSCache.js");
const {
  getAccessToken,
  getBestQualityPlaylistUri,
  getEdgeUrl,
  getMasterPlaylist,
  getPlaylistContent,
  parseMasterPlaylist,
} = require("../../Jujuby/Prober/Utils/getEdgeAddr.js");
const { getSomeInfo } = require("./getSomeInfo.js");

const handleError = (err, content, filename = "error.err") => {
  const msg = new Date().toISOString() + "\t" + content + "\t" + err + "\n";
  fs.appendFileSync(path.join(process.cwd(), filename), msg);
};

const readViewerCount = async (amountP, amountQ) => {
  const tsY2H = new Date().toISOString().substring(0, 13);
  const filename = `${tsY2H}vcnt${amountP}_${amountQ}.tsv`;
  const filepath = path.join(process.cwd(), filename);

  let channels = [];
  try {
    let content = fs.readFileSync(filepath, "utf8");

    content = content.split("\n");
    channels = content[content.length - 3].split("\t");
  } catch (err) {
    handleError(err, "@ readMidN()");
  }
  return channels;
};

const getIP = async (channel) => {
  return getAccessToken(channel)
    .then((token) => getMasterPlaylist(token, channel))
    .then((masterPlaylist) => parseMasterPlaylist(masterPlaylist))
    .then((playlists) => getBestQualityPlaylistUri(playlists))
    .then((uri) => getPlaylistContent(uri))
    .then((rawContent) => {
      const urlObj = new URL(getEdgeUrl(rawContent));
      return urlObj.hostname;
    })
    .then((hostname) => {
      const ip = lookupDNSCache(hostname);
      return ip;
    })
    .catch((error) => {
      handleError(error, `@ getIP(), ${channel}`);
      return error.message;
    });
};

const get3IP = async (channels) => {
  if (channels.length === 0) {
    const err = "Empty list. channels.length === 0";
    handleError(err, err);
    return;
  }
  const tsD2H = new Date().toISOString().substring(8, 13);

  // const t0 = new Date();
  for (let i = 0; i < channels.length; i++) {
    const filename = tsD2H + channels[i] + ".tsv";
    const filepath = path.join(process.cwd(), filename);

    const tsH2 = new Date().toISOString().substring(11);
    let ip = await getIP(channels[i]);
    const tsM2 = new Date().toISOString().substring(14);

    try {
      fs.appendFileSync(filepath, tsH2 + "\t" + ip + "\t" + tsM2 + "\n");
    } catch (err) {
      handleError(err, `@ get3IP(), ${channels[i]}`);
    }
  }
  // const tn = new Date();
  // if (t0.getMinutes() % 10 === 0) {
  //   const dt = (tn - t0) / 1000;
  //   const filename = `${new Date().toISOString().substring(0, 13)}dt.csv`;
  //   const filepath = path.join(process.cwd(), filename);
  //   try {
  //     fs.appendFileSync(
  //       filepath,
  //       `"${t0.toISOString().substring(11)}",${dt}\n`
  //     );
  //   } catch (err) {
  //     handleError(err, "@ get3IP(), dt");
  //   }
  // }
};

const getSomeIP = async (amountP = 1, amountQ = 3) => {
  const ts2H = new Date().toISOString().substring(0, 13);
  const filename = `${ts2H}vcnt${amountP}_${amountQ}.tsv`;
  const filepath = path.join(process.cwd(), filename);

  if (!fs.existsSync(filepath)) await getSomeInfo(amountP, amountQ);

  readViewerCount(amountP, amountQ)
    .then((channels) => get3IP(channels))
    .catch((err) => {
      handleError(err, "Err at getSomeIP()");
    });
};

module.exports = { readViewerCount, getIP, get3IP, getSomeIP };

if (require.main === module) {
  getSomeIP();
}
