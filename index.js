const cron = require("node-cron");
const fs = require("fs");
const process = require('process');
const { getTopIP } = require("../Jujuby/Prober/Utils/getTopIP.js");

cron.schedule("* 40-59 9 * * *", ()=>{getTopIP(10);});
cron.schedule("0    0 10 * * *", ()=>{process.exit();});
