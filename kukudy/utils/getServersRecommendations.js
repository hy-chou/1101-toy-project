const axios = require('axios');
const countryID = require('./nordVPNCountryList').countryList.TW;

const url = 'https://nordvpn.com/wp-admin/admin-ajax.php';
const config = {
  params: {
    action: 'servers_recommendations',
    filters: {
      country_id: countryID,
      servers_technologies: [3],
    },
  },
};

const getServersRecommendations = async () => axios.get(url, config)
  .then((res) => res.data.map(
    (server) => server.hostname.slice(0, server.hostname.indexOf('.')),
  ));

if (require.main === module) {
  getServersRecommendations()
    // eslint-disable-next-line no-console
    .then((serverID) => console.log(serverID.join('\t')));
}
