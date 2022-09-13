const cron = require("node-cron");
const process = require("process");
const { dirname } = require("node:path");
const KAPI = require("./KAPI.js");
const { mkdir, appendFile } = require("node:fs/promises");

const handleError = async (err, location) => {
  const ts = new Date().toISOString();
  const ts2H = ts.slice(0, 13);
  const errPath = `errs/${ts2H}error.tsv`;
  const lines = ts + "\t" + location + "\t" + err + "\n";

  console.error(lines);
  return append(errPath, lines);
};

const append = async (path, data) => {
  await mkdir(dirname(path), { recursive: true });
  return appendFile(path, data);
};

const getAPageOfStreams = async (cursor = "") => {
  // return API.twitchAPI("/helix/streams", {
  //   first: 100,
  //   after: cursor,
  // })
  return KAPI.getStreams(cursor)
    .then(async (res) => {
      const ts = new Date().toISOString();
      const ts2H = ts.slice(0, 13);
      const rawPath = `raws/${ts2H}raw.json.tsv`;
      const lines = ts + "\t" + JSON.stringify(res.data) + "\n";

      await append(rawPath, lines);
      return res.data;
    })
    .catch((err) => handleError(err, "@ getAPageOfStreams()"));
};

const writeUserLogins = async (c, ulogins) => {
  const ts2H = new Date().toISOString().slice(0, 13);
  const ulgPath = `ulgs/${ts2H}/${ts2H}ulg${c}.tsv`;
  let lines = new Date().toISOString() + "\n";

  ulogins.map((ulogin) => (lines += ulogin + "\t"));
  lines = lines.slice(0, -1) + "\n";

  return append(ulgPath, lines);
};

const getUserLogins = async (c1 = 1, cn = 100, groupSize = 100) => {
  let cSliced = 0;
  let data = await getAPageOfStreams();
  let grandList = data.data.map((item) => item.user_login);
  let writingList = [];

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
    writingList.push(
      writeUserLogins(
        cSliced + 1,
        grandList.slice(0, Math.min(groupSize, cn - cSliced))
      )
    );
    grandList = grandList.slice(groupSize);
    cSliced += groupSize;
  }

  return Promise.all(writingList);
};

module.exports = { getUserLogins };

if (require.main === module) {
  const pargv = process.argv;
  const stopProcess = () => process.kill(process.pid, "SIGTERM");

  switch (pargv.length) {
    case 2:
      getUserLogins().then(stopProcess);
      break;
    case 4:
      getUserLogins(Number(pargv[2]), Number(pargv[3])).then(stopProcess);
      break;
    case 6:
      cron.schedule(pargv[4], () =>
        getUserLogins(Number(pargv[2]), Number(pargv[3]))
      );
      cron.schedule(pargv[5], stopProcess);
      break;
    default:
      console.log("Error:  wrong argv");
      stopProcess();
  }
}
