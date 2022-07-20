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

const writeUserLogins = async (c, ulogins) => {
  const ulgPath = path.join(process.cwd(), `ulg${c}.tsv`);
  let lines = new Date().toISOString() + "\n";

  ulogins.map(ulogin => lines += ulogin + "\t");
  lines = lines.slice(0, -1) + "\n";

  try {
    fs.appendFileSync(ulgPath, lines);
  } catch (err) {
    handleError(err, "@writeUserLogins()");
  }
};

const getUserLogins = async (c1=1, cn=100, groupSize=100) => {
  let cSliced = 0;
  let data = await getAPageOfStreams();
  let grandList = data.data.map((item) => item.user_login);

  while (grandList.length < c1) {
    data = await getAPageOfStreams(data.pagination.cursor);
    grandList = grandList.concat(data.data.map((item) => item.user_login));
  }

  grandList = grandList.slice(c1 - 1);
  cSliced += c1 - 1;

  while (cSliced < cn) {
    while (grandList.length < groupSize) {
      data = await getAPageOfStreams(data.pagination.cursor);
      grandList = grandList.concat(data.data.map((item) => item.user_login));
    }
    writeUserLogins(cSliced + 1, grandList.slice(0, Math.min(groupSize, cn - cSliced)))
    grandList = grandList.slice(groupSize);
    cSliced += groupSize;
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
