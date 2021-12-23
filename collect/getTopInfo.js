const API = require("../../Jujuby/Prober/src/Api.js");
const fs = require("fs");
const path = require("path");

const handleError = (err, content, filename = "error.err") => {
  const msg = `  [${new Date().toISOString()}]\n` + content + "\n" + err + "\n";
  fs.appendFileSync(path.join(process.cwd(), filename), msg);
};

const pullTopN = async (amount) => {
  let N = amount;
  const records = [];
  let cursor = "";

  while (N > 0) {
    let n = N >= 100 ? 100 : N;
    N -= 100;

    const response = await API.twitchAPI("/helix/streams", {
      first: n,
      after: cursor,
    });
    const liveChannels = response.data.data;

    if (liveChannels.length === 0 || records.length >= amount) break;
    liveChannels.map((data) => records.push(data));
    cursor = response.data.pagination.cursor;
  }
  return records;
};

const writeTopN = async (records) => {
  const now = new Date();

  const rawFileName = `${now.toISOString().substring(0, 13)}raw.json`;
  const rawFilePath = path.join(process.cwd(), rawFileName);
  try {
    fs.appendFileSync(rawFilePath, `${now.toISOString().substring(14)}\n`);
    fs.appendFileSync(rawFilePath, JSON.stringify(records));
  } catch (err) {
    handleError(err, "Err at writeTopN()->writeFS()");
  }

  const topFileName = `${now.toISOString().substring(0, 13)}top.csv`;
  const topFilePath = path.join(process.cwd(), topFileName);
  let user_login_line = "";
  let viewer_count_line = `${now.toISOString().substring(14)}`;
  records.map((item) => {
    user_login_line += `, ${item["user_login"]}`;
    viewer_count_line += `, ${item["viewer_count"]}`;
  });
  user_login_line = user_login_line.substring(2) + `\n`;
  viewer_count_line += `\n`;
  try {
    fs.appendFileSync(topFilePath, user_login_line);
    fs.appendFileSync(topFilePath, viewer_count_line);
  } catch (err) {
    handleError(err, "Err at writeTopN()->appendFS()");
    console.error(err);
  }
};

const getTopInfo = async (amount = 10) => {
  return pullTopN(amount)
    .then((records) => writeTopN(records))
    .catch((err) => handleError(err, "Err at getTopInfo()"));
};

module.exports = { pullTopN, writeTopN, getTopInfo };

if (require.main === module) {
  getTopInfo();
}
