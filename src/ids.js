// const cheerio = require('cheerio');
const fs = require('fs');
const request = require('request');
const got = require("got");
const { EOL } = require('os');

const url =
  "https://www.freelancer.com/ajax/directory/getFreelancer.php?jobs%5B%5D=370";
const path = './logos/';

function downloadImage(url, filename) {
  request.head(url, function(err, res, body){
    request(url).pipe(fs.createWriteStream(filename));
  });
}

(async () => {
  let total = 0;
  let page = 0;
  let ws = fs.createWriteStream("users.txt");
  while (1) {
    let offset = page * 10;
    const res = await got(url + "&offset=" + offset);
    let data = JSON.parse(res.body);

    if (data.status == "success") {
      total += data.users.length;
      console.log("---- Page " + page + ' ----');
      page++;
      data.users.forEach(user => {
        console.log(user.username);
        ws.write(user.username + "," + user.country + "," + user.logo_url + EOL);
        /*if (user.logo_url)
          downloadImage(user.logo_url, path + user.username + '(' + user.country + ').jpg');*/
      });
    } else break;
  }
})();