const API = require("../../Jujuby/Prober/src/Api.js");
const fs = require("fs");
const path = require("path");

const handleError = (err, content, filename = "error.err") => {
  const msg = `\t[${new Date().toISOString()}]\n` + content + "\n" + err + "\n";
  fs.appendFileSync(path.join(process.cwd(), filename), msg);
};

const pullInfo = async (amountP, amountQ) => {
  let P = amountP - 1;
  let N = amountQ - amountP + 1;
  const records = [];
  let cursor = "";

  while (P > 0) {
    let n = P >= 100 ? 100 : P;
    P -= 100;

    const response = await API.twitchAPI("/helix/streams", {
      first: n,
      after: cursor,
    });
    const liveChannels = response.data.data;

    if (liveChannels.length === 0) break;
    cursor = response.data.pagination.cursor;
  }
  while (N > 0) {
    let n = N >= 100 ? 100 : N;
    N -= 100;

    const response = await API.twitchAPI("/helix/streams", {
      first: n,
      after: cursor,
    });
    const liveChannels = response.data.data;

    if (liveChannels.length === 0 || records.length >= amountQ - amountP + 1)
      break;
    liveChannels.map((data) => records.push(data));
    cursor = response.data.pagination.cursor;
  }
  return records;
};

const writeInfo = async (records, amountP, amountQ) => {
  const now = new Date();

  const rawFileName = `${now.toISOString().substring(0, 13)}raw.json`;
  const rawFilePath = path.join(process.cwd(), rawFileName);

  try {
    fs.appendFileSync(rawFilePath, `\t[${now.toISOString()}]\n`);
    fs.appendFileSync(rawFilePath, JSON.stringify(records));
  } catch (err) {
    handleError(err, "@ writeInfo(), raw.json");
  }

  const vcntFileName = `${new Date()
    .toISOString()
    .substring(0, 13)}vcnt${amountP}_${amountQ}.csv`;
  const vcntFilePath = path.join(process.cwd(), vcntFileName);

  let user_login_line = "";
  let viewer_count_line = "";
  records.map((item) => {
    user_login_line += `, ${item["user_login"]}`;
    viewer_count_line += `, ${item["viewer_count"]}`;
  });
  user_login_line = user_login_line.substring(2) + `\n`;
  viewer_count_line = viewer_count_line.substring(2) + `\n`;
  try {
    fs.appendFileSync(vcntFilePath, `\t${now.toISOString().substring(14)}\n`);
    fs.appendFileSync(vcntFilePath, user_login_line);
    fs.appendFileSync(vcntFilePath, viewer_count_line);
  } catch (err) {
    handleError(err, "@ writeInfo(), vcnt.csv");
    console.error(err);
  }
};

const getSomeInfo = async (amountP = 1, amountQ = 3) => {
  return pullInfo(amountP, amountQ)
    .then((records) => writeInfo(records, amountP, amountQ))
    .catch((err) => handleError(err, "@ getSomeInfo()"));
};

module.exports = { pullInfo, writeInfo, getSomeInfo };

if (require.main === module) {
  getSomeInfo();
}
