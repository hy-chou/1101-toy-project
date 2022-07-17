const fs = require("fs");
const path = require("path");
const cron = require("node-cron");
const process = require("process");
const API = require("../../Jujuby/Prober/src/Api.js");


const handleError = async (err, location) => {
  const ts = new Date().toISOString();
  const lines = `${ts}\t${location}\t${err}\n`;

  fs.appendFileSync(path.join(process.cwd(), "error.err"), lines);
};

const getAPageOfStreams = async (cursor="") => {
  return API.twitchAPI("/helix/streams", {
    first: 100,
    after: cursor,
  })
  .then((response) => {
    writeRaw(response.data);
    return response.data;
  })
  .catch((err) => handleError(err, "@ getAPageOfStreams()"))
};

const writeRaw = (data) => {
  const rawPath = path.join(process.cwd(), `raw.json.tsv`);
  const lines = new Date().toISOString() + "\t" +JSON.stringify(data) + "\n";

  try {
    fs.appendFileSync(rawPath, lines);
  } catch (err) {
    handleError(err, "@ writeRaw()");
  }
};

const writeUserLogins = async (p, ulogins) => {
  const ulgPath = path.join(process.cwd(), `p${p}.ulg.tsv`);
  let lines = new Date().toISOString() + "\n";

  ulogins.map(ulogin => lines += ulogin + "\t");
  lines = lines.slice(0, -1) + "\n";

  try {
    fs.appendFileSync(ulgPath, lines);
  } catch (err) {
    handleError(err, "@writeUserLogins()");
  }
};

const getUserLogins = async (p1=1, pn=1) => {
  let p = 1;
  let data = await getAPageOfStreams();

  while (p < p1) {
    p += 1;
    data = await getAPageOfStreams(data.pagination.cursor);
  }
  writeUserLogins(p, data.data.map((item) => item.user_login));

  while (p < pn) {
    p += 1;
    data = await getAPageOfStreams(data.pagination.cursor);
    writeUserLogins(p, data.data.map((item) => item.user_login));
  }
};

module.exports = { getUserLogins };

if (require.main === module) {
  const pargv = process.argv;
  const stopProcess = () => process.kill(process.pid, 'SIGTERM');

  switch (pargv.length) {
    case 2:
      getUserLogins()
      .then(stopProcess);
      break;
    case 4:
      getUserLogins(Number(pargv[2]), Number(pargv[3]))
      .then(stopProcess);
      break;
    case 6:
      cron.schedule(pargv[4], () => getUserLogins(Number(pargv[2]), Number(pargv[3])));
      cron.schedule(pargv[5], stopProcess);
      break;
    default:
      console.log("Error:  wrong argv")
      stopProcess();
  }
}
