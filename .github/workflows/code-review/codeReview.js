const https = require("https");

function getArg(argName) {
  const index = process.argv.indexOf("--" + argName);
  if (index > -1 && index + 1 < process.argv.length) {
    return process.argv[index + 1];
  }
}

console.log(process.argv);

const prLink = getArg("pr");
console.log(prLink);

const requesterArg = getArg("user");
console.log(requesterArg);
