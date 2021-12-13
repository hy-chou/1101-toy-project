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
const { getTopInfo } = require("./getTopInfo.js");

const handleError = (err, content, filename = "error.err") => {
  const msg = `  [${new Date().toISOString()}]\n${content}\n${err}\n`;
  if (
    !msg.includes("Request failed with status code 403") &&
    !msg.includes("Request failed with status code 404")
  )
    fs.appendFileSync(path.join(process.cwd(), filename), msg);
};

const readTopN = async () => {
  const filename = `${new Date().toISOString().substring(0, 13)}top.csv`;
  const filepath = path.join(process.cwd(), filename);

  let channels = [];
  try {
    let content = fs.readFileSync(filepath, "utf8");

    content = content.slice(0, content.search("\n"));
    channels = content.split(", ");
    channels.shift();
  } catch (err) {
    handleError(err, "Err at readTopN()->fs.readFS()");
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
      handleError(error, `Err at getIP(), ${channel}`);
      return error.message;
    });
};

const get3IP = async (channels) => {
  if (channels.length === 0) {
    const err = "Empty list. channels.length === 0";
    handleError(err, err);
    return;
  }
  const rightnow = new Date();
  const fileprenom = rightnow.getUTCDate() + "T" + rightnow.getUTCHours() + "_";

  const t0 = new Date();

  for (let i = 0; i < channels.length; i++) {
    const filenom = fileprenom + channels[i] + ".csv";
    const filepath = path.join(process.cwd(), filenom);

    const t1 = new Date().toISOString().substring(11);
    let ip = await getIP(channels[i]);
    const t2 = new Date().toISOString().substring(11);

    if (ip === "Request failed with status code 403") ip = "!403!";
    else if (ip === "Request failed with status code 404") ip = "!404!";
    try {
      fs.appendFileSync(filepath, `"${t1}","${ip}","${t2}"\n`);
    } catch (err) {
      handleError(err, "Err at get3IP()->fs.appendFS()");
    }
  }

  const tn = new Date();
  if (t0.getSeconds() % 60 === 0) {
    const dt = (tn - t0) / 1000;
    const filename = `${new Date().toISOString().substring(0, 13)}dt.csv`;
    const filepath = path.join(process.cwd(), filename);
    try {
      fs.appendFileSync(
        filepath,
        `"${t0.toISOString().substring(11)}",${dt}\n`
      );
    } catch (err) {
      handleError(err, "Err at get3IP()->fs.appendFS(dt)");
    }
  }
};

const getTopIP = async (amount = 3) => {
  const filename = `${new Date().toISOString().substring(0, 13)}top.csv`;
  const filepath = path.join(process.cwd(), filename);

  if (!fs.existsSync(filepath)) await getTopInfo(amount);

  readTopN()
    .then((channels) => get3IP(channels))
    .catch((err) => {
      handleError(err, "Err at getTopIP()");
    });
};

module.exports = { readTopN, getIP, get3IP, getTopIP };

if (require.main === module) {
  getTopIP();
}
