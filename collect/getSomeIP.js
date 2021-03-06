const fs = require("fs");
const path = require("path");
const { URL } = require("url");
const cron = require("node-cron");
const {
  getAccessToken,
  getBestQualityPlaylistUri,
  getEdgeUrl,
  getMasterPlaylist,
  getPlaylistContent,
  parseMasterPlaylist,
} = require("./getEdgeAddrLocal.js");
const { getSomeInfo } = require("./getSomeInfo.js");
const { lookupDNSCache } = require("../../Jujuby/Prober/Cache/DNSCache.js");

const handleError = (err, content, filename = "error.err") => {
  const msg = new Date().toISOString() + "\t" + content + "\t" + err + "\n";
  fs.appendFileSync(path.join(process.cwd(), filename), msg);
};

const readViewerCount = async (amountP, amountQ) => {
  const ts2H = new Date().toISOString().substring(0, 13);
  const filename = `${ts2H}vcnt${amountP}_${amountQ}.tsv`;
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
  const ts2H = new Date().toISOString().substring(0, 13);

  for (let i = 0; i < channels.length; i++) {
    const filename = ts2H + channels[i] + ".tsv";
    const filepath = path.join(process.cwd(), filename);

    const ts1 = new Date();
    let ip = await getIP(channels[i]);
    const ts2 = new Date();
    const dts = (ts2 - ts1)/1000;

    try {
      fs.appendFileSync(filepath, ts1.toISOString() + "\t" + ip + "\t" + dts + "\n");
    } catch (err) {
      handleError(err, `@ get3IP(), ${channels[i]}`);
    }
  }
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

module.exports = { getSomeIP };

if (require.main === module) {
  if (process.argv.length === 2) {
    getSomeIP();
  } else if (process.argv.length === 4) {
    getSomeIP(Number(process.argv[2]), Number(process.argv[3]));
  } else if (process.argv.length === 6) {
    cron.schedule(process.argv[4], () =>{
      let p = Number(process.argv[2]);
      const q = Number(process.argv[3]);
      let pqarray = [];

      while (p + 99 < q) {
        pqarray.push([p, p + 99]);
        p += 100;
      }
      pqarray.push([p, q]);

      pqarray.map((pq) => {
        getSomeIP(pq[0], pq[1]);
      });
    });

    cron.schedule(process.argv[5], () => process.kill(process.pid, 'SIGTERM'));
  }
}
