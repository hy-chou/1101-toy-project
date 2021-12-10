// const API = require("../src/Api.js");
const API = require("../Jujuby/Prober/src/Api.js");
const fs = require("fs");
const path = require("path");

const handleError = (err, content, filename = "error.err") => {
  const msg = `  [${new Date().toISOString()}]\n` + content + "\n" + err + "\n";
  fs.appendFileSync(path.join(process.cwd(), filename), msg);
};

const pullTopN = async (amount) => {
  const records = [];
  let cursor = "";

  while (true) {
    const response = await API.twitchAPI("/helix/streams", {
      first: amount,
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
  const file1name = `${new Date().toISOString().substring(0, 13)}raw.json`;
  const file1path = path.join(process.cwd(), file1name);
  try {
    fs.appendFileSync(file1path, `${new Date().toISOString()}\n`);
    fs.appendFileSync(file1path, JSON.stringify(records));
  } catch (err) {
    handleError(err, "Err at writeTopN()->writeFS()");
  }

  const file2name = `${new Date().toISOString().substring(0, 13)}top.csv`;
  const file2path = path.join(process.cwd(), file2name);
  let user_login_line = `${new Date().toISOString()}`;
  let viewer_count_line = `${new Date().toISOString()}`;
  records.map((item) => {
    user_login_line += `, ${item["user_login"]}`;
    viewer_count_line += `, ${item["viewer_count"]}`;
  });
  user_login_line += `\n`;
  viewer_count_line += `\n`;
  try {
    fs.appendFileSync(file2path, user_login_line);
    fs.appendFileSync(file2path, viewer_count_line);
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
