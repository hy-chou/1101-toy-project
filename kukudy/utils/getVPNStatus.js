const axios = require('axios');

const url = 'https://nordvpn.com/wp-admin/admin-ajax.php';
const config = { params: { action: 'get_user_info_data' } };

const getVPNStatus = async () => axios.get(url, config)
  // eslint-disable-next-line no-console
  .then((res) => console.log(res.data));

if (require.main === module) {
  getVPNStatus();
}
