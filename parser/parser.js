var config = require('./parserConfig.js'); 
var snoowrap = require('snoowrap');
var sqlite = require('sqlite');

const reddit = new snoowrap ({
    userAgent: config.userAgent,
    clientId: config.clientId,
    clientSecret: config.clientSecret,
    username: config.username,
    password: config.password
})

var dbPromise = sqlite.open('./rsc/users.db', { Promise });

async function getUsers() {
    db = await dbPromise;
    return users = await db.get( "SELECT DISTINCT ID, sub, query, udid FROM users Group BY sub, query, udid ORDER BY id");
}

async function downloadNewPost() {
   const users = await getUsers()
   console.log(users)
   return reddit.getSubreddit('rocketleagueexchange').getNew()
    .filter(post => post.title.indexOf(users.query) > -1).then((post) => post.forEach((submission) => console.log(submission.title)));
}; 

//setInterval(downloadNewPost, 1500)
//getUsers();
downloadNewPost();
