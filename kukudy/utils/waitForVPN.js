/* eslint-disable no-await-in-loop */
const axios = require('axios');
const { sleep } = require('./utils');

const reqVPNStatus = () => axios.get(
  'https://nordvpn.com/wp-admin/admin-ajax.php',
  { params: { action: 'get_user_info_data' } },
);

const waitForVPN = async () => {
  let { data } = await reqVPNStatus();

  while (!data.status) {
    await sleep(3000);
    data = (await reqVPNStatus()).data;
  }
};

if (require.main === module) {
  waitForVPN();
}
