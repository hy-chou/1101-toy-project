const fs = require("fs");
const path = require("path");
const cron = require("node-cron");
const process = require("process");
const API = require("../../Jujuby/Prober/src/Api.js");

const handleError = async (err, location) => {
  const ts = new Date().toISOString();
  const lines = ts + "\t" + location + "\t" + err + "\n";

  fs.appendFileSync(path.join(process.cwd(), "error.err"), lines);
}

const getAPageOfStreams = async (cursor="") => {
  const response = await API.twitchAPI("/helix/streams", {
    first: 100,
    after: cursor,
  });

  const ts = new Date().toISOString();
  const rawPath = path.join(process.cwd(), `raw.json.tsv`);
  const rawLines = ts + "\t" +JSON.stringify(response.data) + "\n";

  fs.appendFile(rawPath, rawLines, (err) => {
    if (err) handleError(err, "@getAPageOfStreams");
  });

  return response.data
}

const getUserLogins = async (p1=1, pn=1) => {
  let p = 1;
  let ulogins = [];
  let data = await getAPageOfStreams();
  let cursor = data.pagination.cursor;

  while (p < p1) {
    p += 1;
    data = await getAPageOfStreams(cursor);
    cursor = data.pagination.cursor;
  }
  data.data.map((item) => ulogins.push(item.user_login));
  writeUserLogins(ulogins.slice(), p);

  while (p < pn) {
    p += 1;
    ulogins = [];
    data = await getAPageOfStreams(cursor);
    cursor = data.pagination.cursor;
    data.data.map(item => ulogins.push(item.user_login));
    writeUserLogins(ulogins.slice(), p);
  }
}

const writeUserLogins = async (ulogins, p) => {
  const ts = new Date().toISOString();
  let lines = "";

  ulogins.map(ulogin => lines += "\t" + String(ulogin));
  lines = ts + "\n" + lines.substring(1) + "\n";

  const uloginsFileName = `ulogins${p}.tsv`;
  const uloginsFilePath = path.join(process.cwd(), uloginsFileName);

  console.log(lines.substring(0, 80) + "...");

  try {
    fs.appendFileSync(uloginsFilePath, lines);
  } catch (err) {
    handleError(err, "@writeUserLogins, ulogins.tsv");
  }
}

module.exports = { getUserLogins };

if (require.main === module) {
  if (process.argv.length === 2) {
    getUserLogins()
    .then(() => process.kill(process.pid, 'SIGTERM'));
  } else if (process.argv.length === 4) {
    getUserLogins(Number(process.argv[2]), Number(process.argv[3]))
    .then(() => process.kill(process.pid, 'SIGTERM'));
  } else if (process.argv.length === 6) {
    cron.schedule(process.argv[4], () => {
      getUserLogins(Number(process.argv[2]), Number(process.argv[3]))
    });
    cron.schedule(process.argv[5], () => process.kill(process.pid, 'SIGTERM'));
  }
}
