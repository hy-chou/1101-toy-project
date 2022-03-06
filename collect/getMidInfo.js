const API = require("../../Jujuby/Prober/src/Api.js");
const fs = require("fs");
const path = require("path");

const handleError = (err, content, filename = "error.err") => {
  const msg = `  [${new Date().toISOString()}]\n` + content + "\n" + err + "\n";
  fs.appendFileSync(path.join(process.cwd(), filename), msg);
};

const pullMidN = async (amountP, amountQ) => {
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
    // const liveChannels = response.data.data;

    // if (liveChannels.length === 0 || records.length >= amountQ - amountP + 1) break;
    // liveChannels.map((data) => records.push(data));
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

const writeMidN = async (records) => {
  const now = new Date();

  const rawFileName = `${now.toISOString().substring(0, 13)}raw.json`;
  const rawFilePath = path.join(process.cwd(), rawFileName);
  try {
    fs.appendFileSync(rawFilePath, `${now.toISOString().substring(14)}\n`);
    fs.appendFileSync(rawFilePath, JSON.stringify(records));
  } catch (err) {
    handleError(err, "Err at writeMidN()->writeFS()");
  }

  const fileName = `${now.toISOString().substring(0, 13)}mid.csv`;
  const filePath = path.join(process.cwd(), fileName);
  let user_login_line = "";
  let viewer_count_line = `${now.toISOString().substring(14)}`;
  records.map((item) => {
    user_login_line += `, ${item["user_login"]}`;
    viewer_count_line += `, ${item["viewer_count"]}`;
  });
  user_login_line = user_login_line.substring(2) + `\n`;
  viewer_count_line += `\n`;
  try {
    fs.appendFileSync(filePath, user_login_line);
    fs.appendFileSync(filePath, viewer_count_line);
  } catch (err) {
    handleError(err, "Err at writeMidN()->appendFS()");
    console.error(err);
  }
};

const getMidInfo = async (amountP = 3, amountQ = 5) => {
  return pullMidN(amountP, amountQ)
    .then((records) => writeMidN(records))
    .catch((err) => handleError(err, "Err at getMidInfo()"));
};

module.exports = { pullMidN, writeMidN, getMidInfo };

if (require.main === module) {
  getMidInfo();
}
