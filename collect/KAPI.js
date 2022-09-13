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
    return kaxios.get("https://api.twitch.tv/helix/streams", {
      headers: {
        Authorization: `Bearer ${process.env.ACCESS_TOKEN}`,
        "Client-Id": process.env.CLIENT_ID,
      },
      params: {
        first: 100,
        after: cursor,
      },
    });
  };

  static getMasterPlaylist = (token, channel = "twitchdev") => {
    return kaxios.get(
      `https://usher.ttvnw.net/api/channel/hls/${channel}.m3u8`,
      {
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
      }
    );
  };
}

module.exports = KAPI;
