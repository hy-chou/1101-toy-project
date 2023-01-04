/* eslint-disable no-await-in-loop */
const axios = require('axios');
const { getTS, sleep, writeData } = require('./utils');

const reqVPNStatus = () => axios.get(
  'https://nordvpn.com/wp-admin/admin-ajax.php',
  { params: { action: 'get_user_info_data' } },
);

const waitForVPN = async () => {
  let countdown = 0;
  let { data } = await reqVPNStatus();

  while (!data.status && countdown < 10_000) {
    await sleep(countdown);
    data = (await reqVPNStatus()).data;
    countdown += 1000;
  }

  if (!data.status) {
    process.exit(1);
  }

  await writeData(
    './logs/vpn.json.tsv',
    `${getTS()}\t${JSON.stringify(data)}\n`,
  );
};

if (require.main === module) {
  waitForVPN();
}
