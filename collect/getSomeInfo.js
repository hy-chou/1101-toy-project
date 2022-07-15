const API = require("../../Jujuby/Prober/src/Api.js");
const fs = require("fs");
const path = require("path");
const process = require("process");
const cron = require("node-cron");
const { getSomeIP } = require("./getSomeIP.js");

const handleError = (err, content, filename = "error.err") => {
  const msg = new Date().toISOString() + "\t" + content + "\t" + err + "\n";
  fs.appendFileSync(path.join(process.cwd(), filename), msg);
};

const pullInfo = async (amountP, amountQ) => {
  let N = amountQ;
  const records = [];
  let cursor = "";

  while (N > 0){
    N -= 100;

    const response = await API.twitchAPI("/helix/streams", {
      first: 100,
      after: cursor,
    });
    const liveChannels = response.data.data;

    if (liveChannels.length === 0) break;

    liveChannels.map((data) => records.push(data));
    cursor = response.data.pagination.cursor;
  }

  return records.slice(amountP - amountQ - 1);
};

const chunkInfo = async (longrecords, amountP, amountQ) => {
  let N = 0;

  while (N + 100 < amountQ - amountP + 1) {
    writeInfo(longrecords.slice(N, N + 100), amountP + N, amountP + N + 99);
    N += 100;
  }
  writeInfo(longrecords.slice(N), amountP + N, amountQ);
}

const writeInfo = async (records, amountP, amountQ) => {
  const ts = new Date().toISOString();
  const ts2H = ts.substring(0, 13);

  const rawFileName = ts2H + "raw.json.tsv";
  const rawFilePath = path.join(process.cwd(), rawFileName);

  try {
    fs.appendFileSync(rawFilePath, `${ts}\t${JSON.stringify(records)}\n`);
  } catch (err) {
    handleError(err, "@ writeInfo(), raw.json.tsv");
  }

  const vcntFileName = `${ts2H}vcnt${amountP}_${amountQ}.tsv`;
  const vcntFilePath = path.join(process.cwd(), vcntFileName);

  let user_login_line = "";
  let viewer_count_line = "";
  records.map((item) => {
    user_login_line += "\t" + item["user_login"];
    viewer_count_line += "\t" + item["viewer_count"];
  });
  user_login_line = user_login_line.substring(1) + "\n";
  viewer_count_line = viewer_count_line.substring(1) + "\n";
  try {
    fs.appendFileSync(vcntFilePath, ts + "\n");
    fs.appendFileSync(vcntFilePath, user_login_line);
    fs.appendFileSync(vcntFilePath, viewer_count_line);
  } catch (err) {
    handleError(err, "@ writeInfo(), vcnt.csv");
    console.error(err);
  }
};

const getSomeInfo = async (amountP = 1, amountQ = 314) => {
  return pullInfo(amountP, amountQ)
    .then((records) => chunkInfo(records, amountP, amountQ))
    .catch((err) => handleError(err, "@ getSomeInfo()"));
};

module.exports = { getSomeInfo };

if (require.main === module) {
  if (process.argv.length === 2) {
    getSomeInfo();
  } else if (process.argv.length === 4) {
    getSomeInfo(Number(process.argv[2]), Number(process.argv[3]));
  } else if (process.argv.length === 6) {
    cron.schedule(process.argv[4], async () => {
      let p = Number(process.argv[2]);
      const q = Number(process.argv[3]);
      let pqarray = [];

      await getSomeInfo(p, q);
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
