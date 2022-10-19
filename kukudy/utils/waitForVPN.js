/* eslint-disable no-await-in-loop */
const axios = require('axios');
const { sleep } = require('./utils');

const url = 'https://nordvpn.com/wp-admin/admin-ajax.php';
const config = { params: { action: 'get_user_info_data' } };

const reqVPNStatus = async () => axios.get(url, config);

const waitForVPN = async () => {
  let { data } = await reqVPNStatus();

  while (!data.status) {
    await sleep(3000);
    data = (await reqVPNStatus()).data;
  }

  return data;
};

module.exports = { reqVPNStatus };

if (require.main === module) {
  waitForVPN();
}
