const fs = require("fs");
const request = require("request");
const got = require("got");
const jsdom = require("jsdom");
const readline = require("readline");
const { JSDOM } = jsdom;
const { EOL } = require("os");
const { exit } = require("process");

const url = "https://www.freelancer.com/u/";
const path = "./users/";

async function downloadImage(url, filename) {
  try {
    await request.head(url, async function (err, res, body) {
      await request(url).pipe(fs.createWriteStream(filename));
    });
  } catch (e) {
    console.log(e);
  }
}

(async () => {
  if (!fs.existsSync(path)) fs.mkdirSync(path);

  if (!fs.existsSync("ids.txt")) {
    console.log("ids.txt does not exist");
    exit(0);
  }

  const rs = fs.createReadStream("ids.txt");
  // const ws = fs.createWriteStream("tmp.txt");

  const comma = ",";

  const lineReader = readline.createInterface({
    input: rs
  });

  for await (const line of lineReader) {
    let arr = line.split(comma);
    console.log("************************************", line)
    if (arr.length == 3) {
      let id = arr[0];
      let country = arr[1];
      // let logo = arr[2];

      try {
        const res = await got(url + id);
        const dom = new JSDOM(res.body);
        const document = dom.window.document;
        let json = document.querySelector("#webapp-state").innerHTML;
        const data = JSON.parse(json.replace(/&q;/g, '"'));

        let name = document
          .querySelector(".NameContainer-name h3")
          .textContent.replace(/[^a-zA-Z& ]/g, "")
          .replace(/\s\s+/g, " ")
          .trim();
        // const nodeList = [
        //   ...document.querySelectorAll(".PortfolioItemCard-file-image img")
        // ];

        let images = [];
        const documents = data.NGRX_STATE.portfolios[0].documents;
        for (key in documents) {
          documents[key].rawDocument.files.forEach(file => {
            images.push(file.cdnUrl);
          });
        }

        await images.forEach(async (image, index) => {
          var str = "" + (index + 1);
          var pad = "0000";
          var ans = pad.substring(0, pad.length - str.length) + str;
          // console.log(ans);
          let pPath = path + country + "-" + id + "-" + ans + ".jpg";
          console.log("=====file name===", pPath);
          console.log("======url======", image);
          await downloadImage(image, pPath);
        });

        //ws.write(row + EOL);
        console.log(name);
      } catch (e) {
        // console.log(e);
      }
    }
  }
  //ws.close();
  rs.close();
})();
