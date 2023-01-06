/* eslint-disable no-console */
const axios = require('axios');

const cityToCountryID = {
  Madrid: 202, // ES
  London: 227, // UK
  Paris: 74, // FR
  Amsterdam: 153, // NL
  Marseille: 74, // FR
  Frankfurt: 81, // DE
  Milan: 106, // IT
  Oslo: 163, // NO
  Copenhagen: 58, // DK
  Berlin: 81, // DE
  Prague: 57, // CZ
  Vienna: 14, // AT
  Stockholm: 208, // SE
  Warsaw: 174, // PL
  Helsinki: 73, // FI
};

if (require.main === module) {
  const cityName = process.argv[2];
  const countryID = cityToCountryID[cityName];

  if (countryID === undefined) {
    console.error(`city "${cityName}" DNE`);
    process.exit(1);
  }

  axios.get('https://nordvpn.com/wp-admin/admin-ajax.php', {
    params: {
      action: 'servers_recommendations',
      filters: {
        country_id: countryID,
        servers_technologies: [3],
      },
      limit: 9999,
    },
  })
    .then((res) => res.data)
    .then((data) => data
      .filter((item) => item.locations[0].country.city.name === cityName))
    .then((serverList) => {
      if (serverList.length === 0) {
        process.exit(1);
      }

      const { hostname } = serverList[0];

      console.log(hostname.slice(0, hostname.indexOf('.')));
    });
}
