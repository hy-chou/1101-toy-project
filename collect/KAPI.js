const axios = require("axios");

require("dotenv").config({ path: "../.env" });

const kaxios = axios.create({
  timeout: 30 * 1000,
  headers: { keepAlive: true },
});

class KAPI {
  static get = (url) => {
    return kaxios.get(url);
  };

  static getStreams = (cursor = "") => {
    const url = "https://api.twitch.tv/helix/streams";
    const config = {
      headers: {
        Authorization: `Bearer ${process.env.ACCESS_TOKEN}`,
        "Client-Id": process.env.CLIENT_ID,
      },
      params: {
        first: 100,
        after: cursor,
      },
    };

    return kaxios.get(url, config);
  };

  static getMasterPlaylist = (token, channel = "twitchdev") => {
    const url = `https://usher.ttvnw.net/api/channel/hls/${channel}.m3u8`;
    const config = {
      params: {
        client_id: process.env.CLIENT_ID,

        player: "twitchweb",
        token: token.value,
        sig: token.signature,
        allow_audio_only: false,
        fast_bread: true,
        allow_source: true,
        p: Math.round(Math.random() * 1000000),
      },
    };

    return kaxios.get(url, config);
  };

  static getPlaybackAccessToken = (channel) => {
    const url = "https://gql.twitch.tv/gql";
    const data = JSON.stringify({
      operationName: "PlaybackAccessToken_Template",
      query:
        'query PlaybackAccessToken_Template($login: String!, $isLive: Boolean!, $vodID: ID!, $isVod: Boolean!, $playerType: String!) {  streamPlaybackAccessToken(channelName: $login, params: {platform: "web", playerBackend: "mediaplayer", playerType: $playerType}) @include(if: $isLive) {    value    signature    __typename  }  videoPlaybackAccessToken(id: $vodID, params: {platform: "web", playerBackend: "mediaplayer", playerType: $playerType}) @include(if: $isVod) {    value    signature    __typename  }}',
      variables: {
        isLive: true,
        login: channel,
        isVod: false,
        vodID: "",
        playerType: "site",
      },
    });
    const config = { headers: { "Client-Id": process.env.CLIENT_ID_GQL } };

    return kaxios.post(url, data, config);
  };
}

module.exports = KAPI;
