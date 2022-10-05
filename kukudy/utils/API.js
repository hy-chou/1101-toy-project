const https = require('node:https');
const axios = require('axios');
const { writeData, getTS } = require('./utils');

require('dotenv').config({ path: '../.env' });

const kaxios = axios.create({
  timeout: 150_000,
  httpsAgent: new https.Agent({ keepAlive: true }),
});

kaxios.interceptors.response.use(
  async (response) => {
    const t2 = getTS();
    const ts2H = t2.slice(0, 13);
    const { type, t1 } = response.config.kukudy;
    const rtt = Date.parse(t2) - Date.parse(t1);

    await writeData(
      `./logs/rtts/${ts2H}/${type}.tsv`,
      `${t1}\t${rtt / 1000}\t${response.status}\n`,
    );
    if (type === 'reqStreams') {
      await writeData(
        `./logs/hdrs/${ts2H}/${type}.json.tsv`,
        `${t1}\t${JSON.stringify(response.headers)}\n`,
      );
    }

    return response;
  },
  async (error) => {
    const t2 = getTS();
    const ts2H = t2.slice(0, 13);
    const { type, t1 } = error.config.kukudy;
    const rtt = Date.parse(t2) - Date.parse(t1);

    await writeData(
      `./logs/rtts/${ts2H}/${type}.tsv`,
      `${t1}\t${rtt / 1000}\t${error.message}\n`,
    );

    if (error.code === 'ERR_BAD_REQUEST') {
      if (error.response.status === 404) { return Promise.reject(new Error('E404')); }
      if (error.response.status === 403) { return Promise.reject(new Error('E403')); }
    }
    if (error.code === 'ECONNABORTED') { return Promise.reject(new Error('ECONNABORTED')); }
    await writeData(
      `./errs/${ts2H}.tsv`,
      `${t1}\t${type}\t${error.code}\t${error.message}\n`,
    );
    return Promise.reject(error);
  },
);

class KAPI {
  static reqStreams = (cursor = '') => {
    const url = 'https://api.twitch.tv/helix/streams';
    const config = {
      headers: {
        Authorization: `Bearer ${process.env.ACCESS_TOKEN}`,
        'Client-Id': process.env.CLIENT_ID,
      },
      params: {
        first: 100,
        after: cursor,
      },

      kukudy: {
        type: 'reqStreams',
        t1: getTS(),
      },
    };

    return kaxios.get(url, config);
  };

  static reqPlaybackAccessToken = (userLogin) => {
    const url = 'https://gql.twitch.tv/gql';
    const data = JSON.stringify({
      operationName: 'PlaybackAccessToken_Template',
      query:
        'query PlaybackAccessToken_Template($login: String!, $isLive: Boolean!, $vodID: ID!, $isVod: Boolean!, $playerType: String!) {  streamPlaybackAccessToken(channelName: $login, params: {platform: "web", playerBackend: "mediaplayer", playerType: $playerType}) @include(if: $isLive) {    value    signature    __typename  }  videoPlaybackAccessToken(id: $vodID, params: {platform: "web", playerBackend: "mediaplayer", playerType: $playerType}) @include(if: $isVod) {    value    signature    __typename  }}',
      variables: {
        isLive: true,
        login: userLogin,
        isVod: false,
        vodID: '',
        playerType: 'site',
      },
    });
    const config = {
      headers: { 'Client-Id': process.env.CLIENT_ID_GQL },
      kukudy: {
        type: 'reqPAT',
        t1: getTS(),
      },
    };

    return kaxios.post(url, data, config);
  };

  static reqUsherM3U8 = (sPAToken, userLogin) => {
    const url = `https://usher.ttvnw.net/api/channel/hls/${userLogin}.m3u8`;
    const config = {
      params: {
        client_id: process.env.CLIENT_ID,

        player: 'twitchweb',
        token: sPAToken.value,
        sig: sPAToken.signature,
        allow_audio_only: false,
        fast_bread: true,
        allow_source: true,
        p: Math.round(Math.random() * 1000000),
      },
      kukudy: {
        type: 'reqUsherM3U8',
        t1: getTS(),
      },
    };

    return kaxios.get(url, config);
  };

  static reqGet = (url) => {
    const config = {
      kukudy: {
        type: 'reqGet',
        t1: getTS(),
      },
    };
    return kaxios.get(url, config);
  };
}

module.exports = KAPI;
