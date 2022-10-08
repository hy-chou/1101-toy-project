const axios = require('axios');

const url = 'https://nordvpn.com/wp-admin/admin-ajax.php';
const config = { params: { action: 'get_user_info_data' } };

const reqVPNStatus = async () => axios.get(url, config);

module.exports = { reqVPNStatus };

if (require.main === module) {
  reqVPNStatus()
    .then((res) => console.log(res.data));
}
